import random
import json
import os
import math
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from copy import deepcopy
from sqlalchemy import create_engine, Table, MetaData, select
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
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


# ===========================================================   =
# START CODE FOR SCHEDULING FUNCTIONS
# ============================================================

# ============================================================
# SCHEDULING FUNCTIONS
# ============================================================

# Time slot configuration
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
# Day patterns for weekly scheduling (Wednesday standalone is fallback only)
DAY_PATTERNS = {
    "TTH": ["Tuesday", "Thursday"],
    "MF": ["Monday", "Friday"],
    "MWF": ["Monday", "Wednesday", "Friday"]
}
START_HOUR = 7  # 7 AM
END_HOUR = 21   # 9 PM
PART_TIME_START_HOUR = 17  # 5 PM - Part-time faculty can only teach from 5 PM onwards
# 10 PM - Extended end time for part-time faculty to accommodate evening classes
PART_TIME_END_HOUR = 22
LUNCH_START = 12
LUNCH_END = 13
MAX_CAPACITY_EXCESS = 5  # Allow up to 5 students over capacity

# Unit to hour conversion constants (for scheduling contact hours)
LECTURE_UNIT_TO_HOUR = 1.0  # 1 student unit = 1 contact hour
LAB_UNIT_TO_HOUR = 3.0  # 1 student unit = 3 contact hours

# Faculty load calculation constants
# 1 student lec unit = 1 teacher unit
LECTURE_STUDENT_UNIT_TO_TEACHER_UNIT = 1.0
# 1 student lab unit = 3 hours × 0.75 = 2.25 teacher units
LAB_STUDENT_UNIT_TO_TEACHER_UNIT = 2.25

# Target percentage of total lecture HOURS that should be face-to-face
# Laboratory is always face-to-face and does NOT count toward this ratio
TARGET_FACE_TO_FACE_PERCENTAGE = 0.70  # 30% face-to-face


def get_balanced_patterns(day_pattern_tracker, weekly_hours):
    """
    Return day patterns sorted by usage (least used first) with randomization for ties.
    Only includes patterns where weekly_hours / len(pattern_days) >= 1 hour per meeting.
    This ensures fair distribution across TTH, MF, and MWF.

    Args:
        day_pattern_tracker: dict mapping pattern name to usage count, e.g. {"TTH": 3, "MF": 2, "MWF": 1}
        weekly_hours: total weekly contact hours for the class being scheduled

    Returns:
        List of tuples: (pattern_name, pattern_days_list), sorted by least-used first, ties randomized.
    """
    # Filter to valid patterns only (each meeting must be at least 1 hour)
    valid_patterns = []
    for pattern_name, pattern_days in DAY_PATTERNS.items():
        hours_per_meeting = weekly_hours / len(pattern_days)
        if hours_per_meeting >= 1.0:
            valid_patterns.append((pattern_name, pattern_days))

    # Build count groups for sorting
    patterns_with_counts = [
        (pattern_name, pattern_days, day_pattern_tracker.get(pattern_name, 0))
        for pattern_name, pattern_days in valid_patterns
    ]

    count_groups = {}
    for pattern_name, pattern_days, count in patterns_with_counts:
        if count not in count_groups:
            count_groups[count] = []
        count_groups[count].append((pattern_name, pattern_days))

    # Shuffle within each count group and build result
    result = []
    for count in sorted(count_groups.keys()):
        group = count_groups[count]
        random.shuffle(group)
        result.extend(group)

    return result


def get_randomized_time_slots(available_slots):
    """
    Return time slots in randomized order to spread schedules across different times.
    """
    slots_copy = list(available_slots)
    random.shuffle(slots_copy)
    return slots_copy


def generate_time_slots():
    """
    Generate all available time slots (excluding lunch break 12-1pm).
    Returns list of time slots as tuples (start_hour, end_hour).
    """
    slots = []
    for hour in range(START_HOUR, END_HOUR):
        # Skip lunch hour
        if hour >= LUNCH_START and hour < LUNCH_END:
            continue
        slots.append((hour, hour + 1))
    return slots


def time_to_string(hour):
    """Convert hour (24-hour format) to readable string."""
    if hour == 0:
        return "12:00 AM"
    elif hour < 12:
        return f"{hour}:00 AM"
    elif hour == 12:
        return "12:00 PM"
    else:
        return f"{hour - 12}:00 PM"


def format_time_slot(start_hour, duration):
    """Format time slot as string. Handles fractional hours."""
    end_hour = start_hour + duration

    def time_to_str(hour):
        """Convert hour (can be fractional) to readable string."""
        hour_int = int(hour)
        minutes = int((hour - hour_int) * 60)

        if hour_int == 0:
            time_str = "12"
            am_pm = "AM"
        elif hour_int < 12:
            time_str = str(hour_int)
            am_pm = "AM"
        elif hour_int == 12:
            time_str = "12"
            am_pm = "PM"
        else:
            time_str = str(hour_int - 12)
            am_pm = "PM"

        if minutes > 0:
            time_str += f":{minutes:02d}"
        else:
            time_str += ":00"

        return f"{time_str} {am_pm}"

    return f"{time_to_str(start_hour)} - {time_to_str(end_hour)}"


def check_time_overlap(time1_start, time1_duration, time2_start, time2_duration):
    """Check if two time blocks overlap."""
    time1_end = time1_start + time1_duration
    time2_end = time2_start + time2_duration

    return not (time1_end <= time2_start or time2_end <= time1_start)


def check_lunch_conflict(start_hour, duration):
    """Check if a time block conflicts with lunch break."""
    end_hour = start_hour + duration

    # Check if any part of the block overlaps with lunch (12-1pm)
    if start_hour < LUNCH_END and end_hour > LUNCH_START:
        return True
    return False


def is_valid_time_block(start_hour, duration):
    """Check if a time block is valid (within hours and doesn't cross lunch)."""
    end_hour = start_hour + duration

    # Check if within operating hours
    if start_hour < START_HOUR or end_hour > END_HOUR:
        return False

    # Check if crosses lunch break
    if check_lunch_conflict(start_hour, duration):
        return False

    return True


def find_available_slots(start_hour, end_hour, duration, exclude_lunch=True):
    """
    Find all possible starting times for a block of given duration.
    Returns list of valid start hours.
    """
    valid_slots = []

    for hour in range(start_hour, end_hour):
        if is_valid_time_block(hour, duration):
            valid_slots.append(hour)

    return valid_slots


def is_room_available(room, day, start_hour, duration, schedule_tracker):
    """
    Check if a room is available for the given day and time block.
    """
    room_id = room["room_id"]  # Changed from room["id"]

    if room_id not in schedule_tracker:
        return True

    if day not in schedule_tracker[room_id]:
        return True

    # Check all existing schedules for this room on this day
    for scheduled_block in schedule_tracker[room_id][day]:
        if check_time_overlap(start_hour, duration,
                              scheduled_block["start_hour"],
                              scheduled_block["duration"]):
            return False

    return True


def is_faculty_available(faculty_id, day, start_hour, duration, faculty_schedule_tracker):
    """
    Check if a faculty member is available for the given day and time block.
    """
    if faculty_id not in faculty_schedule_tracker:
        return True

    if day not in faculty_schedule_tracker[faculty_id]:
        return True

    # Check all existing schedules for this faculty on this day
    for scheduled_block in faculty_schedule_tracker[faculty_id][day]:
        if check_time_overlap(start_hour, duration,
                              scheduled_block["start_hour"],
                              scheduled_block["duration"]):
            return False

    return True


def get_faculty_daily_hours(faculty_id, day, faculty_schedule_tracker):
    """
    Calculate total hours already scheduled for a faculty member on a specific day.
    """
    if faculty_id not in faculty_schedule_tracker:
        return 0

    if day not in faculty_schedule_tracker[faculty_id]:
        return 0

    total_hours = 0
    for scheduled_block in faculty_schedule_tracker[faculty_id][day]:
        total_hours += scheduled_block["duration"]

    return total_hours


def get_faculty_next_start_hour(faculty_id, day, faculty_schedule_tracker, default_start):
    """
    Returns the consecutive next start hour for a faculty on a given day.
    This is the end time of their last scheduled class, or default_start if no classes yet.
    Ensures back-to-back (no gap) scheduling within the day.
    """
    if faculty_id not in faculty_schedule_tracker:
        return default_start
    if day not in faculty_schedule_tracker[faculty_id]:
        return default_start
    slots = faculty_schedule_tracker[faculty_id][day]
    if not slots:
        return default_start
    return math.ceil(max(s["start_hour"] + s["duration"] for s in slots))


def is_class_available(class_id, day, start_hour, duration, class_schedule_tracker):
    """
    Check if a class section is available (not already scheduled) for the given day and time block.
    Prevents the same class_id from being scheduled at overlapping times.
    """
    if class_id not in class_schedule_tracker:
        return True

    if day not in class_schedule_tracker[class_id]:
        return True

    # Check all existing schedules for this class on this day
    for scheduled_block in class_schedule_tracker[class_id][day]:
        if check_time_overlap(start_hour, duration,
                              scheduled_block["start_hour"],
                              scheduled_block["duration"]):
            return False

    return True


def is_branch_available(faculty_id, day, branch_id, faculty_branch_tracker):
    """
    Check if a faculty member can be scheduled at the given branch on a given day.
    A faculty may only be assigned to ONE college branch per day.
    Returns True if:
      - branch_id is None (class has no branch constraint), OR
      - faculty has no branch assigned on that day yet, OR
      - faculty's already-assigned branch for that day matches branch_id.
    Returns False if a DIFFERENT branch is already assigned for that day.
    """
    if branch_id is None:
        return True
    if faculty_id not in faculty_branch_tracker:
        return True
    if day not in faculty_branch_tracker[faculty_id]:
        return True
    return faculty_branch_tracker[faculty_id][day] == branch_id


def update_branch_tracker(faculty_id, days, branch_id, faculty_branch_tracker):
    """
    Record the branch a faculty is assigned to for the given days.
    Skips if branch_id is None.
    """
    if branch_id is None:
        return
    if faculty_id not in faculty_branch_tracker:
        faculty_branch_tracker[faculty_id] = {}
    for day in days:
        faculty_branch_tracker[faculty_id][day] = branch_id


def parse_time_to_hour(time_str):
    """
    Convert a time string like '8:00AM' or '1:00PM' to an integer hour.
    Returns None if parsing fails.
    """
    try:
        time_str = time_str.strip().upper()
        if 'AM' in time_str:
            time_str = time_str.replace('AM', '').strip()
            hour = int(time_str.split(':')[0])
            if hour == 12:
                hour = 0
        elif 'PM' in time_str:
            time_str = time_str.replace('PM', '').strip()
            hour = int(time_str.split(':')[0])
            if hour != 12:
                hour += 12
        else:
            hour = int(time_str.split(':')[0])
        return hour
    except Exception:
        return None


def parse_preferred_time(time_str):
    """
    Parse preferred time string into a list of (start_hour, end_hour) tuples.
    Example: "8:00AM - 12:00PM, 1:00PM - 5:00PM" -> [(8, 12), (13, 17)]
    Returns empty list if no preferred time or parsing fails.
    """
    if not time_str:
        return []
    windows = []
    for segment in time_str.split(','):
        segment = segment.strip()
        if ' - ' not in segment:
            continue
        parts = segment.split(' - ')
        if len(parts) != 2:
            continue
        start = parse_time_to_hour(parts[0].strip())
        end = parse_time_to_hour(parts[1].strip())
        if start is not None and end is not None:
            windows.append((start, end))
    return windows


def filter_slots_by_preferred_time(slots, preferred_windows, duration):
    """
    Filter time slots to only include those that fit entirely within
    at least one preferred time window.
    If no preferred windows are defined, all slots are returned unchanged.
    """
    if not preferred_windows:
        return slots
    filtered = []
    for slot in slots:
        for (win_start, win_end) in preferred_windows:
            if slot >= win_start and slot + duration <= win_end:
                filtered.append(slot)
                break
    return filtered


def filter_rooms_by_type_and_institute(rooms, course_type, institute_id):
    """
    Filter rooms by type (Lecture/Laboratory) and institute.
    More flexible matching to handle data variations.
    """
    filtered = []
    for room in rooms:
        room_type = room.get("room_type", "").strip()
        room_institute = room.get("institute_id")

        # Check room type match (case-insensitive)
        if room_type.lower() != course_type.lower():
            continue

        # Check institute match (if institute_id is provided)
        # If class has no institute_id, allow any room with matching type
        if institute_id is not None and room_institute is not None:
            if room_institute != institute_id:
                continue

        filtered.append(room)

    return filtered


def find_suitable_room(rooms, course_type, institute_id, class_size, day, start_hour,
                       duration, schedule_tracker):
    """
    Find a suitable room that matches all requirements.
    """
    # Filter rooms by type and institute
    candidate_rooms = filter_rooms_by_type_and_institute(
        rooms, course_type, institute_id)

    # Sort by capacity (prefer rooms closer to class size)
    candidate_rooms.sort(key=lambda r: r.get(
        "room_capacity", 0))  # Changed from "capacity"

    for room in candidate_rooms:
        room_capacity = room.get("room_capacity", 0)  # Changed from "capacity"

        # Check capacity (allow up to MAX_CAPACITY_EXCESS over)
        if room_capacity < class_size:
            if class_size - room_capacity > MAX_CAPACITY_EXCESS:
                continue

        # Check if room is available
        if is_room_available(room, day, start_hour, duration, schedule_tracker):
            return room

    return None


def schedule_class_with_lab(cls, rooms, faculty_id, employment_type,
                            schedule_tracker, faculty_schedule_tracker,
                            unscheduled_meetings, class_schedule_tracker,
                            day_pattern_tracker, preferred_time=None, faculty_branch_tracker=None):
    """
    Schedule a class that has both lecture and lab components.
    They must be scheduled consecutively (lecture first, then lab) on the same day.
    Classes meet on a day pattern (TTH, MF, or MWF) with hours split equally.

    Part-time faculty can only be scheduled from 5:00 PM onwards.

    IMPORTANT: Classes with lab MUST be face-to-face (require physical rooms).

    Returns list of scheduled meetings if successful, None otherwise.
    """
    institute_id = cls.get("institute_id")
    class_size = cls.get("class_size", 30)

    # Classes with lab MUST be face-to-face
    schedule_type = "face to face"

    lecture_units = cls.get("course_lec", 0)
    lab_units = cls.get("course_lab", 0)

    # Convert units to contact hours (total per week)
    lecture_hours_per_week = lecture_units * LECTURE_UNIT_TO_HOUR
    lab_hours_per_week = lab_units * LAB_UNIT_TO_HOUR
    total_hours_per_week = lecture_hours_per_week + lab_hours_per_week

    # Determine start and end hours based on employment type
    if employment_type.lower() == "part time":
        scheduling_start_hour = PART_TIME_START_HOUR
        scheduling_end_hour = PART_TIME_END_HOUR
    else:
        scheduling_start_hour = START_HOUR
        scheduling_end_hour = END_HOUR

    # Track the most recent failure reason for specific error reporting
    fail_reason = "No available time slots"

    # Try each day pattern (TTH, MF, MWF) - balanced for fairness
    balanced_patterns = get_balanced_patterns(day_pattern_tracker, total_hours_per_week)
    for pattern_name, pattern_days in balanced_patterns:
        num_meetings = len(pattern_days)
        lecture_hours = lecture_hours_per_week / num_meetings
        lab_hours = lab_hours_per_week / num_meetings
        total_duration = lecture_hours + lab_hours

        # Get consecutive start: right after the faculty's last class on ALL days
        next_starts = [
            get_faculty_next_start_hour(faculty_id, day, faculty_schedule_tracker, scheduling_start_hour)
            for day in pattern_days
        ]
        consecutive_start = max(next_starts)

        # Find slots starting from consecutive point (in order, not randomized)
        available_slots = find_available_slots(
            consecutive_start, scheduling_end_hour, total_duration)
        # Restrict to preferred time windows if the faculty has one
        available_slots = filter_slots_by_preferred_time(
            available_slots, preferred_time, total_duration)

        # Try each time slot in order to keep scheduling back-to-back
        for start_hour in available_slots:
            # Check faculty availability on ALL days
            if not all(is_faculty_available(faculty_id, day, start_hour, total_duration,
                                           faculty_schedule_tracker)
                       for day in pattern_days):
                fail_reason = "Faculty time conflict"
                continue

            # Constraint: Check faculty daily workload limit (max 8 hours per day)
            if not all(get_faculty_daily_hours(faculty_id, day, faculty_schedule_tracker) + total_duration <= 8
                       for day in pattern_days):
                fail_reason = "Faculty daily workload limit exceeded (max 8 hours)"
                continue

            # Constraint: Check class section availability on ALL days
            class_id = cls["class_id"]
            if not all(is_class_available(class_id, day, start_hour, total_duration, class_schedule_tracker)
                       for day in pattern_days):
                fail_reason = "Class section time conflict"
                continue

            # Find lecture room on first day
            lecture_room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                              pattern_days[0], start_hour, lecture_hours, schedule_tracker)
            if not lecture_room:
                fail_reason = "No available lecture room"
                continue

            # Check if same lecture room is available on ALL remaining days
            if not all(is_room_available(lecture_room, day, start_hour, lecture_hours, schedule_tracker)
                       for day in pattern_days[1:]):
                fail_reason = "No available lecture room on all pattern days"
                continue

            # Find lab room (starting right after lecture) on first day
            lab_start_hour = start_hour + lecture_hours
            lab_room = find_suitable_room(rooms, "Laboratory", institute_id, class_size,
                                          pattern_days[0], lab_start_hour, lab_hours, schedule_tracker)
            if not lab_room:
                fail_reason = "No available laboratory room"
                continue

            # Check if same lab room is available on ALL remaining days
            if not all(is_room_available(lab_room, day, lab_start_hour, lab_hours, schedule_tracker)
                       for day in pattern_days[1:]):
                fail_reason = "No available laboratory room on all pattern days"
                continue

            # Constraint: Check faculty branch consistency on ALL days
            branch_id = cls.get("college_branch_id")
            if not all(is_branch_available(faculty_id, day, branch_id, faculty_branch_tracker or {})
                       for day in pattern_days):
                fail_reason = "Faculty branch conflict"
                continue

            # All checks passed! Schedule on ALL days of the pattern
            scheduled_meetings = []

            lecture_room_id = lecture_room["room_id"]
            lab_room_id = lab_room["room_id"]

            for day in pattern_days:
                # Schedule lecture room
                if lecture_room_id not in schedule_tracker:
                    schedule_tracker[lecture_room_id] = {}
                if day not in schedule_tracker[lecture_room_id]:
                    schedule_tracker[lecture_room_id][day] = []

                schedule_tracker[lecture_room_id][day].append({
                    "start_hour": start_hour,
                    "duration": lecture_hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"]
                })

                # Schedule lab room
                if lab_room_id not in schedule_tracker:
                    schedule_tracker[lab_room_id] = {}
                if day not in schedule_tracker[lab_room_id]:
                    schedule_tracker[lab_room_id][day] = []

                schedule_tracker[lab_room_id][day].append({
                    "start_hour": lab_start_hour,
                    "duration": lab_hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"]
                })

                # Add to faculty schedule tracker
                if faculty_id not in faculty_schedule_tracker:
                    faculty_schedule_tracker[faculty_id] = {}
                if day not in faculty_schedule_tracker[faculty_id]:
                    faculty_schedule_tracker[faculty_id][day] = []

                faculty_schedule_tracker[faculty_id][day].append({
                    "start_hour": start_hour,
                    "duration": total_duration,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"]
                })

                # Add to class schedule tracker
                if class_id not in class_schedule_tracker:
                    class_schedule_tracker[class_id] = {}
                if day not in class_schedule_tracker[class_id]:
                    class_schedule_tracker[class_id][day] = []

                class_schedule_tracker[class_id][day].append({
                    "start_hour": start_hour,
                    "duration": total_duration,
                    "faculty_id": faculty_id,
                    "course_code": cls["course_code"]
                })

                # Create lecture meeting entry
                scheduled_meetings.append({
                    "class_id": cls["class_id"],
                    "set_name": cls["set_name"],
                    "course_level": cls["course_level"],
                    "course_code": cls["course_code"],
                    "program_id": cls["program_id"],
                    "program_name": cls.get("program_name", "Unknown"),
                    "program_code": cls.get("program_code", "Unknown"),
                    "institute_id": institute_id,
                    "type": "Lecture",
                    "day": day,
                    "start_hour": start_hour,
                    "duration": lecture_hours,
                    "time_slot": format_time_slot(start_hour, lecture_hours),
                    "room_id": lecture_room_id,
                    "room_name": lecture_room.get("room_name", "Unknown"),
                    "room_type": lecture_room.get("room_type", "Unknown"),
                    "room_capacity": lecture_room.get("room_capacity", 0),
                    "class_size": class_size,
                    "schedule_type": schedule_type
                })

                # Create lab meeting entry
                scheduled_meetings.append({
                    "class_id": cls["class_id"],
                    "set_name": cls["set_name"],
                    "course_level": cls["course_level"],
                    "course_code": cls["course_code"],
                    "program_id": cls["program_id"],
                    "program_name": cls.get("program_name", "Unknown"),
                    "program_code": cls.get("program_code", "Unknown"),
                    "institute_id": institute_id,
                    "type": "Laboratory",
                    "day": day,
                    "start_hour": lab_start_hour,
                    "duration": lab_hours,
                    "time_slot": format_time_slot(lab_start_hour, lab_hours),
                    "room_id": lab_room_id,
                    "room_name": lab_room.get("room_name", "Unknown"),
                    "room_type": lab_room.get("room_type", "Unknown"),
                    "room_capacity": lab_room.get("room_capacity", 0),
                    "class_size": class_size,
                    "schedule_type": schedule_type
                })

            # Update day pattern tracker for fairness
            day_pattern_tracker[pattern_name] = day_pattern_tracker.get(pattern_name, 0) + 1

            # Update faculty branch tracker for all days
            update_branch_tracker(faculty_id, pattern_days, branch_id, faculty_branch_tracker or {})

            return scheduled_meetings

    # Fallback: Try Wednesday with full hours (not split)
    wednesday = "Wednesday"
    wed_lecture_hours = lecture_hours_per_week
    wed_lab_hours = lab_hours_per_week
    wed_total_duration = wed_lecture_hours + wed_lab_hours

    # Get consecutive start on Wednesday
    wed_consecutive_start = get_faculty_next_start_hour(
        faculty_id, wednesday, faculty_schedule_tracker, scheduling_start_hour)
    available_slots = find_available_slots(
        wed_consecutive_start, scheduling_end_hour, wed_total_duration)
    available_slots = filter_slots_by_preferred_time(
        available_slots, preferred_time, wed_total_duration)

    for start_hour in available_slots:
        if not is_faculty_available(faculty_id, wednesday, start_hour, wed_total_duration,
                                    faculty_schedule_tracker):
            fail_reason = "Faculty time conflict"
            continue

        faculty_hours_wed = get_faculty_daily_hours(faculty_id, wednesday, faculty_schedule_tracker)
        if faculty_hours_wed + wed_total_duration > 8:
            fail_reason = "Faculty daily workload limit exceeded (max 8 hours)"
            continue

        class_id = cls["class_id"]
        if not is_class_available(class_id, wednesday, start_hour, wed_total_duration, class_schedule_tracker):
            fail_reason = "Class section time conflict"
            continue

        branch_id = cls.get("college_branch_id")
        if not is_branch_available(faculty_id, wednesday, branch_id, faculty_branch_tracker or {}):
            fail_reason = "Faculty branch conflict"
            continue

        lecture_room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                          wednesday, start_hour, wed_lecture_hours, schedule_tracker)
        if not lecture_room:
            fail_reason = "No available lecture room"
            continue

        wed_lab_start_hour = start_hour + wed_lecture_hours
        lab_room = find_suitable_room(rooms, "Laboratory", institute_id, class_size,
                                      wednesday, wed_lab_start_hour, wed_lab_hours, schedule_tracker)
        if not lab_room:
            fail_reason = "No available laboratory room"
            continue

        # All checks passed! Schedule on Wednesday only
        scheduled_meetings = []

        lecture_room_id = lecture_room["room_id"]
        if lecture_room_id not in schedule_tracker:
            schedule_tracker[lecture_room_id] = {}
        if wednesday not in schedule_tracker[lecture_room_id]:
            schedule_tracker[lecture_room_id][wednesday] = []
        schedule_tracker[lecture_room_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "class_id": cls["class_id"],
            "course_code": cls["course_code"]
        })

        lab_room_id = lab_room["room_id"]
        if lab_room_id not in schedule_tracker:
            schedule_tracker[lab_room_id] = {}
        if wednesday not in schedule_tracker[lab_room_id]:
            schedule_tracker[lab_room_id][wednesday] = []
        schedule_tracker[lab_room_id][wednesday].append({
            "start_hour": wed_lab_start_hour,
            "duration": wed_lab_hours,
            "class_id": cls["class_id"],
            "course_code": cls["course_code"]
        })

        if faculty_id not in faculty_schedule_tracker:
            faculty_schedule_tracker[faculty_id] = {}
        if wednesday not in faculty_schedule_tracker[faculty_id]:
            faculty_schedule_tracker[faculty_id][wednesday] = []
        faculty_schedule_tracker[faculty_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_total_duration,
            "class_id": cls["class_id"],
            "course_code": cls["course_code"]
        })

        if class_id not in class_schedule_tracker:
            class_schedule_tracker[class_id] = {}
        if wednesday not in class_schedule_tracker[class_id]:
            class_schedule_tracker[class_id][wednesday] = []
        class_schedule_tracker[class_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_total_duration,
            "faculty_id": faculty_id,
            "course_code": cls["course_code"]
        })

        scheduled_meetings.append({
            "class_id": cls["class_id"],
            "set_name": cls["set_name"],
            "course_level": cls["course_level"],
            "course_code": cls["course_code"],
            "program_id": cls["program_id"],
            "program_name": cls.get("program_name", "Unknown"),
            "program_code": cls.get("program_code", "Unknown"),
            "institute_id": institute_id,
            "type": "Lecture",
            "day": wednesday,
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "time_slot": format_time_slot(start_hour, wed_lecture_hours),
            "room_id": lecture_room_id,
            "room_name": lecture_room.get("room_name", "Unknown"),
            "room_type": lecture_room.get("room_type", "Unknown"),
            "room_capacity": lecture_room.get("room_capacity", 0),
            "class_size": class_size,
            "schedule_type": schedule_type
        })

        scheduled_meetings.append({
            "class_id": cls["class_id"],
            "set_name": cls["set_name"],
            "course_level": cls["course_level"],
            "course_code": cls["course_code"],
            "program_id": cls["program_id"],
            "program_name": cls.get("program_name", "Unknown"),
            "program_code": cls.get("program_code", "Unknown"),
            "institute_id": institute_id,
            "type": "Laboratory",
            "day": wednesday,
            "start_hour": wed_lab_start_hour,
            "duration": wed_lab_hours,
            "time_slot": format_time_slot(wed_lab_start_hour, wed_lab_hours),
            "room_id": lab_room_id,
            "room_name": lab_room.get("room_name", "Unknown"),
            "room_type": lab_room.get("room_type", "Unknown"),
            "room_capacity": lab_room.get("room_capacity", 0),
            "class_size": class_size,
            "schedule_type": schedule_type
        })

        update_branch_tracker(faculty_id, [wednesday], branch_id, faculty_branch_tracker or {})

        return scheduled_meetings

    # Could not schedule
    unscheduled_meetings.append({
        "class_id": cls["class_id"],
        "course_code": cls["course_code"],
        "course_id": cls.get("course_id"),
        "institute_id": cls.get("institute_id"),
        "class_size": cls.get("class_size", 30),
        "faculty_name": cls.get("faculty_name", "Unknown"),
        "program_id": cls["program_id"],
        "program_name": cls.get("program_name", "Unknown"),
        "program_code": cls.get("program_code", "Unknown"),
        "type": "Lecture+Lab",
        "hours": f"{lecture_hours_per_week}h lec + {lab_hours_per_week}h lab per week",
        "reason": fail_reason
    })

    return None


def schedule_lecture_only(cls, rooms, faculty_id, employment_type,
                          schedule_tracker, faculty_schedule_tracker,
                          unscheduled_meetings, class_schedule_tracker,
                          lecture_type_tracker, day_pattern_tracker, preferred_time=None, faculty_branch_tracker=None,
                          day_f2f_tracker=None):
    """
    Schedule a class that has only lecture (no lab).
    Classes meet on a day pattern (TTH, MF, or MWF) with hours split equally per meeting.

    Part-time faculty can only be scheduled from 5:00 PM onwards.

    Strategy:
    - Each meeting day in the pattern gets its OWN face-to-face or online assignment
    - num_f2f_days = int(len(pattern_days) * TARGET_FACE_TO_FACE_PERCENTAGE + 0.5)
      e.g. 30% on MF (2 days) -> 1 f2f + 1 online;  30% on MWF (3 days) -> 1 f2f + 2 online
    - Fairness: days with fewer f2f assignments (day_f2f_tracker) get f2f priority,
      ties are broken randomly so no single day always wins
    - One room is found for ALL f2f days together; if unavailable, those days fall back to online
    - Day patterns are balanced for fair distribution (day_pattern_tracker)
    - Patterns are filtered by minimum 1-hour-per-meeting rule

    Returns list of scheduled meetings if successful, None otherwise.
    """
    if day_f2f_tracker is None:
        day_f2f_tracker = {}

    institute_id = cls.get("institute_id")
    class_size = cls.get("class_size", 30)

    lecture_units = cls.get("course_lec", 0)
    lecture_hours_per_week = lecture_units * LECTURE_UNIT_TO_HOUR

    # Determine start and end hours based on employment type
    if employment_type.lower() == "part time":
        scheduling_start_hour = PART_TIME_START_HOUR
        scheduling_end_hour = PART_TIME_END_HOUR
    else:
        scheduling_start_hour = START_HOUR
        scheduling_end_hour = END_HOUR

    # Track the most recent failure reason for specific error reporting
    fail_reason = "No available time slots"

    # Try each day pattern - balanced for fairness
    balanced_patterns = get_balanced_patterns(day_pattern_tracker, lecture_hours_per_week)
    for pattern_name, pattern_days in balanced_patterns:
        num_meetings = len(pattern_days)
        lecture_hours = lecture_hours_per_week / num_meetings  # Hours per meeting

        # Get consecutive start: right after the faculty's last class on ALL days
        next_starts = [
            get_faculty_next_start_hour(faculty_id, day, faculty_schedule_tracker, scheduling_start_hour)
            for day in pattern_days
        ]
        consecutive_start = max(next_starts)

        # Find slots starting from consecutive point (in order, not randomized)
        available_slots = find_available_slots(
            consecutive_start, scheduling_end_hour, lecture_hours)
        # Restrict to preferred time windows if the faculty has one
        available_slots = filter_slots_by_preferred_time(
            available_slots, preferred_time, lecture_hours)

        # Try each time slot in order to keep scheduling back-to-back
        for start_hour in available_slots:
            # Check faculty availability on ALL days
            if not all(is_faculty_available(faculty_id, day, start_hour, lecture_hours,
                                           faculty_schedule_tracker)
                       for day in pattern_days):
                fail_reason = "Faculty time conflict"
                continue

            # Constraint: Check faculty daily workload limit (max 8 hours per day)
            if not all(get_faculty_daily_hours(faculty_id, day, faculty_schedule_tracker) + lecture_hours <= 8
                       for day in pattern_days):
                fail_reason = "Faculty daily workload limit exceeded (max 8 hours)"
                continue

            # Constraint: Check class section availability on ALL days
            class_id = cls["class_id"]
            if not all(is_class_available(class_id, day, start_hour, lecture_hours, class_schedule_tracker)
                       for day in pattern_days):
                fail_reason = "Class section time conflict"
                continue

            # Constraint: Check faculty branch consistency on ALL days
            branch_id = cls.get("college_branch_id")
            if not all(is_branch_available(faculty_id, day, branch_id, faculty_branch_tracker or {})
                       for day in pattern_days):
                fail_reason = "Faculty branch conflict"
                continue

            # --- Per-day face-to-face / online assignment ---
            # Decide how many days in this pattern are f2f (standard rounding)
            n = len(pattern_days)
            num_f2f = int(n * TARGET_FACE_TO_FACE_PERCENTAGE + 0.5)
            num_f2f = max(0, min(n, num_f2f))

            # Fairness: days with fewer f2f assignments get priority; ties broken randomly
            days_sorted = sorted(pattern_days,
                                 key=lambda d: (day_f2f_tracker.get(d, 0), random.random()))
            f2f_day_set = set(days_sorted[:num_f2f])
            day_types = {d: ("face to face" if d in f2f_day_set else "online")
                         for d in pattern_days}

            # Find ONE room available on ALL f2f days (same room each occurrence)
            f2f_days = [d for d in pattern_days if day_types[d] == "face to face"]
            lecture_room = None
            if f2f_days:
                lecture_room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                                  f2f_days[0], start_hour, lecture_hours, schedule_tracker)
                if lecture_room and not all(
                        is_room_available(lecture_room, d, start_hour, lecture_hours, schedule_tracker)
                        for d in f2f_days[1:]):
                    lecture_room = None  # room not available on all f2f days
                if not lecture_room:
                    # No room for all f2f days: fall back all f2f days to online
                    for d in f2f_days:
                        day_types[d] = "online"
                    f2f_days = []

            lecture_room_id = lecture_room["room_id"] if lecture_room else None

            # Schedule each day with its own schedule_type
            scheduled_meetings = []
            for day in pattern_days:
                schedule_type = day_types[day]
                day_is_f2f = (schedule_type == "face to face")

                # Room tracker (only for f2f days)
                if day_is_f2f and lecture_room:
                    if lecture_room_id not in schedule_tracker:
                        schedule_tracker[lecture_room_id] = {}
                    if day not in schedule_tracker[lecture_room_id]:
                        schedule_tracker[lecture_room_id][day] = []
                    schedule_tracker[lecture_room_id][day].append({
                        "start_hour": start_hour,
                        "duration": lecture_hours,
                        "class_id": cls["class_id"],
                        "course_code": cls["course_code"]
                    })

                # Faculty schedule tracker (all days)
                if faculty_id not in faculty_schedule_tracker:
                    faculty_schedule_tracker[faculty_id] = {}
                if day not in faculty_schedule_tracker[faculty_id]:
                    faculty_schedule_tracker[faculty_id][day] = []
                faculty_schedule_tracker[faculty_id][day].append({
                    "start_hour": start_hour,
                    "duration": lecture_hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"]
                })

                # Class schedule tracker (all days)
                if class_id not in class_schedule_tracker:
                    class_schedule_tracker[class_id] = {}
                if day not in class_schedule_tracker[class_id]:
                    class_schedule_tracker[class_id][day] = []
                class_schedule_tracker[class_id][day].append({
                    "start_hour": start_hour,
                    "duration": lecture_hours,
                    "faculty_id": faculty_id,
                    "course_code": cls["course_code"]
                })

                # Build meeting entry with per-day schedule_type
                meeting_entry = {
                    "class_id": cls["class_id"],
                    "set_name": cls["set_name"],
                    "course_level": cls["course_level"],
                    "course_code": cls["course_code"],
                    "program_id": cls["program_id"],
                    "program_name": cls.get("program_name", "Unknown"),
                    "program_code": cls.get("program_code", "Unknown"),
                    "institute_id": institute_id,
                    "type": "Lecture",
                    "day": day,
                    "start_hour": start_hour,
                    "duration": lecture_hours,
                    "time_slot": format_time_slot(start_hour, lecture_hours),
                    "class_size": class_size,
                    "schedule_type": schedule_type
                }

                if day_is_f2f and lecture_room:
                    meeting_entry["room_id"] = lecture_room_id
                    meeting_entry["room_name"] = lecture_room.get("room_name", "Unknown")
                    meeting_entry["room_type"] = lecture_room.get("room_type", "Unknown")
                    meeting_entry["room_capacity"] = lecture_room.get("room_capacity", 0)
                else:
                    meeting_entry["room_id"] = None
                    meeting_entry["room_name"] = "Online"
                    meeting_entry["room_type"] = "Online"
                    meeting_entry["room_capacity"] = 0

                scheduled_meetings.append(meeting_entry)

            # Update lecture_type_tracker with actual per-meeting hours
            for day in pattern_days:
                if day_types[day] == "face to face":
                    lecture_type_tracker["face_to_face_hours"] += lecture_hours
                else:
                    lecture_type_tracker["online_hours"] += lecture_hours
            lecture_type_tracker["total_lecture_hours"] += lecture_hours_per_week

            # Update day_f2f_tracker for fairness across future classes
            for day in pattern_days:
                if day_types[day] == "face to face":
                    day_f2f_tracker[day] = day_f2f_tracker.get(day, 0) + 1

            # Update day pattern tracker for fairness
            day_pattern_tracker[pattern_name] = day_pattern_tracker.get(pattern_name, 0) + 1

            # Update faculty branch tracker for all days
            update_branch_tracker(faculty_id, pattern_days, branch_id, faculty_branch_tracker or {})

            return scheduled_meetings

    # Fallback: Try Wednesday with full hours (not split)
    wednesday = "Wednesday"
    wed_lecture_hours = lecture_hours_per_week  # Full hours for single day

    # Get consecutive start on Wednesday
    wed_consecutive_start = get_faculty_next_start_hour(
        faculty_id, wednesday, faculty_schedule_tracker, scheduling_start_hour)
    available_slots = find_available_slots(
        wed_consecutive_start, scheduling_end_hour, wed_lecture_hours)
    available_slots = filter_slots_by_preferred_time(
        available_slots, preferred_time, wed_lecture_hours)

    for start_hour in available_slots:
        if not is_faculty_available(faculty_id, wednesday, start_hour, wed_lecture_hours,
                                    faculty_schedule_tracker):
            fail_reason = "Faculty time conflict"
            continue

        faculty_hours_wed = get_faculty_daily_hours(faculty_id, wednesday, faculty_schedule_tracker)
        if faculty_hours_wed + wed_lecture_hours > 8:
            fail_reason = "Faculty daily workload limit exceeded (max 8 hours)"
            continue

        class_id = cls["class_id"]
        if not is_class_available(class_id, wednesday, start_hour, wed_lecture_hours, class_schedule_tracker):
            fail_reason = "Class section time conflict"
            continue

        branch_id = cls.get("college_branch_id")
        if not is_branch_available(faculty_id, wednesday, branch_id, faculty_branch_tracker or {}):
            fail_reason = "Faculty branch conflict"
            continue

        # Per-day f2f/online for Wednesday (single day, same fairness logic as pattern days)
        # int(1 * pct + 0.5): 1 if pct >= 0.5 (50%+), 0 otherwise (below 50% -> online)
        wed_num_f2f = int(1 * TARGET_FACE_TO_FACE_PERCENTAGE + 0.5)
        wed_schedule_type = "face to face" if wed_num_f2f == 1 else "online"

        lecture_room = None
        schedule_type = wed_schedule_type

        if wed_schedule_type == "face to face":
            lecture_room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                              wednesday, start_hour, wed_lecture_hours, schedule_tracker)
            if not lecture_room:
                schedule_type = "online"
        # If target is online, no room needed

        # Schedule on Wednesday only
        scheduled_meetings = []
        lecture_room_id = lecture_room["room_id"] if lecture_room else None

        # Add to room schedule tracker (only if face-to-face)
        if lecture_room:
            if lecture_room_id not in schedule_tracker:
                schedule_tracker[lecture_room_id] = {}
            if wednesday not in schedule_tracker[lecture_room_id]:
                schedule_tracker[lecture_room_id][wednesday] = []
            schedule_tracker[lecture_room_id][wednesday].append({
                "start_hour": start_hour,
                "duration": wed_lecture_hours,
                "class_id": cls["class_id"],
                "course_code": cls["course_code"]
            })

        if faculty_id not in faculty_schedule_tracker:
            faculty_schedule_tracker[faculty_id] = {}
        if wednesday not in faculty_schedule_tracker[faculty_id]:
            faculty_schedule_tracker[faculty_id][wednesday] = []
        faculty_schedule_tracker[faculty_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "class_id": cls["class_id"],
            "course_code": cls["course_code"]
        })

        if class_id not in class_schedule_tracker:
            class_schedule_tracker[class_id] = {}
        if wednesday not in class_schedule_tracker[class_id]:
            class_schedule_tracker[class_id][wednesday] = []
        class_schedule_tracker[class_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "faculty_id": faculty_id,
            "course_code": cls["course_code"]
        })

        # Create meeting entry (Wednesday - full hours)
        meeting_entry = {
            "class_id": cls["class_id"],
            "set_name": cls["set_name"],
            "course_level": cls["course_level"],
            "course_code": cls["course_code"],
            "program_id": cls["program_id"],
            "program_name": cls.get("program_name", "Unknown"),
            "program_code": cls.get("program_code", "Unknown"),
            "institute_id": institute_id,
            "type": "Lecture",
            "day": wednesday,
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "time_slot": format_time_slot(start_hour, wed_lecture_hours),
            "class_size": class_size,
            "schedule_type": schedule_type
        }

        if lecture_room:
            meeting_entry["room_id"] = lecture_room_id
            meeting_entry["room_name"] = lecture_room.get("room_name", "Unknown")
            meeting_entry["room_type"] = lecture_room.get("room_type", "Unknown")
            meeting_entry["room_capacity"] = lecture_room.get("room_capacity", 0)
        else:
            meeting_entry["room_id"] = None
            meeting_entry["room_name"] = "Online"
            meeting_entry["room_type"] = "Online"
            meeting_entry["room_capacity"] = 0

        scheduled_meetings.append(meeting_entry)

        # Update lecture type tracker with Wednesday hours
        if schedule_type == "online":
            lecture_type_tracker["online_hours"] += wed_lecture_hours
        else:
            lecture_type_tracker["face_to_face_hours"] += wed_lecture_hours
            day_f2f_tracker[wednesday] = day_f2f_tracker.get(wednesday, 0) + 1
        lecture_type_tracker["total_lecture_hours"] += wed_lecture_hours

        # Update faculty branch tracker for Wednesday
        update_branch_tracker(faculty_id, [wednesday], branch_id, faculty_branch_tracker or {})

        return scheduled_meetings

    # Could not schedule on any day pattern or Wednesday
    unscheduled_meetings.append({
        "class_id": cls["class_id"],
        "course_code": cls["course_code"],
        "course_id": cls.get("course_id"),
        "institute_id": cls.get("institute_id"),
        "class_size": cls.get("class_size", 30),
        "faculty_name": cls.get("faculty_name", "Unknown"),
        "program_id": cls["program_id"],
        "program_name": cls.get("program_name", "Unknown"),
        "program_code": cls.get("program_code", "Unknown"),
        "type": "Lecture",
        "hours": f"{lecture_hours_per_week}h per week",
        "reason": fail_reason
    })

    return None


def schedule_class_meeting(cls, course_type, hours, rooms, faculty_id,
                           schedule_tracker, faculty_schedule_tracker,
                           unscheduled_meetings):
    """
    DEPRECATED: This function is kept for backward compatibility but not used in new logic.
    Try to schedule a single meeting (lecture or laboratory).
    Returns scheduled meeting dict if successful, None otherwise.
    """
    institute_id = cls.get("institute_id")
    class_size = cls.get("class_size", 30)  # Default to 30 if not specified

    # Track the most recent failure reason for specific error reporting
    fail_reason = "No available time slots"

    # Try each day
    for day in DAYS:
        # Find available time slots for this duration
        available_slots = find_available_slots(START_HOUR, END_HOUR, hours)

        # Try each time slot
        for start_hour in available_slots:
            # Check faculty availability
            if not is_faculty_available(faculty_id, day, start_hour, hours,
                                        faculty_schedule_tracker):
                fail_reason = "Faculty time conflict"
                continue

            # Find suitable room
            room = find_suitable_room(rooms, course_type, institute_id, class_size,
                                      day, start_hour, hours, schedule_tracker)

            if not room:
                fail_reason = f"No available {course_type.lower()} room"

            if room:
                # Schedule this meeting
                room_id = room["room_id"]

                # Add to room schedule tracker
                if room_id not in schedule_tracker:
                    schedule_tracker[room_id] = {}
                if day not in schedule_tracker[room_id]:
                    schedule_tracker[room_id][day] = []

                schedule_tracker[room_id][day].append({
                    "start_hour": start_hour,
                    "duration": hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"]
                })

                # Add to faculty schedule tracker
                if faculty_id not in faculty_schedule_tracker:
                    faculty_schedule_tracker[faculty_id] = {}
                if day not in faculty_schedule_tracker[faculty_id]:
                    faculty_schedule_tracker[faculty_id][day] = []

                faculty_schedule_tracker[faculty_id][day].append({
                    "start_hour": start_hour,
                    "duration": hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"]
                })

                return {
                    "class_id": cls["class_id"],
                    "set_name": cls["set_name"],
                    "course_level": cls["course_level"],
                    "course_code": cls["course_code"],
                    "program_id": cls["program_id"],
                    "institute_id": institute_id,
                    "type": course_type,
                    "day": day,
                    "start_hour": start_hour,
                    "duration": hours,
                    "time_slot": format_time_slot(start_hour, hours),
                    "room_id": room_id,
                    "room_name": room.get("room_name", "Unknown"),
                    "room_type": room.get("room_type", "Unknown"),
                    # Changed from "capacity"
                    "room_capacity": room.get("room_capacity", 0),
                    "class_size": class_size
                }

    # Could not schedule
    unscheduled_meetings.append({
        "class_id": cls["class_id"],
        "course_code": cls["course_code"],
        "course_id": cls.get("course_id"),
        "institute_id": cls.get("institute_id"),
        "class_size": cls.get("class_size", 30),
        "faculty_name": cls.get("faculty_name", "Unknown"),
        "type": course_type,
        "hours": hours,
        "reason": fail_reason
    })

    return None


def create_schedule(faculty_loads, rooms):
    """
    Create a complete schedule for all faculty loads.
    Scheduling rules:
    - Lecture: 1 student unit = 1 contact hour = 1 teacher unit
    - Laboratory: 1 student unit = 3 contact hours = 2.25 teacher units (3 × 0.75)
    - Classes meet on day patterns (TTH, MF, or MWF) with hours split equally
    - Pattern chosen dynamically: must have >= 1h per meeting, least-used first
    - Lecture and lab are scheduled consecutively (lecture first, then lab)
    - Wednesday standalone is fallback only (full hours, not split)

    Returns scheduled classes and unscheduled meetings.
    """
    schedule_tracker = {}  # Track room schedules
    faculty_schedule_tracker = {}  # Track faculty schedules
    class_schedule_tracker = {}  # Track class section schedules to prevent self-conflicts
    # Track lecture hours for f2f/online percentage distribution
    lecture_type_tracker = {"face_to_face_hours": 0.0, "online_hours": 0.0, "total_lecture_hours": 0.0}
    # Track day pattern usage for fair distribution
    day_pattern_tracker = {"TTH": 0, "MF": 0, "MWF": 0}
    # Track per-day f2f assignment count so no single day always gets f2f
    day_f2f_tracker = {}
    faculty_branch_tracker = {}
    complete_schedule = []
    unscheduled_meetings = []

    print("\n" + "="*80)
    print(" " * 25 + "STARTING SCHEDULING PROCESS")
    print("="*80)
    print("Scheduling Rules:")
    print("  - Lecture: 1 student unit = 1 contact hour per week")
    print("  - Laboratory: 1 student unit = 3 contact hours per week")
    print("  - Teacher Units: Lecture 1:1, Lab 1:2.25")
    print("  - Primary: Classes meet on day patterns (TTH, MF, or MWF)")
    print("  - Pattern valid only if weekly_hours / num_meetings >= 1h per meeting")
    print("  - Hours SPLIT equally between meetings of the chosen pattern")
    print("  - Fallback: Wednesday scheduling with FULL hours (not split)")
    print("  - Lecture and lab scheduled consecutively in each meeting")
    print("  - Faculty daily workload limit: Max 8 hours per day")
    print("  - Part-time faculty: Scheduled from 5:00 PM to 10:00 PM only")
    print("  - Full-time faculty: Scheduled anytime (7:00 AM to 9:00 PM)")
    print("  - Laboratory classes MUST be face-to-face")
    print(f"  - Lecture f2f target: {int(TARGET_FACE_TO_FACE_PERCENTAGE * 100)}% per meeting day "
          f"(e.g. MF: 1 day f2f + 1 online; MWF: 1 day f2f + 2 online at 30%)")
    print("  - Day patterns and time slots are RANDOMIZED for fair distribution")
    print("="*80)

    # Shuffle faculty order for fair distribution
    faculty_items = list(faculty_loads.items())
    random.shuffle(faculty_items)

    # Process each faculty's assigned classes
    for faculty_id, faculty_info in faculty_items:
        faculty_name = faculty_info["faculty_name"]
        employment_type = faculty_info.get("employment_type", "full time")
        preferred_time = faculty_info.get("preferred_time", [])

        if len(faculty_info["assigned_classes"]) == 0:
            continue

        print(
            f"\nScheduling classes for: {faculty_name} (ID: {faculty_id}) [{employment_type.title()}]")

        # Shuffle classes for fair distribution
        classes_to_schedule = list(faculty_info["assigned_classes"])
        random.shuffle(classes_to_schedule)

        for cls in classes_to_schedule:
            lecture_units = cls.get("course_lec", 0)
            lab_units = cls.get("course_lab", 0)

            # Convert to contact hours per week
            lecture_hours_per_week = lecture_units * LECTURE_UNIT_TO_HOUR
            lab_hours_per_week = lab_units * LAB_UNIT_TO_HOUR

            # Determine scheduling strategy
            if lecture_units > 0 and lab_units > 0:
                # Course has both lecture and lab
                print(
                    f"  Scheduling {cls['course_code']} (Lec: {lecture_units}u={lecture_hours_per_week}h/wk + Lab: {lab_units}u={lab_hours_per_week}h/wk)...", end=" ")
                scheduled_meetings = schedule_class_with_lab(
                    cls, rooms, faculty_id, employment_type,
                    schedule_tracker, faculty_schedule_tracker, unscheduled_meetings, class_schedule_tracker,
                    day_pattern_tracker, preferred_time, faculty_branch_tracker
                )

                if scheduled_meetings:
                    for meeting in scheduled_meetings:
                        meeting["faculty_id"] = faculty_id
                        meeting["faculty_name"] = faculty_name
                        meeting["employment_type"] = employment_type
                        complete_schedule.append(meeting)
                    print("[OK] Scheduled")
                else:
                    if unscheduled_meetings:
                        unscheduled_meetings[-1]["faculty_name"] = faculty_name
                    print("[FAILED]")

            elif lecture_units > 0:
                # Course has only lecture
                print(
                    f"  Scheduling {cls['course_code']} (Lecture only: {lecture_units}u={lecture_hours_per_week}h/wk)...", end=" ")
                scheduled_meetings = schedule_lecture_only(
                    cls, rooms, faculty_id, employment_type,
                    schedule_tracker, faculty_schedule_tracker, unscheduled_meetings, class_schedule_tracker,
                    lecture_type_tracker, day_pattern_tracker, preferred_time, faculty_branch_tracker,
                    day_f2f_tracker
                )

                if scheduled_meetings:
                    for meeting in scheduled_meetings:
                        meeting["faculty_id"] = faculty_id
                        meeting["faculty_name"] = faculty_name
                        meeting["employment_type"] = employment_type
                        complete_schedule.append(meeting)
                    print("[OK] Scheduled")
                else:
                    if unscheduled_meetings:
                        unscheduled_meetings[-1]["faculty_name"] = faculty_name
                    print("[FAILED]")

            elif lab_units > 0:
                # Course has only lab (unusual, but handle it)
                print(
                    f"  Scheduling {cls['course_code']} (Lab only: {lab_units}u={lab_hours_per_week}h/wk)...", end=" ")
                # Treat lab-only as lecture for scheduling purposes
                scheduled_meetings = schedule_lecture_only(
                    cls, rooms, faculty_id, employment_type,
                    schedule_tracker, faculty_schedule_tracker, unscheduled_meetings, class_schedule_tracker,
                    lecture_type_tracker, day_pattern_tracker, preferred_time, faculty_branch_tracker,
                    day_f2f_tracker
                )

                if scheduled_meetings:
                    # Change type to Laboratory
                    for meeting in scheduled_meetings:
                        meeting["type"] = "Laboratory"
                        meeting["faculty_id"] = faculty_id
                        meeting["faculty_name"] = faculty_name
                        meeting["employment_type"] = employment_type
                        complete_schedule.append(meeting)
                    print("[OK] Scheduled")
                else:
                    if unscheduled_meetings:
                        unscheduled_meetings[-1]["faculty_name"] = faculty_name
                    print("[FAILED]")

    print("\n" + "="*80)
    print(f"Scheduling Complete: {len(complete_schedule)} meetings scheduled, "
          f"{len(unscheduled_meetings)} unscheduled")
    print("-"*80)
    total_lecture_hours = lecture_type_tracker["total_lecture_hours"]
    if total_lecture_hours > 0:
        f2f_hours = lecture_type_tracker["face_to_face_hours"]
        online_hours = lecture_type_tracker["online_hours"]
        f2f_pct = (f2f_hours / total_lecture_hours) * 100
        online_pct = (online_hours / total_lecture_hours) * 100
        print(f"Lecture Distribution: {f2f_hours:.1f}h face-to-face ({f2f_pct:.1f}%), "
              f"{online_hours:.1f}h online ({online_pct:.1f}%) "
              f"[Target: {int(TARGET_FACE_TO_FACE_PERCENTAGE * 100)}% f2f]")
    print("-"*80)
    # Show day pattern distribution
    tth_count = day_pattern_tracker.get("TTH", 0)
    mf_count = day_pattern_tracker.get("MF", 0)
    mwf_count = day_pattern_tracker.get("MWF", 0)
    # Count Wednesday-only fallback schedules from complete_schedule
    wed_only_classes = set()
    for m in complete_schedule:
        if m["day"] == "Wednesday":
            wed_only_classes.add(m["class_id"])
    # Remove classes that also appear on other days (those are MWF, not Wed-only)
    for m in complete_schedule:
        if m["day"] != "Wednesday":
            wed_only_classes.discard(m["class_id"])
    wed_count = len(wed_only_classes)
    total_patterns = tth_count + mf_count + mwf_count + wed_count
    if total_patterns > 0:
        print(f"Day Distribution: TTH: {tth_count}, MF: {mf_count}, MWF: {mwf_count}, Wed-only: {wed_count}")
    # Show per-day f2f assignment counts (fairness audit)
    if day_f2f_tracker:
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        f2f_summary = ", ".join(
            f"{d[:3]}: {day_f2f_tracker[d]}"
            for d in day_order if d in day_f2f_tracker and day_f2f_tracker[d] > 0
        )
        if f2f_summary:
            print(f"  F2F meetings per day: {f2f_summary}")

    # Validate schedule for conflicts
    print("-"*80)
    print("Validating schedule for conflicts...")
    conflicts = validate_schedule(complete_schedule)
    if conflicts:
        print(f"WARNING: Found {len(conflicts)} conflicts:")
        for conflict in conflicts[:10]:  # Show first 10 conflicts
            print(f"  - {conflict}")
        if len(conflicts) > 10:
            print(f"  ... and {len(conflicts) - 10} more conflicts")
    else:
        print("No conflicts detected!")
    print("="*80)

    return complete_schedule, unscheduled_meetings


def validate_schedule(schedule):
    """
    Validate the schedule for conflicts:
    - Same class_id at same day/time
    - Same room at same day/time (excluding online)
    - Same faculty at same day/time
    Returns list of conflict descriptions.
    """
    conflicts = []

    # Group by day
    for day in DAYS:
        day_schedule = [m for m in schedule if m["day"] == day]

        # Check for class conflicts (same class_id at overlapping times)
        class_groups = {}
        for meeting in day_schedule:
            class_id = meeting["class_id"]
            if class_id not in class_groups:
                class_groups[class_id] = []
            class_groups[class_id].append(meeting)

        for class_id, meetings in class_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append(
                                f"Class conflict: {m1['course_code']} (class_id={class_id}) "
                                f"on {day} at {m1['time_slot']} and {m2['time_slot']}"
                            )

        # Check for room conflicts (same room at overlapping times, excluding online)
        room_groups = {}
        for meeting in day_schedule:
            room_id = meeting.get("room_id")
            if room_id is None:  # Skip online classes
                continue
            if room_id not in room_groups:
                room_groups[room_id] = []
            room_groups[room_id].append(meeting)

        for room_id, meetings in room_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append(
                                f"Room conflict: {m1['room_name']} (room_id={room_id}) "
                                f"on {day} at {m1['time_slot']} ({m1['course_code']}) "
                                f"and {m2['time_slot']} ({m2['course_code']})"
                            )

        # Check for faculty conflicts (same faculty at overlapping times)
        faculty_groups = {}
        for meeting in day_schedule:
            faculty_id = meeting.get("faculty_id")
            if faculty_id is None:
                continue
            if faculty_id not in faculty_groups:
                faculty_groups[faculty_id] = []
            faculty_groups[faculty_id].append(meeting)

        for faculty_id, meetings in faculty_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append(
                                f"Faculty conflict: {m1['faculty_name']} (faculty_id={faculty_id}) "
                                f"on {day} at {m1['time_slot']} ({m1['course_code']}) "
                                f"and {m2['time_slot']} ({m2['course_code']})"
                            )

    return conflicts


def validate_schedule_detailed(schedule):
    """
    Validate the schedule for conflicts and return detailed conflict data for Excel export.
    Returns list of conflict dictionaries with structured data.
    """
    conflicts = []

    # Group by day
    for day in DAYS:
        day_schedule = [m for m in schedule if m["day"] == day]

        # Check for class conflicts (same class_id at overlapping times)
        class_groups = {}
        for meeting in day_schedule:
            class_id = meeting["class_id"]
            if class_id not in class_groups:
                class_groups[class_id] = []
            class_groups[class_id].append(meeting)

        for class_id, meetings in class_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append({
                                "type": "Class Conflict",
                                "day": day,
                                "time_slot_1": m1["time_slot"],
                                "time_slot_2": m2["time_slot"],
                                "course_1": m1["course_code"],
                                "course_2": m2["course_code"],
                                "resource": f"Class Section",
                                "resource_id": class_id,
                                "details": f"Same class section scheduled at overlapping times"
                            })

        # Check for room conflicts (same room at overlapping times, excluding online)
        room_groups = {}
        for meeting in day_schedule:
            room_id = meeting.get("room_id")
            if room_id is None:  # Skip online classes
                continue
            if room_id not in room_groups:
                room_groups[room_id] = []
            room_groups[room_id].append(meeting)

        for room_id, meetings in room_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append({
                                "type": "Room Conflict",
                                "day": day,
                                "time_slot_1": m1["time_slot"],
                                "time_slot_2": m2["time_slot"],
                                "course_1": m1["course_code"],
                                "course_2": m2["course_code"],
                                "resource": m1.get("room_name", "Unknown"),
                                "resource_id": room_id,
                                "details": f"Same room double-booked at overlapping times"
                            })

        # Check for faculty conflicts (same faculty at overlapping times)
        faculty_groups = {}
        for meeting in day_schedule:
            faculty_id = meeting.get("faculty_id")
            if faculty_id is None:
                continue
            if faculty_id not in faculty_groups:
                faculty_groups[faculty_id] = []
            faculty_groups[faculty_id].append(meeting)

        for faculty_id, meetings in faculty_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append({
                                "type": "Faculty Conflict",
                                "day": day,
                                "time_slot_1": m1["time_slot"],
                                "time_slot_2": m2["time_slot"],
                                "course_1": m1["course_code"],
                                "course_2": m2["course_code"],
                                "resource": m1.get("faculty_name", "Unknown"),
                                "resource_id": faculty_id,
                                "details": f"Same faculty assigned to overlapping classes"
                            })

    return conflicts


def save_schedule_to_text(schedule, unscheduled, filename):
    """Save schedule to a readable text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write(" " * 35 + "CLASS SCHEDULE\n")
        f.write("="*100 + "\n")
        f.write(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Scheduled Meetings: {len(schedule)}\n")
        f.write(f"Total Unscheduled Meetings: {len(unscheduled)}\n")
        f.write("="*100 + "\n\n")

        # Group by day
        for day in DAYS:
            day_schedule = [s for s in schedule if s["day"] == day]

            if not day_schedule:
                continue

            f.write("\n" + "="*100 + "\n")
            f.write(f" {day.upper()}\n")
            f.write("="*100 + "\n\n")

            # Sort by time
            day_schedule.sort(key=lambda x: x["start_hour"])

            for entry in day_schedule:
                f.write("-"*100 + "\n")
                f.write(f"Time        : {entry['time_slot']}\n")
                f.write(f"Course      : {entry['course_code']}\n")
                f.write(f"Type        : {entry['type']}\n")
                f.write(
                    f"Faculty     : {entry['faculty_name']} (ID: {entry['faculty_id']}) [{entry.get('employment_type', 'N/A')}]\n")
                f.write(
                    f"Room        : {entry['room_name']} (ID: {entry['room_id']})\n")
                f.write(f"Room Type   : {entry['room_type']}\n")
                f.write(
                    f"Capacity    : {entry['room_capacity']} (Class Size: {entry['class_size']})\n")
                f.write(f"Program ID  : {entry['program_id']}\n")
                f.write(f"Institute ID: {entry['institute_id']}\n")
                f.write(f"Class ID    : {entry['class_id']}\n")
                f.write("\n")

        # Unscheduled meetings
        if unscheduled:
            f.write("\n" + "="*100 + "\n")
            f.write(" UNSCHEDULED MEETINGS\n")
            f.write("="*100 + "\n\n")

            for entry in unscheduled:
                f.write(f"Course: {entry['course_code']} | Type: {entry['type']} | "
                        f"Hours: {entry['hours']} | Reason: {entry['reason']}\n")

    print(f"\n[INFO] Schedule saved to text file: {filename}")


def save_schedule_to_json(schedule, unscheduled, filename):
    """Save schedule to a JSON file."""
    # Count full time and part time faculty in schedule
    faculty_types = {}
    for entry in schedule:
        fid = entry.get("faculty_id")
        if fid not in faculty_types:
            faculty_types[fid] = entry.get("employment_type", "full time")

    full_time_count = sum(1 for et in faculty_types.values()
                          if et.lower() == "full time")
    part_time_count = sum(1 for et in faculty_types.values()
                          if et.lower() == "part time")

    output_data = {
        "metadata": {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_scheduled": len(schedule),
            "total_unscheduled": len(unscheduled),
            "full_time_faculty_scheduled": full_time_count,
            "part_time_faculty_scheduled": part_time_count,
            "days": DAYS,
            "start_hour": START_HOUR,
            "end_hour": END_HOUR
        },
        "scheduled_meetings": schedule,
        "unscheduled_meetings": unscheduled
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)

    print(f"[INFO] Schedule saved to JSON file: {filename}")


def save_schedule_to_excel(schedule, unscheduled, faculty_loads, filename):
    """Save schedule to an Excel file with multiple sheets."""
    wb = Workbook()

    # Remove default sheet
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    # Define styles
    header_fill = PatternFill(start_color="366092",
                              end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    subheader_fill = PatternFill(
        start_color="B4C7E7", end_color="B4C7E7", fill_type="solid")
    subheader_font = Font(bold=True, size=11)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    center_aligned = Alignment(
        horizontal='center', vertical='center', wrap_text=True)

    # ============================================================
    # SHEET 1: Schedule by Day
    # ============================================================
    ws_by_day = wb.create_sheet("Schedule by Day")

    # Headers - added Employment Type and Schedule Type
    headers = ["Day", "Time", "Course Code", "Type", "Faculty", "Employment Type", "Schedule Type", "Room", "Room Type",
               "Capacity", "Class Size", "Program ID", "Institute ID", "Class ID", "Program Code"]
    ws_by_day.append(headers)

    # Style headers
    for col_num, header in enumerate(headers, 1):
        cell = ws_by_day.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Sort schedule by day and time
    sorted_schedule = sorted(schedule, key=lambda x: (
        DAYS.index(x["day"]), x["start_hour"]))

    # Add data
    for entry in sorted_schedule:
        # Get employment type from faculty_loads
        faculty_id = entry["faculty_id"]
        employment_type = faculty_loads.get(
            faculty_id, {}).get("employment_type", "full time")

        ws_by_day.append([
            entry["day"],
            entry["time_slot"],
            entry["course_code"],
            entry["type"],
            entry["faculty_name"],
            employment_type.title(),  # Capitalize for display
            # Schedule Type
            entry.get("schedule_type", "face to face").title(),
            entry["room_name"],
            entry["room_type"],
            entry["room_capacity"],
            entry["class_size"],
            entry["program_id"],
            entry["institute_id"],
            entry["class_id"],
            entry.get("program_code", "")
        ])

    # Apply borders and auto-adjust column widths
    for row in ws_by_day.iter_rows(min_row=2, max_row=ws_by_day.max_row):
        for cell in row:
            cell.border = border
            # Numeric columns (shifted due to Schedule Type)
            if cell.column in [10, 11, 12, 13, 14]:
                cell.alignment = Alignment(horizontal='center')

        # Color code employment type
        emp_type_cell = row[5]  # Employment Type column
        if emp_type_cell.value == "Full Time":
            emp_type_cell.fill = PatternFill(
                start_color="4472C4", end_color="4472C4", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")
        else:  # Part Time
            emp_type_cell.fill = PatternFill(
                start_color="ED7D31", end_color="ED7D31", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")

        # Color code schedule type
        schedule_type_cell = row[6]  # Schedule Type column
        if schedule_type_cell.value == "Face To Face":
            schedule_type_cell.fill = PatternFill(
                start_color="70AD47", end_color="70AD47", fill_type="solid")
            schedule_type_cell.font = Font(bold=True, color="FFFFFF")
        elif schedule_type_cell.value == "Online":
            schedule_type_cell.fill = PatternFill(
                start_color="5B9BD5", end_color="5B9BD5", fill_type="solid")
            schedule_type_cell.font = Font(bold=True, color="FFFFFF")

    # Auto-adjust column widths
    for col in range(1, len(headers) + 1):
        ws_by_day.column_dimensions[get_column_letter(col)].width = 15
    ws_by_day.column_dimensions['B'].width = 20  # Time column
    ws_by_day.column_dimensions['E'].width = 25  # Faculty name
    ws_by_day.column_dimensions['F'].width = 18  # Employment Type
    ws_by_day.column_dimensions['G'].width = 16  # Schedule Type

    # ============================================================
    # SHEET 2: Schedule by Faculty
    # ============================================================
    ws_by_faculty = wb.create_sheet("Schedule by Faculty")

    # Headers - added Employment Type
    headers_faculty = ["Faculty Name", "Faculty ID", "Employment Type", "Day", "Time", "Course Code",
                       "Type", "Room", "Hours", "Class ID", "Program Code"]
    ws_by_faculty.append(headers_faculty)

    # Style headers
    for col_num, header in enumerate(headers_faculty, 1):
        cell = ws_by_faculty.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Sort by faculty name
    sorted_by_faculty = sorted(schedule, key=lambda x: (
        x["faculty_name"], DAYS.index(x["day"]), x["start_hour"]))

    # Add data
    for entry in sorted_by_faculty:
        # Get employment type from faculty_loads
        faculty_id = entry["faculty_id"]
        employment_type = faculty_loads.get(
            faculty_id, {}).get("employment_type", "full time")

        ws_by_faculty.append([
            entry["faculty_name"],
            entry["faculty_id"],
            employment_type.title(),  # Capitalize for display
            entry["day"],
            entry["time_slot"],
            entry["course_code"],
            entry["type"],
            entry["room_name"],
            entry["duration"],
            entry["class_id"],
            entry.get("program_code", "")
        ])

    # Apply styling
    for row in ws_by_faculty.iter_rows(min_row=2, max_row=ws_by_faculty.max_row):
        for cell in row:
            cell.border = border

        # Color code employment type
        emp_type_cell = row[2]  # Employment Type column
        if emp_type_cell.value == "Full Time":
            emp_type_cell.fill = PatternFill(
                start_color="4472C4", end_color="4472C4", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")
        else:  # Part Time
            emp_type_cell.fill = PatternFill(
                start_color="ED7D31", end_color="ED7D31", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")

    # Auto-adjust column widths
    for col in range(1, len(headers_faculty) + 1):
        ws_by_faculty.column_dimensions[get_column_letter(col)].width = 15
    ws_by_faculty.column_dimensions['A'].width = 25  # Faculty name
    ws_by_faculty.column_dimensions['C'].width = 18  # Employment Type
    ws_by_faculty.column_dimensions['E'].width = 20  # Time

    # ============================================================
    # SHEET 3: Schedule by Room
    # ============================================================
    ws_by_room = wb.create_sheet("Schedule by Room")

    # Headers
    headers_room = ["Room Name", "Room ID", "Room Type", "Capacity", "Day",
                    "Time", "Course Code", "Faculty", "Class ID", "Program Code"]
    ws_by_room.append(headers_room)

    # Style headers
    for col_num, header in enumerate(headers_room, 1):
        cell = ws_by_room.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Sort by room and day/time
    sorted_by_room = sorted(schedule, key=lambda x: (
        x["room_name"], DAYS.index(x["day"]), x["start_hour"]))

    # Add data
    for entry in sorted_by_room:
        ws_by_room.append([
            entry["room_name"],
            entry["room_id"],
            entry["room_type"],
            entry["room_capacity"],
            entry["day"],
            entry["time_slot"],
            entry["course_code"],
            entry["faculty_name"],
            entry["class_id"],
            entry.get("program_code", "")
        ])

    # Apply styling
    for row in ws_by_room.iter_rows(min_row=2, max_row=ws_by_room.max_row):
        for cell in row:
            cell.border = border

    # Auto-adjust column widths
    for col in range(1, len(headers_room) + 1):
        ws_by_room.column_dimensions[get_column_letter(col)].width = 15
    ws_by_room.column_dimensions['F'].width = 20  # Time
    ws_by_room.column_dimensions['H'].width = 25  # Faculty name

    # ============================================================
    # SHEET 4: Schedule by Day and Room
    # ============================================================
    ws_day_room = wb.create_sheet("Schedule by Day & Room")

    # Headers
    headers_day_room = ["Day", "Room Name", "Room Type", "Time", "Course Code",
                        "Type", "Faculty", "Class Size", "Class ID", "Program Code"]
    ws_day_room.append(headers_day_room)

    # Style headers
    for col_num, header in enumerate(headers_day_room, 1):
        cell = ws_day_room.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Sort by day, room, and time
    sorted_by_day_room = sorted(schedule, key=lambda x: (
        DAYS.index(x["day"]), x["room_name"], x["start_hour"]))

    # Add data
    for entry in sorted_by_day_room:
        ws_day_room.append([
            entry["day"],
            entry["room_name"],
            entry["room_type"],
            entry["time_slot"],
            entry["course_code"],
            entry["type"],
            entry["faculty_name"],
            entry["class_size"],
            entry["class_id"],
            entry.get("program_code", "")
        ])

    # Apply styling
    for row in ws_day_room.iter_rows(min_row=2, max_row=ws_day_room.max_row):
        for cell in row:
            cell.border = border

    # Auto-adjust column widths
    for col in range(1, len(headers_day_room) + 1):
        ws_day_room.column_dimensions[get_column_letter(col)].width = 15
    ws_day_room.column_dimensions['B'].width = 20  # Room Name
    ws_day_room.column_dimensions['D'].width = 20  # Time
    ws_day_room.column_dimensions['G'].width = 25  # Faculty name

    # ============================================================
    # SHEET 5: Faculty Load Summary
    # ============================================================
    ws_summary = wb.create_sheet("Faculty Load Summary")

    # Headers - added Employment Type and Max Load
    headers_summary = ["Faculty Name", "Faculty ID", "Employment Type", "Max Load",
                       "Total Courses", "Total Units", "Lecture Hours", "Lab Hours", "Load Status"]
    ws_summary.append(headers_summary)

    # Style headers
    for col_num, header in enumerate(headers_summary, 1):
        cell = ws_summary.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Add faculty load data
    faculty_list = []
    for fid, info in faculty_loads.items():
        num_courses = len(info["assigned_classes"])
        total_units = info["total_units"]
        employment_type = info.get("employment_type", "full time")
        load_unit = info.get("load_unit", MAX_LOAD)
        load_status = "FULL" if total_units >= load_unit else "PARTIAL" if total_units > 0 else "NONE"

        faculty_list.append([
            info["faculty_name"],
            fid,
            employment_type.title(),  # Capitalize for display
            load_unit,
            num_courses,
            round(total_units, 2),
            info["total_lecture_hours"],
            info["total_lab_hours"],
            load_status
        ])

    # Sort by faculty name
    faculty_list.sort(key=lambda x: x[0])

    # Add data
    for row_data in faculty_list:
        ws_summary.append(row_data)

    # Apply styling and conditional formatting for load status
    for row in ws_summary.iter_rows(min_row=2, max_row=ws_summary.max_row):
        for cell in row:
            cell.border = border
            if cell.column in [4, 5, 6, 7, 8]:  # Numeric columns
                cell.alignment = Alignment(horizontal='center')

        # Color code employment type
        emp_type_cell = row[2]  # Employment Type column
        if emp_type_cell.value == "Full Time":
            emp_type_cell.fill = PatternFill(
                start_color="4472C4", end_color="4472C4", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")
        else:  # Part Time
            emp_type_cell.fill = PatternFill(
                start_color="ED7D31", end_color="ED7D31", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")

        # Color code load status
        status_cell = row[8]  # Load Status column (now index 8)
        if status_cell.value == "FULL":
            status_cell.fill = PatternFill(
                start_color="00B050", end_color="00B050", fill_type="solid")
            status_cell.font = Font(bold=True, color="FFFFFF")
        elif status_cell.value == "PARTIAL":
            status_cell.fill = PatternFill(
                start_color="FFC000", end_color="FFC000", fill_type="solid")
            status_cell.font = Font(bold=True)
        else:
            status_cell.fill = PatternFill(
                start_color="FF0000", end_color="FF0000", fill_type="solid")
            status_cell.font = Font(bold=True, color="FFFFFF")

    # Auto-adjust column widths
    for col in range(1, len(headers_summary) + 1):
        ws_summary.column_dimensions[get_column_letter(col)].width = 16
    ws_summary.column_dimensions['A'].width = 25  # Faculty name
    ws_summary.column_dimensions['C'].width = 18  # Employment Type

    # ============================================================
    # SHEET 6: Unscheduled Classes
    # ============================================================
    if unscheduled:
        ws_unscheduled = wb.create_sheet("Unscheduled Classes")

        # Headers
        headers_unsch = ["Course Code", "Type", "Hours", "Class ID", "Reason"]
        ws_unscheduled.append(headers_unsch)

        # Style headers
        for col_num, header in enumerate(headers_unsch, 1):
            cell = ws_unscheduled.cell(1, col_num)
            cell.font = header_font
            cell.fill = PatternFill(
                start_color="C00000", end_color="C00000", fill_type="solid")
            cell.alignment = center_aligned
            cell.border = border

        # Add unscheduled data
        for entry in unscheduled:
            ws_unscheduled.append([
                entry["course_code"],
                entry["type"],
                entry["hours"],
                entry["class_id"],
                entry["reason"]
            ])

        # Apply styling
        for row in ws_unscheduled.iter_rows(min_row=2, max_row=ws_unscheduled.max_row):
            for cell in row:
                cell.border = border

        # Auto-adjust column widths
        ws_unscheduled.column_dimensions['A'].width = 15
        ws_unscheduled.column_dimensions['B'].width = 12
        ws_unscheduled.column_dimensions['C'].width = 10
        ws_unscheduled.column_dimensions['D'].width = 12
        ws_unscheduled.column_dimensions['E'].width = 40

    # ============================================================
    # SHEET 7: Schedule Conflicts
    # ============================================================
    # Detect conflicts using validate_schedule_detailed
    conflicts_data = validate_schedule_detailed(schedule)

    ws_conflicts = wb.create_sheet("Schedule Conflicts")

    # Headers
    headers_conflicts = ["Conflict Type", "Day", "Time Slot 1", "Time Slot 2", "Course 1", "Course 2",
                         "Resource", "Resource ID", "Details"]
    ws_conflicts.append(headers_conflicts)

    # Style headers
    conflict_header_fill = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
    for col_num, header in enumerate(headers_conflicts, 1):
        cell = ws_conflicts.cell(1, col_num)
        cell.font = header_font
        cell.fill = conflict_header_fill
        cell.alignment = center_aligned
        cell.border = border

    if conflicts_data:
        # Add conflict data
        for conflict in conflicts_data:
            ws_conflicts.append([
                conflict["type"],
                conflict["day"],
                conflict["time_slot_1"],
                conflict["time_slot_2"],
                conflict["course_1"],
                conflict["course_2"],
                conflict["resource"],
                conflict["resource_id"],
                conflict["details"]
            ])

        # Apply styling
        for row in ws_conflicts.iter_rows(min_row=2, max_row=ws_conflicts.max_row):
            for cell in row:
                cell.border = border

            # Color code conflict type
            conflict_type_cell = row[0]
            if "Room" in str(conflict_type_cell.value):
                conflict_type_cell.fill = PatternFill(
                    start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")
                conflict_type_cell.font = Font(bold=True)
            elif "Class" in str(conflict_type_cell.value):
                conflict_type_cell.fill = PatternFill(
                    start_color="FFB347", end_color="FFB347", fill_type="solid")
                conflict_type_cell.font = Font(bold=True)
            elif "Faculty" in str(conflict_type_cell.value):
                conflict_type_cell.fill = PatternFill(
                    start_color="77DD77", end_color="77DD77", fill_type="solid")
                conflict_type_cell.font = Font(bold=True)
    else:
        # No conflicts - add a message
        ws_conflicts.append(["No conflicts detected", "", "", "", "", "", "", "", "Schedule is conflict-free!"])
        cell = ws_conflicts.cell(2, 1)
        cell.fill = PatternFill(start_color="00B050", end_color="00B050", fill_type="solid")
        cell.font = Font(bold=True, color="FFFFFF")

    # Auto-adjust column widths
    ws_conflicts.column_dimensions['A'].width = 15  # Conflict Type
    ws_conflicts.column_dimensions['B'].width = 12  # Day
    ws_conflicts.column_dimensions['C'].width = 18  # Time Slot 1
    ws_conflicts.column_dimensions['D'].width = 18  # Time Slot 2
    ws_conflicts.column_dimensions['E'].width = 15  # Course 1
    ws_conflicts.column_dimensions['F'].width = 15  # Course 2
    ws_conflicts.column_dimensions['G'].width = 20  # Resource
    ws_conflicts.column_dimensions['H'].width = 12  # Resource ID
    ws_conflicts.column_dimensions['I'].width = 40  # Details

    # Save workbook
    wb.save(filename)
    print(f"[INFO] Schedule saved to Excel file: {filename}")


# ===========================================================   =
# START CODE FOR FACULTY aSSIGNING TO CLASSES
# ============================================================
def fetch_table_data(table: Table) -> List[Dict]:
    """
    Fetch all rows from a given SQLAlchemy Table and return as a list of dictionaries.
    """
    with engine.connect() as conn:
        result = conn.execute(select(table))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]


# ============================================================
# FACULTY LOAD CALCULATION FUNCTIONS
# ============================================================

MAX_LOAD = 18  # maximum faculty load units


def compute_load(lec_units, lab_units):
    """
    Compute teacher load units from student lecture and lab units.
    Based on the formula:
    - Lecture: 1 student unit = 1 hour = 1 teacher unit
    - Laboratory: 1 student unit = 3 hours × 0.75/hour = 2.25 teacher units

    lec_units: student lecture units
    lab_units: student laboratory units
    Returns total teacher units for faculty loading
    """
    teacher_lec_units = lec_units * LECTURE_STUDENT_UNIT_TO_TEACHER_UNIT
    teacher_lab_units = lab_units * LAB_STUDENT_UNIT_TO_TEACHER_UNIT
    return teacher_lec_units + teacher_lab_units


def matches_expertise(course, faculty_course):
    """
    Check if faculty expertise matches a class.
    Must match: course_code AND program_id.
    """
    return (
        faculty_course["course_code"] == course["course_code"]
        and faculty_course["program_id"] == course["program_id"]
    )


def assign_faculty(classes_courses, faculty_expertise_courses):
    """
    Assign classes to faculty based on matching expertise and load limit.
    Uses load_unit from faculty data (18 for full time, 9 for part time).
    """

    # Prepare load tracking structure
    faculty_loads = {}

    for f in faculty_expertise_courses:
        fid = f["faculty_id"]
        # Only set if not already set (avoid overwriting with duplicate entries)
        if fid not in faculty_loads:
            faculty_loads[fid] = {
                "faculty_name": f["faculty_name"],
                "employment_type": f.get("employment_type", "full time"),
                # Use faculty's load_unit or default to MAX_LOAD
                "load_unit": f.get("load_unit", MAX_LOAD),
                "preferred_time": parse_preferred_time(f.get("preffered_time", "")),
                "assigned_classes": [],
                "total_units": 0,
                "total_lecture_hours": 0,
                "total_lab_hours": 0,
            }

    # Assign classes
    for course in classes_courses:
        assigned = False

        for faculty in faculty_expertise_courses:

            # Skip faculty without expertise rows
            if faculty["course_code"] is None:
                continue

            # Check if faculty expertise matches class
            if matches_expertise(course, faculty):

                units = compute_load(
                    course["course_lec"], course["course_lab"])
                fid = faculty["faculty_id"]

                # Get faculty's specific load limit (18 for full time, 9 for part time)
                faculty_max_load = faculty_loads[fid]["load_unit"]

                # Check if load limit allows assignment
                if faculty_loads[fid]["total_units"] + units <= faculty_max_load:

                    faculty_loads[fid]["assigned_classes"].append(course)
                    faculty_loads[fid]["total_units"] += units
                    faculty_loads[fid]["total_lecture_hours"] += course["course_lec"]
                    faculty_loads[fid]["total_lab_hours"] += course["course_lab"]

                    assigned = True
                    break

        if not assigned:
            print(
                f"[WARNING] No qualified faculty found for course: {course['course_code']}")

    return faculty_loads


def save_faculty_load_to_text(faculty_loads: Dict, filename: str):
    """
    Save faculty loading results to a plain text file in a readable format.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(" " * 25 + "FACULTY LOAD ASSIGNMENTS\n")
        f.write("=" * 80 + "\n")
        f.write(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Full Time Max Load: 18 units | Part Time Max Load: 9 units\n")
        f.write("=" * 80 + "\n\n")

        # Faculty with assignments
        for fid, info in faculty_loads.items():
            if len(info["assigned_classes"]) == 0:
                continue

            employment_type = info.get("employment_type", "full time").title()
            load_unit = info.get("load_unit", MAX_LOAD)

            f.write("-" * 80 + "\n")
            f.write(f"Faculty: {info['faculty_name']} (ID: {fid})\n")
            f.write(
                f"Employment Type: {employment_type} | Max Load: {load_unit} units\n")
            f.write("-" * 80 + "\n")
            f.write(
                f"Total Units Load      : {info['total_units']:.2f} / {load_unit} units\n")
            f.write(
                f"Total Lecture Hours   : {info['total_lecture_hours']} hours\n")
            f.write(
                f"Total Laboratory Hours: {info['total_lab_hours']} hours\n")
            f.write(
                f"Number of Classes     : {len(info['assigned_classes'])}\n\n")
            f.write("Assigned Classes:\n")

            for idx, cls in enumerate(info["assigned_classes"], 1):
                units = compute_load(cls['course_lec'], cls['course_lab'])
                f.write(f"  {idx}. Course Code   : {cls['course_code']}\n")
                f.write(f"     Class ID      : {cls['class_id']}\n")
                f.write(f"     Program ID    : {cls['program_id']}\n")
                f.write(f"     Lecture Hours : {cls['course_lec']}\n")
                f.write(f"     Lab Hours     : {cls['course_lab']}\n")
                f.write(f"     Units Load    : {units:.2f}\n\n")

            f.write("\n")

        # Summary section
        f.write("\n" + "=" * 80 + "\n")
        f.write(" " * 30 + "SUMMARY REPORT\n")
        f.write("=" * 80 + "\n\n")

        total_faculty_with_loads = 0
        total_faculty_without_loads = 0
        total_full_time = 0
        total_part_time = 0

        for fid, info in faculty_loads.items():
            num_courses = len(info["assigned_classes"])
            total_units = info["total_units"]
            employment_type = info.get("employment_type", "full time")
            load_unit = info.get("load_unit", MAX_LOAD)

            if num_courses > 0:
                total_faculty_with_loads += 1
                if employment_type.lower() == "full time":
                    total_full_time += 1
                else:
                    total_part_time += 1
                load_status = "FULL" if total_units >= load_unit else "PARTIAL"
                emp_short = "FT" if employment_type.lower() == "full time" else "PT"
                f.write(
                    f"{info['faculty_name']:<35} | {emp_short} | {num_courses:>2} courses | {total_units:>5.2f}/{load_unit:>2} units | {load_status}\n")
            else:
                total_faculty_without_loads += 1

        f.write("\n" + "-" * 80 + "\n")
        f.write(
            f"Total Faculty with Assignments   : {total_faculty_with_loads}\n")
        f.write(f"  - Full Time Faculty            : {total_full_time}\n")
        f.write(f"  - Part Time Faculty            : {total_part_time}\n")
        f.write(
            f"Total Faculty without Assignments: {total_faculty_without_loads}\n")
        f.write("=" * 80 + "\n")

    print(f"\n[INFO] Faculty load saved to text file: {filename}")


def save_faculty_load_to_json(faculty_loads: Dict, filename: str):
    """
    Save faculty loading results to a JSON file.
    """
    # Prepare JSON-serializable data
    output_data = {
        "metadata": {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "full_time_max_load": 18,
            "part_time_max_load": 9,
            "total_faculty": len(faculty_loads),
            "faculty_with_assignments": sum(1 for info in faculty_loads.values() if len(info["assigned_classes"]) > 0),
            "faculty_without_assignments": sum(1 for info in faculty_loads.values() if len(info["assigned_classes"]) == 0),
            "full_time_faculty": sum(1 for info in faculty_loads.values() if info.get("employment_type", "full time").lower() == "full time" and len(info["assigned_classes"]) > 0),
            "part_time_faculty": sum(1 for info in faculty_loads.values() if info.get("employment_type", "full time").lower() == "part time" and len(info["assigned_classes"]) > 0)
        },
        "faculty_loads": []
    }

    for fid, info in faculty_loads.items():
        employment_type = info.get("employment_type", "full time")
        load_unit = info.get("load_unit", MAX_LOAD)

        faculty_entry = {
            "faculty_id": fid,
            "faculty_name": info["faculty_name"],
            "employment_type": employment_type,
            "max_load_unit": load_unit,
            "total_units": round(info["total_units"], 2),
            "total_lecture_hours": info["total_lecture_hours"],
            "total_lab_hours": info["total_lab_hours"],
            "number_of_classes": len(info["assigned_classes"]),
            "load_status": "FULL" if info["total_units"] >= load_unit else "PARTIAL" if info["total_units"] > 0 else "NONE",
            "assigned_classes": []
        }

        for cls in info["assigned_classes"]:
            class_entry = {
                "class_id": cls["class_id"],
                "course_code": cls["course_code"],
                "program_id": cls["program_id"],
                "institute_id": cls.get("institute_id", None),
                "lecture_hours": cls["course_lec"],
                "lab_hours": cls["course_lab"],
                "units_load": round(compute_load(cls["course_lec"], cls["course_lab"]), 2)
            }
            faculty_entry["assigned_classes"].append(class_entry)

        output_data["faculty_loads"].append(faculty_entry)

    # Sort by faculty name
    output_data["faculty_loads"].sort(key=lambda x: x["faculty_name"])

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)

    print(f"[INFO] Faculty load saved to JSON file: {filename}")
# ============================================================
# MAIN SCRIPT
# ============================================================


if __name__ == "__main__":

    # ------------------------------------------
    # LOAD DATA FROM DATABASE
    # ------------------------------------------
    classes_course_table = Table(
        "classes_course", metadata, autoload_with=engine
    )
    faculty_expertise_courses_table = Table(
        "faculty_expertise_courses", metadata, autoload_with=engine
    )
    rooms_table = Table(
        "rooms", metadata, autoload_with=engine
    )
    programs_table = Table(
        "programs", metadata, autoload_with=engine
    )
    classes_table = Table(
        "classes", metadata, autoload_with=engine
    )

    classes_course = fetch_table_data(classes_course_table)
    faculty_expertise_courses = fetch_table_data(
        faculty_expertise_courses_table
    )
    rooms = fetch_table_data(rooms_table)
    programs = fetch_table_data(programs_table)
    classes = fetch_table_data(classes_table)

    # Build program_id -> program_code lookup map
    program_map = {p["program_id"]: p["program_code"] for p in programs}

    # Build class_id -> class_size lookup map
    class_size_map = {c["class_id"]: c["class_size"] for c in classes}

    # Enrich classes_course with program_code and class_size
    for cls in classes_course:
        cls["program_code"] = program_map.get(cls.get("program_id"), "Unknown")
        cls["class_size"] = class_size_map.get(cls.get("class_id"), 0)

    # ------------------------------------------
    # APPLY FACULTY LOAD ASSIGNMENT
    # ------------------------------------------
    faculty_load_result = assign_faculty(
        classes_course,
        faculty_expertise_courses
    )

    # ------------------------------------------
    # CREATE ROOM AND TIME SCHEDULE
    # ------------------------------------------
    complete_schedule, unscheduled_meetings = create_schedule(
        faculty_load_result,
        rooms
    )
 # Save schedule to Excel file
 
    # Generate timestamp for filenames
    # Create output directory if it doesn't exist
    output_dir = "faculty_loading_output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    schedule_excel_filename = os.path.join(
        output_dir, f"scheduleeeessseee_{timestamp}.xlsx")
    save_schedule_to_excel(complete_schedule, unscheduled_meetings,
                           faculty_load_result, schedule_excel_filename)

 # Save schedule to Excel file
 
    # Generate timestamp for filenames
    # Create output directory if it doesn't exist
    output_dir = "faculty_loading_output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    schedule_excel_filename = os.path.join(
        output_dir, f"scheduleeeessseeejsonnnnn_{timestamp}.json")
    save_schedule_to_json(complete_schedule, unscheduled_meetings, schedule_excel_filename)

    # ------------------------------------------
    # FINAL OUTPUT (FOR NESTJS)
    # ------------------------------------------
    output = {
        "scheduled_meetings": complete_schedule,
        "unscheduled_meetings": unscheduled_meetings
    }

    # IMPORTANT: markers help NestJS safely parse stdout
    print("===JSON_START===")
    print(json.dumps(output, indent=2, default=str))
    print("===JSON_END===")
