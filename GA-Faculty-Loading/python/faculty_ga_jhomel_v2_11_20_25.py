#!/usr/bin/env python3
"""
Faculty Loading Genetic Algorithm - Version 2

MEETING SCHEDULE:
 - Each course can have separate lecture and laboratory meetings
 - Meetings are scheduled with appropriate durations based on course requirements

FACULTY EXPERTISE SYSTEM:
 - All assignments (lecture or lab) only consider faculty listed in faculty_expertise for that course
 - When multiple eligible faculty exist, the algorithm picks the one with the LOWEST projected load
 - No fallback to non-expert faculty

LOAD CALCULATION:
 - Lecture: Each hour counts as 1 unit toward faculty load
 - Laboratory: Each hour counts as 1/3 unit toward faculty load
 - Maximum faculty load: 18 units

ROOM REQUIREMENTS:
 - Room type must match the course type (Lecture or Laboratory)
 - Room capacity must be greater than or equal to the class size
 - Room must be free for the entire block (schedule + other_schedule)
 - Room must be available for the entire block (schedule + other_schedule)
 - Room must be available and conflict-free with all existing schedules

TIME SLOT CONSTRAINTS:
 - Classes run from 8 AM to 6 PM (10 time slots per day)
 - 5 days per week (Monday to Friday)
 - No overnight or multi-day classes allowed
 - Classes must fit within available time slots

Requirements: sqlalchemy, pymysql
"""

import random
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from copy import deepcopy
from sqlalchemy import create_engine, Table, MetaData, select

# =========================
# MySQL Connection (adjust creds/host/db as needed)
# =========================
DB_USER = "root"
DB_PASS = "root"
DB_HOST = "127.0.0.2"
DB_PORT = 3306
DB_NAME = "dnsc_class_scheduler_ga3"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
    echo=False,
)
metadata = MetaData()

# Data structures


@dataclass
class Assignment:
    """Represents a single teaching assignment (lecture OR lab meeting)"""
    class_id: int
    course_id: int
    faculty_id: int
    room_id: int
    time_slot: int  # 0-49 (5 days × 10 slots per day)
    meeting_type: str  # 'lecture' or 'laboratory'
    duration: int  # hours for this meeting

    def __hash__(self):
        return hash((self.class_id, self.course_id, self.faculty_id,
                    self.room_id, self.time_slot, self.meeting_type))


class Chromosome:
    """Represents a complete schedule (solution)"""

    def __init__(self, assignments: List[Assignment]):
        self.assignments = assignments
        self.fitness = 0.0

    def copy(self):
        return Chromosome([Assignment(**vars(a)) for a in self.assignments])


class FacultyLoadingGA:
    """
    Genetic Algorithm for Faculty Loading and Scheduling.
    
    ROOM CONSTRAINTS IMPLEMENTATION:
    ==================================
    This class implements comprehensive room constraints throughout the scheduling process:
    
    1. Room Type Matching:
       - Laboratory courses are assigned to Laboratory rooms
       - Lecture courses are assigned to Lecture rooms
       - Enforced in: _get_suitable_rooms(), fitness calculation
    
    2. Room Capacity Validation:
       - Room capacity must be >= class size
       - Larger capacity shortages receive proportionally higher penalties
       - Enforced in: _get_suitable_rooms(), fitness calculation
    
    3. Room Time Availability:
       - Rooms cannot have overlapping assignments
       - Checked for entire duration of each class
       - Enforced in: _is_room_available(), _get_suitable_rooms(), fitness calculation
    
    4. Optimal Room Usage:
       - Rewards efficient use of room capacity (70-100% full)
       - Prevents unnecessary use of oversized rooms
       - Enforced in: fitness calculation
    
    Methods implementing room constraints:
    - _is_room_available(): Checks if room is free for given time block
    - _get_suitable_rooms(): Returns rooms matching type, capacity, and availability
    - calculate_fitness(): Penalizes room constraint violations
    - mutate(): Ensures mutations respect room constraints
    """
    
    def __init__(self, rooms, faculty, faculty_expertise, courses, classes, program_year_courses):
        # Load data
        self.rooms = {r['room_id']: r for r in rooms}
        self.faculty = {f['faculty_id']: f for f in faculty}
        self.faculty_expertise = self._build_expertise_map(faculty_expertise)
        self.courses = {c['course_id']: c for c in courses}
        self.classes = {c['class_id']: c for c in classes}
        self.program_year_courses = program_year_courses

        # GA parameters
        self.population_size = 150
        self.generations = 300
        self.mutation_rate = 0.2
        self.crossover_rate = 0.8
        self.elite_size = 15

        # Faculty load limit
        self.max_faculty_load = 18.0

        # Time slots: 5 days × 9 slots (8AM-12PM, 1PM-6PM, excluding 12-1PM lunch)
        # Available hours per day: 8-9, 9-10, 10-11, 11-12, [LUNCH], 1-2, 2-3, 3-4, 4-5, 5-6
        self.slots_per_day = 9  # 4 morning + 5 afternoon
        self.total_time_slots = 5 * self.slots_per_day  # 45 total slots
        self.lunch_hour = 12  # 12 PM (noon)

        # Build teaching requirements
        self.teaching_requirements = self._build_requirements()

    def _build_expertise_map(self, faculty_expertise):
        """Build a map of course to qualified faculty"""
        expertise_map = {}  # course_id -> [faculty_ids]
        for entry in faculty_expertise:
            cid = entry['course_id']
            fid = entry['faculty_id']
            if cid not in expertise_map:
                expertise_map[cid] = []
            expertise_map[cid].append(fid)
        return expertise_map

    def _slot_to_hour(self, slot_in_day):
        """Convert slot number (0-8) to actual hour (8-18), skipping lunch (12)"""
        if slot_in_day < 4:
            # Morning slots: 8, 9, 10, 11
            return 8 + slot_in_day
        else:
            # Afternoon slots: 13, 14, 15, 16, 17
            # Skip lunch hour (12), so add 1 to skip from 12 to 13
            return 8 + slot_in_day + 1

    def _is_valid_time_block(self, start_slot_in_day, duration):
        """Check if a time block is valid (doesn't span lunch break)"""
        if duration <= 0:
            return False

        start_hour = self._slot_to_hour(start_slot_in_day)
        end_hour = start_hour + duration

        # Check if block spans across lunch (12-13)
        if start_hour < self.lunch_hour < end_hour:
            return False  # Block would span lunch break

        # Check if block fits within day (8AM-6PM)
        if end_hour > 18:
            return False

        return True

    def _build_requirements(self):
        """Build list of required class-course combinations with meeting details"""
        requirements = []

        for pyc in self.program_year_courses:
            program_id = pyc['program_id']
            course_id = pyc['course_id']
            year_level = pyc['year_level']

            # Find all classes for this program and year level
            for class_id, class_info in self.classes.items():
                if (class_info['program_id'] == program_id and
                        self._extract_year(class_info['set_name']) == year_level):

                    course = self.courses[course_id]

                    # Create separate requirements for lecture and lab
                    if course['course_lecture'] > 0:
                        requirements.append({
                            'class_id': class_id,
                            'course_id': course_id,
                            'class_size': class_info['class_size'],
                            'program_id': program_id,
                            'meeting_type': 'lecture',
                            # lecture hours
                            'duration': course['course_lecture']
                        })

                    if course['course_laboratory'] > 0:
                        # Lab: Use the course_laboratory value directly as hours
                        # (already represents actual hours, not units)
                        lab_hours = course['course_laboratory']
                        requirements.append({
                            'class_id': class_id,
                            'course_id': course_id,
                            'class_size': class_info['class_size'],
                            'program_id': program_id,
                            'meeting_type': 'laboratory',
                            'duration': lab_hours
                        })

        return requirements

    def _extract_year(self, set_name: str) -> int:
        """Extract year level from set_name like '1st Year - A'"""
        if '1st' in set_name:
            return 1
        elif '2nd' in set_name:
            return 2
        elif '3rd' in set_name:
            return 3
        elif '4th' in set_name:
            return 4
        return 1

    def _get_qualified_faculty(self, course_id: int) -> List[int]:
        """Get faculty who are qualified to teach this course (from expertise only)"""
        return self.faculty_expertise.get(course_id, [])

    def _calculate_faculty_load(self, faculty_id: int, assignments: List[Assignment]) -> float:
        """Calculate total load for a faculty member"""
        load = 0.0
        for assignment in assignments:
            if assignment.faculty_id == faculty_id:
                if assignment.meeting_type == 'lecture':
                    load += assignment.duration  # 1 hour = 1 unit
                else:  # laboratory
                    load += assignment.duration / 3.0  # 3 hours = 1 unit
        return load

    def _select_faculty_by_load(self, qualified_faculty: List[int],
                                current_assignments: List[Assignment]) -> int:
        """Select faculty with lowest projected load"""
        if not qualified_faculty:
            return None

        # Calculate current loads
        loads = {}
        for fid in qualified_faculty:
            loads[fid] = self._calculate_faculty_load(fid, current_assignments)

        # Find minimum load
        min_load = min(loads.values())

        # Get all faculty with minimum load (for tie-breaking)
        candidates = [fid for fid, load in loads.items() if load == min_load]

        return random.choice(candidates)
    
    def _is_room_available(self, room_id: int, time_slot: int, duration: int, 
                           current_assignments: List[Assignment], exclude_assignment=None) -> bool:
        """
        Check if a room is available for the entire duration at the given time slot.
        
        ROOM AVAILABILITY CONSTRAINTS:
        - Room must be free for all time slots in [time_slot, time_slot + duration)
        - No overlapping assignments in the same room
        - Checks against all existing assignments
        """
        for assignment in current_assignments:
            # Skip if this is the assignment we're trying to reschedule
            if exclude_assignment and assignment is exclude_assignment:
                continue
                
            # Check if same room
            if assignment.room_id == room_id:
                # Check for time overlap
                if self._time_overlap(time_slot, duration, 
                                     assignment.time_slot, assignment.duration):
                    return False
        return True
    
    def _get_suitable_rooms(self, meeting_type: str, class_size: int, 
                           time_slot: int = None, duration: int = None,
                           current_assignments: List[Assignment] = None) -> List[int]:
        """
        Get rooms suitable for this meeting type with comprehensive constraints.
        
        ROOM CONSTRAINT CHECKS:
        1. Room type must match course type (Lecture/Laboratory)
        2. Room capacity must be >= class size
        3. Room must be available for the entire time block (if time_slot provided)
        """
        suitable = []

        for room_id, room in self.rooms.items():
            # CONSTRAINT 1: Check room capacity
            if room['room_capacity'] < class_size:
                continue  # Skip rooms that are too small
            
            # CONSTRAINT 2: Check room type matches meeting type
            room_type_match = False
            if meeting_type == 'laboratory' and room['room_type'] == 'Laboratory':
                room_type_match = True
            elif meeting_type == 'lecture' and room['room_type'] == 'Lecture':
                room_type_match = True
            
            if not room_type_match:
                continue  # Skip rooms with wrong type
            
            # CONSTRAINT 3: Check time availability (if time_slot is provided)
            if time_slot is not None and duration is not None and current_assignments is not None:
                if not self._is_room_available(room_id, time_slot, duration, current_assignments):
                    continue  # Skip rooms that are already occupied
            
            suitable.append(room_id)
        
        # Fallback 1: If no suitable rooms with correct type, try rooms with just correct capacity
        if not suitable:
            for room_id, room in self.rooms.items():
                if room['room_capacity'] >= class_size:
                    if time_slot is not None and duration is not None and current_assignments is not None:
                        if self._is_room_available(room_id, time_slot, duration, current_assignments):
                            suitable.append(room_id)
                    else:
                        suitable.append(room_id)
        
        # Fallback 2: Return any room if desperate (will be heavily penalized in fitness)
        if not suitable:
            suitable = list(self.rooms.keys())
        
        return suitable
    
    def create_individual(self) -> Chromosome:
        """Create a random valid schedule with faculty consistency"""
        assignments = []
        course_faculty_map = {}  # (class_id, course_id) -> faculty_id

        for req in self.teaching_requirements:
            class_id = req['class_id']
            course_id = req['course_id']
            class_size = req['class_size']
            meeting_type = req['meeting_type']
            duration = req['duration']

            # Get qualified faculty only
            qualified_faculty = self._get_qualified_faculty(course_id)
            if not qualified_faculty:
                continue  # Skip if no qualified faculty

            # Check if faculty already assigned to this class-course
            key = (class_id, course_id)
            if key in course_faculty_map:
                faculty_id = course_faculty_map[key]
            else:
                # Select faculty with lowest load
                faculty_id = self._select_faculty_by_load(qualified_faculty, assignments)
                course_faculty_map[key] = faculty_id  # Remember for consistency
            
            # Assign time slot and room with comprehensive validation
            attempts = 0
            time_slot = 0
            room_id = None
            
            while attempts < 100:
                attempts += 1
                day = random.randint(0, 4)  # 5 days
                day_start = day * self.slots_per_day

                # Try random slots that don't span lunch break
                slot_in_day = random.randint(0, self.slots_per_day - 1)

                # Validate that this time block doesn't span lunch
                if not self._is_valid_time_block(slot_in_day, duration):
                    continue
                
                time_slot = day_start + slot_in_day
                
                # Get suitable rooms that are available at this time
                # ROOM CONSTRAINTS: type match, capacity, and time availability
                suitable_rooms = self._get_suitable_rooms(
                    meeting_type, class_size, time_slot, duration, assignments
                )
                
                if suitable_rooms:
                    room_id = random.choice(suitable_rooms)
                    break  # Found valid time slot and room
            
            # If couldn't find valid slot and room after attempts, use fallback
            if room_id is None:
                # Get rooms without time checking (will be penalized in fitness)
                suitable_rooms = self._get_suitable_rooms(meeting_type, class_size)
                room_id = random.choice(suitable_rooms) if suitable_rooms else random.choice(list(self.rooms.keys()))
                # Use a random valid time slot
                day = random.randint(0, 4)
                slot_in_day = random.randint(0, max(0, self.slots_per_day - duration))
                time_slot = day * self.slots_per_day + slot_in_day
            
            assignment = Assignment(
                class_id=class_id,
                course_id=course_id,
                faculty_id=faculty_id,
                room_id=room_id,
                time_slot=time_slot,
                meeting_type=meeting_type,
                duration=duration
            )
            assignments.append(assignment)

        return Chromosome(assignments)

    def calculate_fitness(self, chromosome: Chromosome) -> float:
        """
        Calculate fitness score (higher is better).
        
        ROOM CONSTRAINTS ENFORCED:
        1. Room Capacity: Room capacity must be >= class size (penalty: 500 + 10 per student over)
        2. Room Type Match: 
           - Laboratory meetings require Laboratory rooms (penalty: 400)
           - Lecture meetings require Lecture rooms (penalty: 150)
        3. Room Availability: Same room cannot be used at overlapping times (penalty: 800)
        4. Optimal Usage: Bonus for rooms 70-100% full (reward: +10)
        
        All room constraints are validated in multiple places:
        - During individual creation (_get_suitable_rooms with time checking)
        - During mutation (room reassignment with availability check)
        - During fitness evaluation (penalties for violations)
        """
        score = 10000.0

        # Track conflicts
        faculty_schedule = {}  # faculty_id -> [(time_slot, duration)]
        room_schedule = {}     # room_id -> [(time_slot, duration)]
        class_schedule = {}    # class_id -> [(time_slot, duration)]

        for assignment in chromosome.assignments:
            # HARD CONSTRAINTS (heavy penalties)

            # 1. Faculty expertise - MUST be qualified (no fallback)
            qualified = self._get_qualified_faculty(assignment.course_id)
            if assignment.faculty_id not in qualified:
                score -= 1000  # Massive penalty for unqualified faculty

            # 2. Faculty load limit check
            faculty_load = self._calculate_faculty_load(
                assignment.faculty_id, chromosome.assignments)
            if faculty_load > self.max_faculty_load:
                overload = faculty_load - self.max_faculty_load
                score -= overload * 200  # Heavy penalty for overload
            
            # 3. ROOM CONSTRAINTS - Comprehensive validation
            req = next((r for r in self.teaching_requirements 
                       if r['class_id'] == assignment.class_id 
                       and r['course_id'] == assignment.course_id
                       and r['meeting_type'] == assignment.meeting_type), None)

            if req:
                room = self.rooms.get(assignment.room_id)
                if room:
                    # ROOM CONSTRAINT 1: Capacity must be adequate
                    # Room capacity must be >= class size
                    if room['room_capacity'] < req['class_size']:
                        capacity_shortage = req['class_size'] - room['room_capacity']
                        score -= 500 + (capacity_shortage * 10)  # Larger shortage = bigger penalty
                    
                    # ROOM CONSTRAINT 2: Room type must match meeting type
                    # Laboratory courses need laboratory rooms, lectures need lecture rooms
                    if assignment.meeting_type == 'laboratory':
                        if room['room_type'] != 'Laboratory':
                            score -= 400  # Heavy penalty for lab in non-lab room
                    elif assignment.meeting_type == 'lecture':
                        if room['room_type'] != 'Lecture':
                            score -= 150  # Moderate penalty for lecture in non-lecture room
                    
                    # ROOM CONSTRAINT 3: Bonus for optimal room usage
                    # Reward for using room close to actual class size (not too oversized)
                    if room['room_capacity'] >= req['class_size']:
                        capacity_ratio = req['class_size'] / room['room_capacity']
                        if capacity_ratio >= 0.7:  # Room is 70-100% full
                            score += 10  # Small bonus for efficient room usage
                else:
                    # Room doesn't exist - critical error
                    score -= 1000
            
            # 5. Faculty conflicts (same faculty, same time)
            fid = assignment.faculty_id
            if fid not in faculty_schedule:
                faculty_schedule[fid] = []

            for start, dur in faculty_schedule[fid]:
                if self._time_overlap(assignment.time_slot, assignment.duration, start, dur):
                    score -= 800  # Heavy penalty for faculty conflict

            faculty_schedule[fid].append(
                (assignment.time_slot, assignment.duration))

            # 6. Room conflicts (same room, same time)
            rid = assignment.room_id
            if rid not in room_schedule:
                room_schedule[rid] = []

            for start, dur in room_schedule[rid]:
                if self._time_overlap(assignment.time_slot, assignment.duration, start, dur):
                    score -= 800  # Heavy penalty for room conflict

            room_schedule[rid].append(
                (assignment.time_slot, assignment.duration))

            # 7. Class conflicts (same class, same time)
            cid = assignment.class_id
            if cid not in class_schedule:
                class_schedule[cid] = []

            for start, dur in class_schedule[cid]:
                if self._time_overlap(assignment.time_slot, assignment.duration, start, dur):
                    score -= 800  # Heavy penalty for class conflict

            class_schedule[cid].append(
                (assignment.time_slot, assignment.duration))

            # SOFT CONSTRAINTS (minor penalties)

            # 8. Time slot must fit within day and not span lunch break
            day_idx = assignment.time_slot // self.slots_per_day
            slot_in_day = assignment.time_slot % self.slots_per_day
            start_hour = self._slot_to_hour(slot_in_day)
            end_hour = start_hour + assignment.duration

            # Heavy penalty for spanning lunch break
            if start_hour < self.lunch_hour < end_hour:
                score -= 500  # CANNOT span lunch break

            # Penalty for extending past 6 PM
            if end_hour > 18:
                score -= 400

            # 9. Prefer reasonable time slots (not too late)
            if end_hour > 17:  # After 5 PM
                score -= 20

            # 10. Prefer morning for long sessions
            if assignment.duration >= 3 and start_hour > 11:
                score -= 10

        # 11. Faculty workload balance (encourage even distribution)
        faculty_loads = {}
        for assignment in chromosome.assignments:
            fid = assignment.faculty_id
            load = self._calculate_faculty_load(fid, [assignment])
            faculty_loads[fid] = faculty_loads.get(fid, 0.0) + load

        if faculty_loads:
            avg_load = sum(faculty_loads.values()) / len(faculty_loads)
            for load in faculty_loads.values():
                if load <= self.max_faculty_load:  # Only consider valid loads
                    deviation = abs(load - avg_load)
                    score -= deviation * 2

        # 12. Check that both lecture and lab (if exist) are assigned for each class-course
        course_meetings = {}  # (class_id, course_id) -> set of meeting_types
        for assignment in chromosome.assignments:
            key = (assignment.class_id, assignment.course_id)
            if key not in course_meetings:
                course_meetings[key] = set()
            course_meetings[key].add(assignment.meeting_type)

        for req in self.teaching_requirements:
            key = (req['class_id'], req['course_id'])
            if key in course_meetings:
                if req['meeting_type'] not in course_meetings[key]:
                    score -= 300  # Missing required meeting

        # 13. Faculty consistency: same faculty for lecture AND lab of same course-class
        course_faculty = {}  # (class_id, course_id) -> set of faculty_ids
        for assignment in chromosome.assignments:
            key = (assignment.class_id, assignment.course_id)
            if key not in course_faculty:
                course_faculty[key] = set()
            course_faculty[key].add(assignment.faculty_id)

        for key, faculty_set in course_faculty.items():
            if len(faculty_set) > 1:
                score -= 1000  # HEAVY penalty for different faculty teaching same course-class

        return max(score, 0)

    def _time_overlap(self, start1: int, dur1: int, start2: int, dur2: int) -> bool:
        """Check if two time slots overlap"""
        end1 = start1 + dur1
        end2 = start2 + dur2
        return not (end1 <= start2 or end2 <= start1)

    def selection(self, population: List[Chromosome]) -> Chromosome:
        """Tournament selection"""
        tournament_size = 7
        tournament = random.sample(population, min(
            tournament_size, len(population)))
        return max(tournament, key=lambda x: x.fitness)

    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        """Two-point crossover"""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()

        length = len(parent1.assignments)
        point1 = random.randint(1, length - 2)
        point2 = random.randint(point1 + 1, length - 1)

        child1_assignments = (parent1.assignments[:point1] +
                              parent2.assignments[point1:point2] +
                              parent1.assignments[point2:])

        child2_assignments = (parent2.assignments[:point1] +
                              parent1.assignments[point1:point2] +
                              parent2.assignments[point2:])

        return Chromosome(child1_assignments), Chromosome(child2_assignments)

    def mutate(self, chromosome: Chromosome):
        """
        Mutation: randomly change assignment attributes with room constraint validation.
        Ensures mutations respect room capacity, type, and availability.
        """
        for i, assignment in enumerate(chromosome.assignments):
            if random.random() < self.mutation_rate:
                mutation_type = random.randint(0, 2)

                req = next((r for r in self.teaching_requirements
                            if r['class_id'] == assignment.class_id
                            and r['course_id'] == assignment.course_id
                            and r['meeting_type'] == assignment.meeting_type), None)

                if not req:
                    continue

                if mutation_type == 0:  # Change faculty (must be qualified)
                    qualified = self._get_qualified_faculty(
                        assignment.course_id)
                    if qualified:
                        # Select based on lowest load
                        assignment.faculty_id = self._select_faculty_by_load(
                            qualified, chromosome.assignments)
                
                elif mutation_type == 1:  # Change room with full constraint checking
                    # Get suitable rooms considering current time slot and availability
                    # ROOM CONSTRAINTS: type, capacity, and time availability
                    suitable = self._get_suitable_rooms(
                        assignment.meeting_type, 
                        req['class_size'],
                        assignment.time_slot,
                        assignment.duration,
                        chromosome.assignments
                    )
                    if suitable:
                        assignment.room_id = random.choice(suitable)
                    else:
                        # Fallback: try without time checking
                        suitable = self._get_suitable_rooms(assignment.meeting_type, req['class_size'])
                        if suitable:
                            assignment.room_id = random.choice(suitable)
                
                else:  # Change time slot and potentially room (respecting lunch break)
                    attempts = 0
                    found_valid = False
                    
                    while attempts < 50 and not found_valid:
                        attempts += 1
                        day = random.randint(0, 4)
                        day_start = day * self.slots_per_day
                        slot_in_day = random.randint(0, self.slots_per_day - 1)
                        
                        # Check if time block is valid (doesn't span lunch)
                        if not self._is_valid_time_block(slot_in_day, assignment.duration):
                            continue
                        
                        new_time_slot = day_start + slot_in_day
                        
                        # Check if current room is available at new time
                        # ROOM CONSTRAINT: Room must be free at new time slot
                        if self._is_room_available(
                            assignment.room_id, 
                            new_time_slot, 
                            assignment.duration,
                            chromosome.assignments,
                            exclude_assignment=assignment
                        ):
                            assignment.time_slot = new_time_slot
                            found_valid = True
                        else:
                            # Try to find a different room that's available
                            suitable_rooms = self._get_suitable_rooms(
                                assignment.meeting_type,
                                req['class_size'],
                                new_time_slot,
                                assignment.duration,
                                chromosome.assignments
                            )
                            if suitable_rooms:
                                assignment.time_slot = new_time_slot
                                assignment.room_id = random.choice(suitable_rooms)
                                found_valid = True
    
    def evolve(self):
        """Main GA loop"""
        # Initialize population
        population = [self.create_individual()
                      for _ in range(self.population_size)]

        # Evaluate initial population
        for individual in population:
            individual.fitness = self.calculate_fitness(individual)

        best_solution = max(population, key=lambda x: x.fitness)

        print(f"Generation 0: Best Fitness = {best_solution.fitness:.2f}")

        no_improvement_count = 0
        best_fitness_ever = best_solution.fitness

        for generation in range(1, self.generations + 1):
            new_population = []

            # Elitism: keep best individuals
            population.sort(key=lambda x: x.fitness, reverse=True)
            new_population.extend([ind.copy()
                                  for ind in population[:self.elite_size]])

            # Create new individuals
            while len(new_population) < self.population_size:
                parent1 = self.selection(population)
                parent2 = self.selection(population)

                child1, child2 = self.crossover(parent1, parent2)

                self.mutate(child1)
                self.mutate(child2)

                child1.fitness = self.calculate_fitness(child1)
                child2.fitness = self.calculate_fitness(child2)

                new_population.extend([child1, child2])

            population = new_population[:self.population_size]

            current_best = max(population, key=lambda x: x.fitness)
            if current_best.fitness > best_solution.fitness:
                best_solution = current_best
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if current_best.fitness > best_fitness_ever:
                best_fitness_ever = current_best.fitness

            if generation % 30 == 0:
                print(
                    f"Generation {generation}: Best Fitness = {best_solution.fitness:.2f}")

            # Early stopping if no improvement for 50 generations
            if no_improvement_count >= 50:
                print(
                    f"Early stopping at generation {generation} (no improvement)")
                break

        print(f"\nFinal Best Fitness: {best_solution.fitness:.2f}")
        return best_solution

    def format_schedule(self, chromosome: Chromosome) -> str:
        """Format the schedule for display"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        output = []

        output.append("=" * 120)
        output.append("FACULTY LOADING SCHEDULE")
        output.append("=" * 120)

        # Group by class and course
        schedule_by_class = {}
        for assignment in chromosome.assignments:
            key = (assignment.class_id, assignment.course_id)
            if key not in schedule_by_class:
                schedule_by_class[key] = []
            schedule_by_class[key].append(assignment)

        # Display schedule
        for (class_id, course_id), assignments in sorted(schedule_by_class.items()):
            class_info = self.classes[class_id]
            course = self.courses[course_id]

            output.append(f"\n{'='*120}")
            output.append(
                f"Class: {class_info['set_name']} | Course: {course['course_code']}")
            output.append(f"Class Size: {class_info['class_size']} students")
            output.append(
                f"Course Units: Lecture={course['course_lecture']}, Laboratory={course['course_laboratory']}")
            output.append(f"{'-'*120}")

            for assignment in sorted(assignments, key=lambda x: x.time_slot):
                faculty = self.faculty[assignment.faculty_id]
                room = self.rooms[assignment.room_id]

                day_idx = assignment.time_slot // self.slots_per_day
                slot_in_day = assignment.time_slot % self.slots_per_day
                start_hour = self._slot_to_hour(slot_in_day)
                end_hour = start_hour + assignment.duration

                # Calculate load contribution
                if assignment.meeting_type == 'lecture':
                    load_units = assignment.duration
                else:
                    load_units = assignment.duration / 3.0

                output.append(
                    f"  Meeting Type: {assignment.meeting_type.upper()}")
                output.append(
                    f"  Faculty: {faculty['name']} (Load contribution: {load_units:.2f} units)")
                output.append(
                    f"  Room: {room['room_name']} (Capacity: {room['room_capacity']}, Type: {room['room_type']})")
                output.append(
                    f"  Schedule: {days[day_idx]}, {start_hour:02d}:00 - {end_hour:02d}:00 ({assignment.duration} hours)")
                output.append(f"{'-'*120}")

        # Faculty load summary
        output.append(f"\n{'='*120}")
        output.append("FACULTY LOAD SUMMARY")
        output.append(f"{'='*120}")

        faculty_loads = {}
        for assignment in chromosome.assignments:
            fid = assignment.faculty_id
            load = self._calculate_faculty_load(fid, [assignment])
            faculty_loads[fid] = faculty_loads.get(fid, 0.0) + load

        for fid, load in sorted(faculty_loads.items()):
            faculty = self.faculty[fid]
            status = "[OK]" if load <= self.max_faculty_load else "[OVERLOAD]"
            output.append(
                f"{faculty['name']}: {load:.2f} / {self.max_faculty_load} units {status}")

        return "\n".join(output)

    def to_json(self, chromosome: Chromosome) -> dict:
        """Convert schedule to JSON format for backend"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        schedule_data = {}

        # Group by class (set)
        by_set = {}
        for assignment in chromosome.assignments:
            class_info = self.classes[assignment.class_id]
            set_name = class_info['set_name']

            if set_name not in by_set:
                by_set[set_name] = []

            course = self.courses[assignment.course_id]
            faculty = self.faculty[assignment.faculty_id]
            room = self.rooms[assignment.room_id]

            day_idx = assignment.time_slot // self.slots_per_day
            slot_in_day = assignment.time_slot % self.slots_per_day
            start_hour = self._slot_to_hour(slot_in_day)
            end_hour = start_hour + assignment.duration

            # Calculate load contribution
            if assignment.meeting_type == 'lecture':
                load_units = assignment.duration
            else:
                load_units = assignment.duration / 3.0

            by_set[set_name].append({
                "course_id": assignment.course_id,
                "course_name": course['course_code'],
                "type": assignment.meeting_type.capitalize(),
                "day": days[day_idx],
                "start_hour": start_hour,
                "end_hour": end_hour,
                "room_id": assignment.room_id,
                "room_name": room['room_name'],
                "faculty_id": assignment.faculty_id,
                "faculty_name": faculty['name'],
                "faculty_institute_id": faculty.get('institute_id'),
                "set": set_name,
                "program_id": class_info['program_id'],
                "institute_id": faculty.get('institute_id')
            })

        # Calculate faculty load summary
        faculty_loads = {}
        for assignment in chromosome.assignments:
            fid = assignment.faculty_id
            load = self._calculate_faculty_load(fid, [assignment])
            faculty_loads[fid] = faculty_loads.get(fid, 0.0) + load

        # Format output for each set
        for set_name, schedule in by_set.items():
            # Sort by day and time
            schedule.sort(key=lambda x: (
                days.index(x['day']), x['start_hour']))

            schedule_data[set_name] = {
                "best_schedule": schedule,
                "total_courses": len(schedule),
                "faculty_units": {fid: round(load, 2) for fid, load in faculty_loads.items()}
            }

        return schedule_data

# Helper function to fetch table data


def fetch_table_data(table):
    """Fetch all data from a table and return as list of dicts"""
    try:
        with engine.connect() as conn:
            result = conn.execute(select(table))
            return [dict(row._mapping) for row in result]
    except Exception as e:
        print(f"Failed to load {table.name}:", e)
        return []


# Example usage
if __name__ == "__main__":
    # Load your data from database
    rooms_table = Table("rooms", metadata, autoload_with=engine)
    faculty_table = Table("faculty", metadata, autoload_with=engine)
    faculty_expertise_table = Table(
        "faculty_expertise", metadata, autoload_with=engine)
    courses_table = Table("course_view", metadata, autoload_with=engine)
    classes_table = Table("classes", metadata, autoload_with=engine)
    program_year_courses_table = Table(
        "program_year_course_view", metadata, autoload_with=engine)

    rooms = fetch_table_data(rooms_table)
    faculty = fetch_table_data(faculty_table)
    faculty_expertise = fetch_table_data(faculty_expertise_table)
    courses = fetch_table_data(courses_table)
    classes = fetch_table_data(classes_table)
    program_year_courses = fetch_table_data(program_year_courses_table)

    # rooms = [
    #     {"room_id": 2, "institute_id": 2, "room_capacity": 213213, "room_type": "Laboratory", "room_name": "Lab-1"},
    #     {"room_id": 3, "institute_id": 2, "room_capacity": 45, "room_type": "Lecture", "room_name": "Room-301"},
    #     {"room_id": 4, "institute_id": 2, "room_capacity": 41, "room_type": "Lecture", "room_name": "IC-1"}
    # ]

    # faculty = [
    #     {"faculty_id": 2, "user_accounts_id": 2, "name": "Sigfred Navasquez", "institute_id": 2, "program_id": 31},
    #     {"faculty_id": 11, "user_accounts_id": 11, "name": "Maria Flora", "institute_id": 2, "program_id": 31},
    #     {"faculty_id": 15, "user_accounts_id": 15, "name": "IT1 Faculty", "institute_id": 2, "program_id": 31}
    # ]

    # faculty_expertise = [
    #     {"faculty_id": 2, "course_id": 11},
    #     {"faculty_id": 2, "course_id": 13},
    #     {"faculty_id": 2, "course_id": 9},
    #     {"faculty_id": 11, "course_id": 9},
    #     {"faculty_id": 11, "course_id": 11},
    #     {"faculty_id": 11, "course_id": 13},
    #     {"faculty_id": 15, "course_id": 9},
    #     {"faculty_id": 15, "course_id": 13}
    # ]

    # courses = [
    #     {"course_id": 9, "program_id": 31, "course_code": "IT 111", "course_lecture": 3, "course_laboratory": 1},
    #     {"course_id": 11, "program_id": 31, "course_code": "IT 112", "course_lecture": 2, "course_laboratory": 1},
    #     {"course_id": 13, "program_id": 31, "course_code": "NSTP1", "course_lecture": 3, "course_laboratory": 0},
    #     {"course_id": 15, "program_id": 31, "course_code": "SS 111", "course_lecture": 3, "course_laboratory": 0},
    #     {"course_id": 16, "program_id": 31, "course_code": "SS 112", "course_lecture": 3, "course_laboratory": 0}
    # ]

    # classes = [
    #     {"class_id": 14, "school_year_id": 1, "program_id": 31, "set_name": "1st Year - A", "class_size": 34},
    #     {"class_id": 18, "school_year_id": 1, "program_id": 31, "set_name": "1st Year - B", "class_size": 35}
    # ]

    # program_year_courses = [
    #     {"id": 18, "program_id": 31, "course_id": 9, "year_level": 1, "school_year_id": 1},
    #     {"id": 19, "program_id": 31, "course_id": 13, "year_level": 1, "school_year_id": 1}
    # ]

    # Run GA
    ga = FacultyLoadingGA(rooms, faculty, faculty_expertise,
                          courses, classes, program_year_courses)
    best_schedule = ga.evolve()

    # Print human-readable schedule
    print("\n")
    print(ga.format_schedule(best_schedule))

    # Print JSON for backend (with special markers for parsing)
    print("\n")
    print("===JSON_START===")
    json_output = ga.to_json(best_schedule)
    print(json.dumps(json_output, indent=2))
    print("===JSON_END===")
