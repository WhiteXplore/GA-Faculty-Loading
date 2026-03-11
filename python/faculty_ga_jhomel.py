#!/usr/bin/env python3
"""
No Schedule Conflict - Fixed Schedule with Faculty Load Limit
Faculty capped at 18 units (lecture hours count as hours, lab as 1/3 per hour).

MEETING SCHEDULE:
 - Each course meets TWICE per week maximum:
   1. Once for ALL lecture hours (one contiguous block)
   2. Once for ALL laboratory hours (one contiguous block)
 - Example: 3-hour lecture + 3-hour lab = 2 meetings per week

DYNAMIC HOUR ALLOCATION:
 - Lecture hours: course_lecture field (1 unit = 1 hour)
 - Laboratory hours: course_laboratory field (1 unit = 3 hours)
 - Example: course_lecture=3, course_laboratory=1 → 3-hour lecture block + 3-hour lab block
 
FACULTY EXPERTISE SYSTEM:
 - All assignments (lecture or lab) only consider faculty listed in faculty_expertise for that course.
 - When multiple eligible faculty exist, the algorithm picks the one with the LOWEST projected load (ties broken randomly).
 - No fallback to non-expert faculty.
 
LOAD CALCULATION:
 - Lecture: Each hour counts as 1 unit toward faculty load
 - Laboratory: Each hour counts as 1/3 unit toward faculty load
 - Maximum faculty load: 18 units
 
Requirements: sqlalchemy, pymysql
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import random
from copy import deepcopy
import json
from sqlalchemy import create_engine, Table, MetaData, select

# =========================
# MySQL Connection (adjust creds/host/db as needed)
# =========================
DB_USER = "root"
DB_PASS = "admin12345.."
DB_HOST = "127.0.0.2"
DB_PORT = 3306
DB_NAME = "dnsc_class_scheduler"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
    echo=False,
)
metadata = MetaData()

# =========================
# CONFIGURATION
# =========================
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
# integer hour markers (12 => lunchtime gap)
TIME_SLOTS = [8, 9, 10, 11, 13, 14, 15, 16, 17]
POPULATION_SIZE = 50
GENERATIONS = 200
MUTATION_RATE = 0.12
MAX_ATTEMPTS_PER_HOUR = 500
FACULTY_MAX_UNITS = 18

# =========================
# LOAD TABLES / VIEWS
# =========================
programs_table = Table("programs", metadata, autoload_with=engine)
faculty_table = Table("faculty", metadata, autoload_with=engine)
faculty_expertise_table = Table(
    "faculty_expertise", metadata, autoload_with=engine)
courses_table = Table("course_view", metadata, autoload_with=engine)
assigned_set_courses_table = Table(
    "assigned_set_courses", metadata, autoload_with=engine)
rooms_table = Table("rooms", metadata, autoload_with=engine)
classes_table = Table(
    "classes", metadata, autoload_with=engine)
program_year_courses_table = Table(
    "program_year_courses", metadata, autoload_with=engine)


def fetch_table_data(table):
    try:
        with engine.connect() as conn:
            return [dict(row._mapping) for row in conn.execute(select(table))]
    except Exception as e:
        print(f"Failed to load {table.name}:", e)
        return []


programs = fetch_table_data(programs_table)
faculty = fetch_table_data(faculty_table)
faculty_expertise = fetch_table_data(faculty_expertise_table)
courses = fetch_table_data(courses_table)
assigned_set_courses = fetch_table_data(assigned_set_courses_table)
rooms = fetch_table_data(rooms_table)
classes = fetch_table_data(classes_table)
program_year_courses = fetch_table_data(program_year_courses_table)

# =========================
# HELPER FUNCTIONS
# =========================


def faculty_load_summary(schedule):
    """
    Returns dict: {faculty_id: total_units}
    """
    load = calculate_faculty_load(schedule)
    return {fid: round(units, 2) for fid, units in load.items()}


def calculate_faculty_load(schedule):
    """
    Calculate faculty load in units:
      - Lecture blocks: add (end_hour - start_hour) hours
      - Laboratory 1-hour block: add 1/3 unit (per 1-hour lab block)
    """
    load = {}
    for blk in schedule:
        fid = blk.get("faculty_id")
        if not fid:
            continue
        if blk.get("type") == "Lecture":
            hours = max(0, blk.get("end_hour", blk.get(
                "start_hour", 0)) - blk.get("start_hour", 0))
            load[fid] = load.get(fid, 0) + hours
        elif blk.get("type") == "Laboratory":
            # labs are stored as 1-hour blocks; each lab hour counts as 1/3
            load[fid] = load.get(fid, 0) + (1 / 3)
    return load


def check_availability(schedule, day, start_hour, end_hour, faculty_id=None, room_id=None, other_schedule=None):
    """
    Check if faculty or room is free between start_hour and end_hour on given day.
    Overlap detection: two blocks overlap if not (A.end <= B.start or A.start >= B.end).
    """
    if other_schedule is None:
        other_schedule = []
    for block in (schedule or []) + (other_schedule or []):
        if block.get("day") != day:
            continue
        b_start = block.get("start_hour")
        b_end = block.get("end_hour")
        if b_start is None or b_end is None:
            continue
        # check overlap
        if not (end_hour <= b_start or start_hour >= b_end):
            if faculty_id is not None and block.get("faculty_id") == faculty_id:
                return False
            if room_id is not None and block.get("room_id") == room_id:
                return False
    return True


def get_courses_for_set(set_name):
    course_ids = [a["course_id"]
                  for a in assigned_set_courses if a.get("set") == set_name]
    return [c for c in courses if c.get("course_id") in course_ids]


def faculty_ids_for_course(course_id):
    """
    Return faculty IDs from faculty_expertise for this course only.
    This ensures we *only* consider expert faculty.
    """
    return [ue["faculty_id"] for ue in faculty_expertise if ue.get("course_id") == course_id]


def pick_conflict_free_faculty(schedule, day, start_hour, end_hour, eligible_faculty_ids, other_schedule=None, faculty_load=None, block_type="Lecture"):
    """
    From eligible_faculty_ids (which come from faculty_expertise), pick one that:
      - Is free for the entire block (schedule + other_schedule)
      - Projected load (with this block) <= FACULTY_MAX_UNITS
    Selection strategy:
      - Compute projected loads and choose faculty with the lowest projected load.
      - Tie-breaker: random.choice among lowest-load faculty.
    Returns faculty_id or None.
    """
    if not eligible_faculty_ids:
        return None
    if faculty_load is None:
        faculty_load = calculate_faculty_load(
            (schedule or []) + (other_schedule or []))

    free_candidates = []
    # block contribution for load (lecture: hours, lab: 1/3 per 1-hour block)
    block_contrib = None
    if block_type == "Lecture":
        block_contrib = end_hour - start_hour
    else:
        # for Laboratory each 1-hour slot counts as 1/3
        block_contrib = 1/3

    for fid in eligible_faculty_ids:
        # strictly only consider faculty listed as eligible (from faculty_expertise)
        if not check_availability(schedule, day, start_hour, end_hour, fid, None, other_schedule):
            continue
        projected = faculty_load.get(fid, 0) + block_contrib
        if projected <= FACULTY_MAX_UNITS:
            free_candidates.append((fid, projected))

    if not free_candidates:
        return None

    # pick faculty with minimum projected load; if multiple, random among them
    min_load = min(p for (_, p) in free_candidates)
    lowest = [fid for (fid, p) in free_candidates if p == min_load]
    return random.choice(lowest)


def pick_conflict_free_room(schedule, day, start_hour, end_hour, course_type, program_id, other_schedule=None):
    """
    Prefer rooms with same institute as program; fallback to any room of correct type.
    """
    program_institute_id = None
    if program_id is not None:
        program_institute_id = next((p.get("institute_id") for p in programs if p.get(
            "program_id") == program_id), None)

    primary_rooms = [
        r for r in rooms
        if r.get("room_type") == course_type
        and r.get("institute_id") == program_institute_id
        and check_availability(schedule, day, start_hour, end_hour, None, r["room_id"], other_schedule)
    ]
    if primary_rooms:
        return random.choice(primary_rooms)["room_id"]

    fallback_rooms = [
        r for r in rooms
        if r.get("room_type") == course_type
        and check_availability(schedule, day, start_hour, end_hour, None, r["room_id"], other_schedule)
    ]
    return random.choice(fallback_rooms)["room_id"] if fallback_rooms else None


# =========================
# BLOCK PLACEMENT (no globals) - return True if placed and update schedule/faculty_load
# =========================
def place_lecture_block(schedule, existing_schedule, faculty_load, set_name, course, lec_hours, assigned_faculty_id=None):
    """
    Try to place lec_hours consecutively on a single day.
    Updates schedule list and faculty_load dict in-place when successful.
    """
    if lec_hours <= 0:
        return True
    eligible_faculty = faculty_ids_for_course(course.get("course_id"))
    # if assigned_faculty_id is provided we must still ensure they are in expertise list
    if assigned_faculty_id:
        if assigned_faculty_id not in eligible_faculty:
            # assigned faculty isn't an expert -> do not use them
            assigned_faculty_id = None
        else:
            eligible_faculty = [assigned_faculty_id]

    if not eligible_faculty:
        return False

    attempts = 0
    while attempts < MAX_ATTEMPTS_PER_HOUR:
        attempts += 1
        day = random.choice(DAYS)
        start_hour = random.choice(TIME_SLOTS)
        end_hour = start_hour + lec_hours

        # ensure the block uses contiguous TIME_SLOTS (no lunch gap inside block)
        block_hours = list(range(start_hour, end_hour))
        if not all(h in TIME_SLOTS for h in block_hours):
            continue

        # check availability & load
        faculty_id = pick_conflict_free_faculty(
            schedule, day, start_hour, end_hour, eligible_faculty, existing_schedule, faculty_load, "Lecture")
        room_id = pick_conflict_free_room(
            schedule, day, start_hour, end_hour, "Lecture", course.get("program_id"), existing_schedule)

        if faculty_id and room_id:
            schedule.append({
                "course_id": course.get("course_id"),
                "course_name": course.get("course_code", course.get("course_name", "Unknown")),
                "type": "Lecture",
                "day": day,
                "start_hour": start_hour,
                "end_hour": end_hour,
                "faculty_id": faculty_id,
                "room_id": room_id,
                "set": set_name,
                "program_id": course.get("program_id"),
            })
            # update faculty_load
            faculty_load[faculty_id] = faculty_load.get(
                faculty_id, 0) + lec_hours
            return True
    return False


def place_single_hour(schedule, existing_schedule, faculty_load, set_name, course, slot_type, assigned_faculty_id=None):
    """
    Place a single 1-hour block. Used as fallback if contiguous blocks cannot be placed.
    Updates schedule and faculty_load on success.
    """
    eligible_faculty = faculty_ids_for_course(course.get("course_id"))
    if assigned_faculty_id:
        if assigned_faculty_id not in eligible_faculty:
            assigned_faculty_id = None
        else:
            eligible_faculty = [assigned_faculty_id]

    if not eligible_faculty:
        return False

    attempts = 0
    while attempts < MAX_ATTEMPTS_PER_HOUR:
        attempts += 1
        day = random.choice(DAYS)
        start_hour = random.choice(TIME_SLOTS)
        end_hour = start_hour + 1

        faculty_id = pick_conflict_free_faculty(
            schedule, day, start_hour, end_hour, eligible_faculty, existing_schedule, faculty_load, slot_type)
        room_id = pick_conflict_free_room(
            schedule, day, start_hour, end_hour, slot_type, course.get("program_id"), existing_schedule)

        if faculty_id and room_id:
            schedule.append({
                "course_id": course.get("course_id"),
                "course_name": course.get("course_code", course.get("course_name", "Unknown")),
                "type": slot_type,
                "day": day,
                "start_hour": start_hour,
                "end_hour": end_hour,
                "faculty_id": faculty_id,
                "room_id": room_id,
                "set": set_name,
                "program_id": course.get("program_id"),
            })
            # update faculty_load (1/3 per lab hour; for 1-hour lecture fallback add 1)
            if slot_type == "Lecture":
                faculty_load[faculty_id] = faculty_load.get(faculty_id, 0) + 1
            else:
                faculty_load[faculty_id] = faculty_load.get(
                    faculty_id, 0) + (1 / 3)
            return True
    return False


def place_laboratory_block(schedule, existing_schedule, faculty_load, set_name, course, lab_hours, assigned_faculty_id=None):
    """
    Try to place lab_hours consecutively on a single day.
    Updates schedule list and faculty_load dict in-place when successful.
    Lab hours count as 1/3 unit per hour for faculty load.
    """
    if lab_hours <= 0:
        return True
    eligible_faculty = faculty_ids_for_course(course.get("course_id"))
    # if assigned_faculty_id is provided we must still ensure they are in expertise list
    if assigned_faculty_id:
        if assigned_faculty_id not in eligible_faculty:
            # assigned faculty isn't an expert -> do not use them
            assigned_faculty_id = None
        else:
            eligible_faculty = [assigned_faculty_id]

    if not eligible_faculty:
        return False

    attempts = 0
    while attempts < MAX_ATTEMPTS_PER_HOUR:
        attempts += 1
        day = random.choice(DAYS)
        start_hour = random.choice(TIME_SLOTS)
        end_hour = start_hour + lab_hours

        # ensure the block uses contiguous TIME_SLOTS (no lunch gap inside block)
        block_hours = list(range(start_hour, end_hour))
        if not all(h in TIME_SLOTS for h in block_hours):
            continue

        # check availability & load
        faculty_id = pick_conflict_free_faculty(
            schedule, day, start_hour, end_hour, eligible_faculty, existing_schedule, faculty_load, "Laboratory")
        room_id = pick_conflict_free_room(
            schedule, day, start_hour, end_hour, "Laboratory", course.get("program_id"), existing_schedule)

        if faculty_id and room_id:
            schedule.append({
                "course_id": course.get("course_id"),
                "course_name": course.get("course_code", course.get("course_name", "Unknown")),
                "type": "Laboratory",
                "day": day,
                "start_hour": start_hour,
                "end_hour": end_hour,
                "faculty_id": faculty_id,
                "room_id": room_id,
                "set": set_name,
                "program_id": course.get("program_id"),
            })
            # update faculty_load: lab hours count as 1/3 unit per hour
            lab_units = lab_hours / 3
            faculty_load[faculty_id] = faculty_load.get(
                faculty_id, 0) + lab_units
            return True
    return False


# =========================
# INDIVIDUAL CREATION
# =========================
def create_individual(set_name, existing_schedule=None):
    """
    Create a schedule individual for GA for one 'set'.
    Returns a list of blocks.

    Important: assigned faculty for each course is chosen from faculty_expertise
    and selected by lowest current load to prioritize expertise.
    """
    if existing_schedule is None:
        existing_schedule = []

    schedule = []
    faculty_load = calculate_faculty_load(existing_schedule)
    courses_to_schedule = get_courses_for_set(set_name)

    for course in courses_to_schedule:
        # Get lecture and lab values from course_view fields
        lec_hours = int(course.get("course_lecture", 0))
        # labs stored as units: multiply by 3 to get hours (1 lab unit = 3 hours)
        lab_hours = int(course.get("course_laboratory", 0)) * 3
        eligible_faculty = faculty_ids_for_course(course.get("course_id"))
        if not eligible_faculty:
            # skip courses with no eligible faculty
            continue

        # SELECT assigned_faculty_id by lowest current load among eligible experts
        # (tie-break random)
        loads = [(fid, faculty_load.get(fid, 0)) for fid in eligible_faculty]
        min_load = min(l for (_, l) in loads)
        ties = [fid for (fid, l) in loads if l == min_load]
        assigned_faculty_id = random.choice(ties)

        # Place lecture as one contiguous block if possible
        if lec_hours > 0:
            placed = place_lecture_block(
                schedule, existing_schedule, faculty_load, set_name, course, lec_hours, assigned_faculty_id)
            # if we couldn't place the contiguous lecture block, attempt to place lec_hours as single hours (fallback)
            if not placed:
                for _ in range(lec_hours):
                    ok = place_single_hour(
                        schedule, existing_schedule, faculty_load, set_name, course, "Lecture", assigned_faculty_id)
                    if not ok:
                        break

        # Place laboratory as one contiguous block
        if lab_hours > 0:
            placed = place_laboratory_block(
                schedule, existing_schedule, faculty_load, set_name, course, lab_hours, assigned_faculty_id)
            # if we couldn't place the contiguous laboratory block, skip it (no fallback to maintain twice-per-week meeting)
            # You could add fallback to single hours if needed, but this maintains the strict "meet twice" requirement

    # sort for determinism
    schedule.sort(key=lambda x: (DAYS.index(
        x["day"]), x["start_hour"], x["course_id"]))
    return schedule


# =========================
# FITNESS / GA OPERATIONS
# =========================
def fitness(schedule, existing_schedule=None):
    """
    Fitness with strong penalty for conflicts and overloads.
    Higher is better.
    """
    if existing_schedule is None:
        existing_schedule = []
    score = 0
    seen = []

    # penalize conflicts between blocks in schedule and with existing_schedule
    for a in schedule:
        conflict = False
        for b in seen:
            if a.get("day") == b.get("day") and not (a.get("end_hour") <= b.get("start_hour") or a.get("start_hour") >= b.get("end_hour")):
                if a.get("faculty_id") == b.get("faculty_id") or a.get("room_id") == b.get("room_id"):
                    conflict = True
                    break
        if not conflict and existing_schedule:
            for b in existing_schedule:
                if a.get("day") == b.get("day") and not (a.get("end_hour") <= b.get("start_hour") or a.get("start_hour") >= b.get("end_hour")):
                    if a.get("faculty_id") == b.get("faculty_id") or a.get("room_id") == b.get("room_id"):
                        conflict = True
                        break
        score += -10 if conflict else 1
        seen.append(a)

    # penalize overloads
    faculty_load = calculate_faculty_load(schedule + (existing_schedule or []))
    for fid, units in faculty_load.items():
        if units > FACULTY_MAX_UNITS:
            score -= (units - FACULTY_MAX_UNITS) * 5

    # slight reward for larger schedules (more scheduled blocks)
    score += 0.01 * len(schedule)
    return score


def mutate(individual, existing_schedule=None):
    """
    Mutate by moving a block (keeping its duration), trying to reassign faculty/room.
    Faculty reassignment only picks from experts for that course.
    """
    if existing_schedule is None:
        existing_schedule = []
    for i, block in enumerate(individual):
        if random.random() < MUTATION_RATE:
            attempts = 0
            while attempts < 60:
                attempts += 1
                day = random.choice(DAYS)
                duration = block.get("end_hour") - block.get("start_hour")
                start_hour = random.choice(TIME_SLOTS)
                end_hour = start_hour + duration

                # ensure block fits TIME_SLOTS
                if not all(h in TIME_SLOTS for h in range(start_hour, end_hour)):
                    continue

                faculty_load = calculate_faculty_load(
                    individual + (existing_schedule or []))
                eligible_faculty = faculty_ids_for_course(
                    block.get("course_id"))
                faculty_id = pick_conflict_free_faculty(
                    individual, day, start_hour, end_hour, eligible_faculty, existing_schedule, faculty_load, block.get("type"))
                course_program_id = next((c.get("program_id") for c in courses if c.get(
                    "course_id") == block.get("course_id")), None)
                room_id = pick_conflict_free_room(individual, day, start_hour, end_hour, block.get(
                    "type"), course_program_id, existing_schedule)
                if faculty_id and room_id:
                    # apply mutation
                    individual[i] = {
                        "course_id": block.get("course_id"),
                        "course_name": block.get("course_name"),
                        "type": block.get("type"),
                        "day": day,
                        "start_hour": start_hour,
                        "end_hour": end_hour,
                        "faculty_id": faculty_id,
                        "room_id": room_id,
                        "set": block.get("set"),
                        "program_id": block.get("program_id"),
                    }
                    break
    return individual


def crossover(parent1, parent2):
    """
    Simple crossover: splice at a random point; remove duplicate identical blocks.
    """
    if not parent1 or not parent2:
        return deepcopy(parent1 if parent1 else parent2)
    p1 = deepcopy(parent1)
    p2 = deepcopy(parent2)
    point = random.randint(0, min(len(p1), len(p2)))
    child = p1[:point] + p2[point:]
    unique, seen = [], set()
    for b in child:
        key = (b.get("course_id"), b.get("type"), b.get("day"), b.get(
            "start_hour"), b.get("faculty_id"), b.get("room_id"))
        if key not in seen:
            unique.append(b)
            seen.add(key)
    return unique


def genetic_algorithm(set_name, existing_schedule=None):
    """
    Run GA to produce best individual for given set_name considering existing_schedule.
    """
    population = [create_individual(set_name, existing_schedule)
                  for _ in range(POPULATION_SIZE)]
    for _ in range(GENERATIONS):
        population = sorted(population, key=lambda ind: fitness(
            ind, existing_schedule), reverse=True)
        keep = max(2, POPULATION_SIZE // 10)
        next_gen = population[:keep]
        while len(next_gen) < POPULATION_SIZE:
            p1, p2 = random.sample(
                population[:max(2, POPULATION_SIZE // 2)], 2)
            child = crossover(p1, p2)
            child = mutate(child, existing_schedule)
            next_gen.append(child)
        population = next_gen
    return sorted(population, key=lambda ind: fitness(ind, existing_schedule), reverse=True)[0]


# =========================
# OUTPUT / UTIL
# =========================
def schedule_to_object(schedule, faculty_list, room_list):
    def resolve_faculty_name(f):
        if isinstance(f, dict):
            if f.get("name"):
                return f.get("name")
            return (f.get("first_name", "") + (" " + f.get("last_name") if f.get("last_name") else "")).strip()
        return f"Faculty {f}"

    faculty_map = {f.get("faculty_id"): resolve_faculty_name(f)
                   for f in faculty_list}
    faculty_institute_map = {f.get("faculty_id"): f.get(
        "institute_id") for f in faculty_list}
    room_map = {r.get("room_id"): r.get("room_name") for r in room_list}

    result = []  # <--- initialize here!

    for a in schedule:
        result.append({
            "course_id": a.get("course_id"),
            "course_name": a.get("course_name"),
            "type": a.get("type"),
            "day": a.get("day"),
            "start_hour": a.get("start_hour"),
            "end_hour": a.get("end_hour"),
            "room_id": a.get("room_id"),
            "room_name": room_map.get(a.get("room_id"), "Unknown"),
            "faculty_id": a.get("faculty_id"),
            "faculty_name": faculty_map.get(a.get("faculty_id"), "Unassigned"),
            "faculty_institute_id": faculty_institute_map.get(a.get("faculty_id")),
            "set": a.get("set", "A"),
            "program_id": a.get("program_id"),
            "institute_id": a.get("institute_id"),
        })

    result.sort(key=lambda x: (DAYS.index(
        x["day"]), x["start_hour"], x["course_id"]))

    # Compute faculty load for this schedule
    faculty_units = faculty_load_summary(schedule)

    return {
        "best_schedule": result,
        "total_courses": len(result),
        "faculty_units": faculty_units  # include total units per faculty
    }


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    random.seed()
    all_sets = sorted(set(a.get("set") for a in assigned_set_courses))
    all_schedules = {}
    accumulated_blocks = []  # blocks already placed (between sets)

    for s in all_sets:
        print(
            f"Generating schedule for set: {s} (considering {len(accumulated_blocks)} accumulated blocks)")
        best_schedule = genetic_algorithm(
            set_name=s, existing_schedule=accumulated_blocks)
        obj = schedule_to_object(best_schedule, faculty, rooms)
        all_schedules[s] = obj

        # add placed blocks to accumulated_blocks so next sets avoid conflicts
        for blk in best_schedule:
            accumulated_blocks.append({
                "course_id": blk.get("course_id"),
                "course_name": blk.get("course_name"),
                "type": blk.get("type"),
                "day": blk.get("day"),
                "start_hour": blk.get("start_hour"),
                "end_hour": blk.get("end_hour"),
                "faculty_id": blk.get("faculty_id"),
                "room_id": blk.get("room_id"),
                "set": blk.get("set", s),
                "program_id": blk.get("program_id"),
            })

    # print nicely
    print(json.dumps(all_schedules, indent=2))
    print("\nLoaded rooms data:")
    print(json.dumps(rooms, indent=2, default=str))
    print("\nLoaded programs data:")
    print(json.dumps(programs, indent=2, default=str))
    print("\nLoaded faculty data:")
    print(json.dumps(faculty, indent=2, default=str))
    print("\nLoaded faculty_expertise data:")
    print(json.dumps(faculty_expertise, indent=2, default=str))
    print("\nLoaded courses data:")
    print(json.dumps(courses, indent=2, default=str))
    print("\nLoaded assigned_set_courses data:")
    print(json.dumps(assigned_set_courses, indent=2, default=str))
    print("\nLoaded classes data:")
    print(json.dumps(classes, indent=2, default=str))
    print("\nLoaded program_year_courses data:")
    print(json.dumps(program_year_courses, indent=2, default=str))
