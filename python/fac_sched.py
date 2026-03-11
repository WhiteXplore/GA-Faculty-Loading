"""
Faculty Loading Scheduler
Generates a schedule for lectures and laboratories given rooms, faculty, expertise, courses, classes,
and program-year-course offerings.

Key rules implemented (as requested):
- Use only faculty listed in faculty_expertise for a course; pick the eligible faculty with the lowest projected load.
- Lecture hours count as 1.0 load per hour; Laboratory hours count as 1/3 load per hour. Max load = 18 units.
- Rooms must match room_type, capacity >= class_size, and be free for the entire block.
- Time window: Monday-Friday, 8:00..21:00 (we model hour slots 8..20 inclusive start, each slot = 1 hour).
- No overnight or multi-day classes.
- If a meeting cannot be scheduled because of faculty/room/time conflicts or load limits, it is recorded as unscheduled.

This script is written to be efficient on larger datasets: it uses integer bitmasks for availability across days/hours
and greedy assignment to the earliest-fit time slot. It also attempts to pack lab hours into contiguous blocks
when possible (labs are often scheduled as multi-hour blocks), while lectures are distributed into 1-hour sessions.

Output: list of scheduled meetings and unscheduled meetings; can be exported to JSON.

Run: python faculty_scheduler.py
"""
from typing import List, Dict, Tuple, Optional
import json
import math
from dataclasses import dataclass
from copy import deepcopy
from sqlalchemy import create_engine, Table, MetaData, select
import random
import os
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

# Constants
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
DAY_COUNT = len(DAYS)
START_HOUR = 8
END_HOUR = 21  # classes run up to 9 PM (21:00); last slot start is 20:00 if duration=1
SLOT_COUNT = END_HOUR - START_HOUR  # number of hourly slots per day (13)
MAX_FACULTY_LOAD = 18.0

# Helpers for bitmask availability: we'll represent a single day's availability as an integer with SLOT_COUNT bits
# bit i (0-indexed) corresponds to hour START_HOUR + i being occupied (1) or free (0). For a week, keep a list of 5 ints.


def init_week_availability(free: bool = True) -> List[int]:
    return [0 if not free else 0 for _ in range(DAY_COUNT)]


def block_mask(start_slot: int, duration: int) -> int:
    """Return bitmask for a contiguous block starting at start_slot (0-indexed within day) of duration hours."""
    return ((1 << duration) - 1) << start_slot


def is_block_free(day_mask: int, start_slot: int, duration: int) -> bool:
    mask = block_mask(start_slot, duration)
    return (day_mask & mask) == 0


def occupy_block(day_mask: int, start_slot: int, duration: int) -> int:
    return day_mask | block_mask(start_slot, duration)


# Scheduler implementation
class Scheduler:
    def __init__(self, rooms: List[Dict], faculty: List[Dict], faculty_expertise: List[Dict],
                 courses: List[Dict], classes: List[Dict], program_year_courses: List[Dict], other_schedule: List[Dict] = None):
        self.rooms = {r['room_id']: dict(r) for r in rooms}
        self.faculty = {f['faculty_id']: dict(f) for f in faculty}
        self.courses = {c['course_id']: dict(c) for c in courses}
        self.classes = {cl['class_id']: dict(cl) for cl in classes}
        self.program_year = list(program_year_courses)
        self.faculty_expertise_map = self._build_expertise_map(faculty_expertise)

        # availability: room_id -> list of 5 day masks; faculty_id -> list of 5 day masks
        self.room_availability: Dict[int, List[int]] = {rid: [0]*DAY_COUNT for rid in self.rooms}
        self.faculty_availability: Dict[int, List[int]] = {fid: [0]*DAY_COUNT for fid in self.faculty}

        # load in units
        self.faculty_load: Dict[int, float] = {fid: 0.0 for fid in self.faculty}

        # apply other_schedule to block out rooms and faculty if provided
        self.other_schedule = other_schedule or []
        self._apply_other_schedule()

        self.scheduled: List[Dict] = []
        self.unscheduled: List[Dict] = []

    def _build_expertise_map(self, expertise_list: List[Dict]) -> Dict[int, List[int]]:
        m = {}
        for e in expertise_list:
            m.setdefault(e['course_id'], []).append(e['faculty_id'])
        return m

    def _apply_other_schedule(self):
        # other_schedule items expected to have: type: 'room' or 'faculty', id, day (0-4), start_hour, duration
        for ev in self.other_schedule:
            typ = ev.get('type')
            day = ev['day']
            start = ev['start_hour'] - START_HOUR
            dur = ev['duration']
            if start < 0 or start + dur > SLOT_COUNT:
                continue
            if typ == 'room' and ev.get('id') in self.room_availability:
                rid = ev['id']
                self.room_availability[rid][day] = occupy_block(self.room_availability[rid][day], start, dur)
            if typ == 'faculty' and ev.get('id') in self.faculty_availability:
                fid = ev['id']
                self.faculty_availability[fid][day] = occupy_block(self.faculty_availability[fid][day], start, dur)

    # Utility: compute projected load increase for a meeting
    @staticmethod
    def meeting_load(is_lab: bool, hours: int) -> float:
        return (1.0/3.0) * hours if is_lab else 1.0 * hours

    def eligible_faculty_for_course(self, course_id: int) -> List[int]:
        return self.faculty_expertise_map.get(course_id, [])

    def find_room(self, room_type: str, class_size: int, day: int, start_slot: int, duration: int) -> Optional[int]:
        # iterate rooms (optimize by preferring smallest capacity that fits to leave large rooms free)
        candidates = [r for r in self.rooms.values() if r['room_type'].lower() == room_type.lower() and r['room_capacity'] >= class_size]
        candidates.sort(key=lambda x: x['room_capacity'])
        for r in candidates:
            rid = r['room_id']
            if is_block_free(self.room_availability[rid][day], start_slot, duration):
                return rid
        return None

    def select_faculty(self, course_id: int, required_load_inc: float, day: int, start_slot: int, duration: int) -> Optional[int]:
        elig = self.eligible_faculty_for_course(course_id)
        # filter by availability and load
        valid = []
        for fid in elig:
            if fid not in self.faculty:
                continue
            if self.faculty_load[fid] + required_load_inc > MAX_FACULTY_LOAD:
                continue
            if is_block_free(self.faculty_availability[fid][day], start_slot, duration):
                valid.append(fid)
        if not valid:
            return None
        # choose faculty with lowest projected load (tie-breaker: faculty_id)
        valid.sort(key=lambda f: (self.faculty_load.get(f, 0.0), f))
        return valid[0]

    def reserve(self, rid: int, fid: int, day: int, start_slot: int, duration: int):
        self.room_availability[rid][day] = occupy_block(self.room_availability[rid][day], start_slot, duration)
        self.faculty_availability[fid][day] = occupy_block(self.faculty_availability[fid][day], start_slot, duration)

    def schedule_all(self):
        # For each program_year_course and each class in the matching program, create lecture and lab meetings
        for py in self.program_year:
            course_id = py['course_id']
            program_id = py['program_id']
            year_level = py.get('year_level')
            # find classes that belong to this program & school_year
            relevant_classes = [cl for cl in self.classes.values() if cl['program_id'] == program_id]
            course = self.courses.get(course_id)
            if not course:
                continue
            lec_hours = int(course.get('course_lecture', 0))
            lab_hours = int(course.get('course_laboratory', 0))

            for cl in relevant_classes:
                # schedule lectures (split into 1-hour sessions across the week)
                for _ in range(lec_hours):
                    scheduled = self._schedule_session(course_id=course_id, class_info=cl,
                                                       duration=1, is_lab=False)
                    if not scheduled:
                        self.unscheduled.append({
                            'type': 'lecture', 'course_id': course_id, 'class_id': cl['class_id'], 'reason': 'no slot/faculty/room'
                        })
                # schedule labs (try to pack into contiguous block if duration > 1)
                if lab_hours > 0:
                    # try to schedule lab as one contiguous block when possible
                    scheduled = self._schedule_session(course_id=course_id, class_info=cl,
                                                       duration=lab_hours, is_lab=True)
                    if not scheduled:
                        # fall back to splitting into 1-hour lab sessions (still must use expert faculty)
                        for _ in range(lab_hours):
                            scheduled2 = self._schedule_session(course_id=course_id, class_info=cl,
                                                                duration=1, is_lab=True)
                            if not scheduled2:
                                self.unscheduled.append({
                                    'type': 'lab', 'course_id': course_id, 'class_id': cl['class_id'], 'reason': 'no slot/faculty/room'
                                })
        return self.scheduled, self.unscheduled

    def _schedule_session(self, course_id: int, class_info: Dict, duration: int, is_lab: bool) -> bool:
        # Greedy earliest-fit: iterate days and start slots, try to find a room and eligible faculty
        class_size = class_info['class_size']
        room_type = 'Laboratory' if is_lab else 'Lecture'
        load_inc = self.meeting_load(is_lab, duration)

        # We will attempt to fit the block in any day with start_slot range [0 .. SLOT_COUNT-duration]
        for day in range(DAY_COUNT):
            for start_slot in range(0, SLOT_COUNT - duration + 1):
                # time constraints: no overnight or multi-day — satisfied by block within same day
                # find room that is free for entire block
                rid = self.find_room(room_type, class_size, day, start_slot, duration)
                if rid is None:
                    continue
                # find faculty
                fid = self.select_faculty(course_id, load_inc, day, start_slot, duration)
                if fid is None:
                    continue
                # reserve and record
                self.reserve(rid, fid, day, start_slot, duration)
                self.faculty_load[fid] += load_inc
                meeting = {
                    'course_id': course_id,
                    'class_id': class_info['class_id'],
                    'room_id': rid,
                    'faculty_id': fid,
                    'day': day,
                    'start_hour': START_HOUR + start_slot,
                    'duration': duration,
                    'is_lab': is_lab,
                    'load_increment': load_inc
                }
                self.scheduled.append(meeting)
                return True
        return False


def fetch_table_data(table: Table) -> List[Dict]:
    """Fetch all rows from a SQLAlchemy table and return as list of dicts."""
    with engine.connect() as conn:
        result = conn.execute(select(table))
        rows = result.fetchall()
        # Convert rows to list of dicts
        return [dict(row._mapping) for row in rows]


# ----------------- Example usage with provided sample inputs -----------------
if __name__ == '__main__':
    # sample (commented out in original user input) datasets
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
    # optional existing schedule to block resources (empty here)
    other_schedule = []

    scheduler = Scheduler(rooms=rooms, faculty=faculty, faculty_expertise=faculty_expertise,
                          courses=courses, classes=classes, program_year_courses=program_year_courses,
                          other_schedule=other_schedule)

    scheduled, unscheduled = scheduler.schedule_all()

    print("Scheduled meetings:")
    print(json.dumps(scheduled, indent=2))
    print("\nUnscheduled meetings:")
    print(json.dumps(unscheduled, indent=2))

    # Save to JSON files
    with open('scheduled.json', 'w') as f:
        json.dump(scheduled, f, indent=2)
    with open('unscheduled.json', 'w') as f:
        json.dump(unscheduled, f, indent=2)

    print('\nSaved scheduled.json and unscheduled.json')
