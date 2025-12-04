import random
import json
import os
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


# ===========================================================   =
# START CODE FOR SCHEDULING FUNCTIONS
# ============================================================

# ============================================================
# SCHEDULING FUNCTIONS
# ============================================================

# Time slot configuration
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
START_HOUR = 8  # 8 AM
END_HOUR = 21   # 9 PM
LUNCH_START = 12
LUNCH_END = 13
MAX_CAPACITY_EXCESS = 5  # Allow up to 5 students over capacity


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
    """Format time slot as string."""
    end_hour = start_hour + duration
    return f"{time_to_string(start_hour)} - {time_to_string(end_hour)}"


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


def schedule_class_meeting(cls, course_type, hours, rooms, faculty_id,
                           schedule_tracker, faculty_schedule_tracker,
                           unscheduled_meetings):
    """
    Try to schedule a single meeting (lecture or laboratory).
    Returns scheduled meeting dict if successful, None otherwise.
    """
    institute_id = cls.get("institute_id")
    class_size = cls.get("class_size", 30)  # Default to 30 if not specified

    # Try each day
    for day in DAYS:
        # Find available time slots for this duration
        available_slots = find_available_slots(START_HOUR, END_HOUR, hours)

        # Try each time slot
        for start_hour in available_slots:
            # Check faculty availability
            if not is_faculty_available(faculty_id, day, start_hour, hours,
                                        faculty_schedule_tracker):
                continue

            # Find suitable room
            room = find_suitable_room(rooms, course_type, institute_id, class_size,
                                      day, start_hour, hours, schedule_tracker)

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
        "type": course_type,
        "hours": hours,
        "reason": "No available room/time slot found"
    })

    return None


def create_schedule(faculty_loads, rooms):
    """
    Create a complete schedule for all faculty loads.
    Returns scheduled classes and unscheduled meetings.
    """
    schedule_tracker = {}  # Track room schedules
    faculty_schedule_tracker = {}  # Track faculty schedules
    complete_schedule = []
    unscheduled_meetings = []

    print("\n" + "="*80)
    print(" " * 25 + "STARTING SCHEDULING PROCESS")
    print("="*80)

    # Process each faculty's assigned classes
    for faculty_id, faculty_info in faculty_loads.items():
        faculty_name = faculty_info["faculty_name"]

        if len(faculty_info["assigned_classes"]) == 0:
            continue

        print(f"\nScheduling classes for: {faculty_name} (ID: {faculty_id})")

        for cls in faculty_info["assigned_classes"]:
            lecture_hours = cls.get("course_lec", 0)
            lab_hours = cls.get("course_lab", 0)

            # Schedule lecture if needed
            if lecture_hours > 0:
                print(
                    f"  Scheduling LECTURE for {cls['course_code']} ({lecture_hours}h)...", end=" ")
                lecture_schedule = schedule_class_meeting(
                    cls, "Lecture", lecture_hours, rooms, faculty_id,
                    schedule_tracker, faculty_schedule_tracker, unscheduled_meetings
                )

                if lecture_schedule:
                    lecture_schedule["faculty_id"] = faculty_id
                    lecture_schedule["faculty_name"] = faculty_name
                    complete_schedule.append(lecture_schedule)
                    print("✓ Scheduled")
                else:
                    print("✗ Failed")

          # Schedule laboratory if needed
            if lab_hours > 0:
                # Convert lab units to contact hours (1 unit = 3 contact hours)
                lab_contact_hours = lab_hours * 3
                print(
                    f"  Scheduling LABORATORY for {cls['course_code']} ({lab_hours} unit{'s' if lab_hours != 1 else ''} = {lab_contact_hours}h)...", end=" ")
                lab_schedule = schedule_class_meeting(
                    cls, "Laboratory", lab_contact_hours, rooms, faculty_id,
                    schedule_tracker, faculty_schedule_tracker, unscheduled_meetings
                )

                if lab_schedule:
                    lab_schedule["faculty_id"] = faculty_id
                    lab_schedule["faculty_name"] = faculty_name
                    complete_schedule.append(lab_schedule)
                    print("✓ Scheduled")
                else:
                    print("✗ Failed")

    print("\n" + "="*80)
    print(f"Scheduling Complete: {len(complete_schedule)} meetings scheduled, "
          f"{len(unscheduled_meetings)} unscheduled")
    print("="*80)

    return complete_schedule, unscheduled_meetings


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
                    f"Faculty     : {entry['faculty_name']} (ID: {entry['faculty_id']})\n")
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
    output_data = {
        "metadata": {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_scheduled": len(schedule),
            "total_unscheduled": len(unscheduled),
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

    # Headers
    headers = ["Day", "Time", "Course Code", "Type", "Faculty", "Room", "Room Type",
               "Capacity", "Class Size", "Program ID", "Institute ID", "Class ID"]
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
        ws_by_day.append([
            entry["day"],
            entry["time_slot"],
            entry["course_code"],
            entry["type"],
            entry["faculty_name"],
            entry["room_name"],
            entry["room_type"],
            entry["room_capacity"],
            entry["class_size"],
            entry["program_id"],
            entry["institute_id"],
            entry["class_id"]
        ])

    # Apply borders and auto-adjust column widths
    for row in ws_by_day.iter_rows(min_row=2, max_row=ws_by_day.max_row):
        for cell in row:
            cell.border = border
            if cell.column in [8, 9, 10, 11, 12]:  # Numeric columns
                cell.alignment = Alignment(horizontal='center')

    # Auto-adjust column widths
    for col in range(1, len(headers) + 1):
        ws_by_day.column_dimensions[get_column_letter(col)].width = 15
    ws_by_day.column_dimensions['B'].width = 20  # Time column
    ws_by_day.column_dimensions['E'].width = 25  # Faculty name

    # ============================================================
    # SHEET 2: Schedule by Faculty
    # ============================================================
    ws_by_faculty = wb.create_sheet("Schedule by Faculty")

    # Headers
    headers_faculty = ["Faculty Name", "Faculty ID", "Day", "Time", "Course Code",
                       "Type", "Room", "Hours", "Class ID"]
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
        ws_by_faculty.append([
            entry["faculty_name"],
            entry["faculty_id"],
            entry["day"],
            entry["time_slot"],
            entry["course_code"],
            entry["type"],
            entry["room_name"],
            entry["duration"],
            entry["class_id"]
        ])

    # Apply styling
    for row in ws_by_faculty.iter_rows(min_row=2, max_row=ws_by_faculty.max_row):
        for cell in row:
            cell.border = border

    # Auto-adjust column widths
    for col in range(1, len(headers_faculty) + 1):
        ws_by_faculty.column_dimensions[get_column_letter(col)].width = 15
    ws_by_faculty.column_dimensions['A'].width = 25  # Faculty name
    ws_by_faculty.column_dimensions['D'].width = 20  # Time

    # ============================================================
    # SHEET 3: Schedule by Room
    # ============================================================
    ws_by_room = wb.create_sheet("Schedule by Room")

    # Headers
    headers_room = ["Room Name", "Room ID", "Room Type", "Capacity", "Day",
                    "Time", "Course Code", "Faculty", "Class ID"]
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
            entry["class_id"]
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
    # SHEET 4: Faculty Load Summary
    # ============================================================
    ws_summary = wb.create_sheet("Faculty Load Summary")

    # Headers
    headers_summary = ["Faculty Name", "Faculty ID", "Total Courses", "Total Units",
                       "Lecture Hours", "Lab Hours", "Load Status"]
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
        load_status = "FULL" if total_units >= MAX_LOAD else "PARTIAL" if total_units > 0 else "NONE"

        faculty_list.append([
            info["faculty_name"],
            fid,
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
            if cell.column in [3, 4, 5, 6]:  # Numeric columns
                cell.alignment = Alignment(horizontal='center')

        # Color code load status
        status_cell = row[6]  # Load Status column
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
        ws_summary.column_dimensions[get_column_letter(col)].width = 18
    ws_summary.column_dimensions['A'].width = 25  # Faculty name

    # ============================================================
    # SHEET 5: Unscheduled Classes
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


def compute_load(lec, lab):
    """Compute load units: 1 per lec hour, 1/3 per lab hour."""
    return lec + (lab / 3)


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
    """

    # Prepare load tracking structure
    faculty_loads = {}

    for f in faculty_expertise_courses:
        faculty_loads[f["faculty_id"]] = {
            "faculty_name": f["faculty_name"],
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

                # Check if load limit allows assignment
                if faculty_loads[faculty["faculty_id"]]["total_units"] + units <= MAX_LOAD:

                    faculty_loads[faculty["faculty_id"]
                                  ]["assigned_classes"].append(course)
                    faculty_loads[faculty["faculty_id"]
                                  ]["total_units"] += units
                    faculty_loads[faculty["faculty_id"]
                                  ]["total_lecture_hours"] += course["course_lec"]
                    faculty_loads[faculty["faculty_id"]
                                  ]["total_lab_hours"] += course["course_lab"]

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
        f.write(f"Maximum Load per Faculty: {MAX_LOAD} units\n")
        f.write("=" * 80 + "\n\n")

        # Faculty with assignments
        for fid, info in faculty_loads.items():
            if len(info["assigned_classes"]) == 0:
                continue

            f.write("-" * 80 + "\n")
            f.write(f"Faculty: {info['faculty_name']} (ID: {fid})\n")
            f.write("-" * 80 + "\n")
            f.write(
                f"Total Units Load      : {info['total_units']:.2f} units\n")
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

        for fid, info in faculty_loads.items():
            num_courses = len(info["assigned_classes"])
            total_units = info["total_units"]

            if num_courses > 0:
                total_faculty_with_loads += 1
                load_status = "FULL" if total_units >= MAX_LOAD else "PARTIAL"
                f.write(
                    f"{info['faculty_name']:<40} | {num_courses:>2} courses | {total_units:>6.2f} units | {load_status}\n")
            else:
                total_faculty_without_loads += 1

        f.write("\n" + "-" * 80 + "\n")
        f.write(
            f"Total Faculty with Assignments   : {total_faculty_with_loads}\n")
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
            "max_load": MAX_LOAD,
            "total_faculty": len(faculty_loads),
            "faculty_with_assignments": sum(1 for info in faculty_loads.values() if len(info["assigned_classes"]) > 0),
            "faculty_without_assignments": sum(1 for info in faculty_loads.values() if len(info["assigned_classes"]) == 0)
        },
        "faculty_loads": []
    }

    for fid, info in faculty_loads.items():
        faculty_entry = {
            "faculty_id": fid,
            "faculty_name": info["faculty_name"],
            "total_units": round(info["total_units"], 2),
            "total_lecture_hours": info["total_lecture_hours"],
            "total_lab_hours": info["total_lab_hours"],
            "number_of_classes": len(info["assigned_classes"]),
            "load_status": "FULL" if info["total_units"] >= MAX_LOAD else "PARTIAL" if info["total_units"] > 0 else "NONE",
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

    # Load your data from database
    classes_course_table = Table(
        "classes_course", metadata, autoload_with=engine)
    faculty_expertise_courses_table = Table(
        "faculty_expertise_courses", metadata, autoload_with=engine)
    rooms_table = Table("rooms", metadata, autoload_with=engine)

    classes_course = fetch_table_data(classes_course_table)
    faculty_expertise_courses = fetch_table_data(
        faculty_expertise_courses_table)
    rooms = fetch_table_data(rooms_table)

    print("\nLoaded rooms data:")
    print(json.dumps(rooms, indent=2, default=str))
    print("\nLoaded classes_course:")
    # preview only
    print(json.dumps(classes_course[:5], indent=2, default=str))

    print("\nLoaded faculty_expertise:")
    # preview only
    print(json.dumps(faculty_expertise_courses[:5], indent=2, default=str))

    # ------------------------------------------
    # APPLY FACULTY LOAD ASSIGNMENT
    # ------------------------------------------
    faculty_load_result = assign_faculty(
        classes_course, faculty_expertise_courses)
    print("\nLoaded faculty_expertise:")
    print(faculty_load_result)  # preview only
    # ==================================================================
    # ENHANCED DEBUGGING FOR ROOM MATCHING
    # ==================================================================
    print("\n" + "="*80)
    print("DEBUGGING: ROOM DATA ANALYSIS")
    print("="*80)
    print(f"Total rooms loaded: {len(rooms)}")

    if rooms:
        print("\n--- First 3 Rooms Sample ---")
        for i, room in enumerate(rooms[:3]):
            print(f"\nRoom {i+1}:")
            for key, value in room.items():
                print(f"  {key}: {value}")

        # Analyze room types
        room_types = {}
        for room in rooms:
            rt = room.get("room_type")
            room_types[rt] = room_types.get(rt, 0) + 1

        print(f"\n--- Room Types Distribution ---")
        for rt, count in room_types.items():
            print(f"  '{rt}': {count} rooms")

        # Analyze institutes
        room_institutes = {}
        for room in rooms:
            ri = room.get("institute_id")
            room_institutes[ri] = room_institutes.get(ri, 0) + 1

        print(f"\n--- Room Institute Distribution ---")
        for ri, count in sorted(room_institutes.items()):
            print(f"  Institute {ri}: {count} rooms")

    print("\n" + "="*80)
    print("DEBUGGING: CLASS DATA ANALYSIS")
    print("="*80)

    # ------------------------------------------
    # CREATE ROOM AND TIME SCHEDULE
    # ------------------------------------------
    print("\n" + "="*80)
    print("Starting schedule generation...")
    print("="*80)

    complete_schedule, unscheduled_meetings = create_schedule(
        faculty_load_result, rooms)
    print("\nLoaded faculty_expertise:")
    print(complete_schedule, unscheduled_meetings)
    print("\nLoaded faculty_expertise:yyyyyyyyyyyyyyyyyyyy")
    # preview only
    # ------------------------------------------
    # DISPLAY SCHEDULE SUMMARY
    # ------------------------------------------
    print("\n" + "="*80)
    print(" SCHEDULE SUMMARY BY DAY")
    print("="*80)

    for day in DAYS:
        day_schedule = [s for s in complete_schedule if s["day"] == day]
        print(f"\n{day}: {len(day_schedule)} meetings scheduled")

    # ------------------------------------------
    # SAVE TO FILES
    # ------------------------------------------

    # Create output directory if it doesn't exist
    output_dir = "faculty_loading_output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate timestamp for filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # # Save faculty loading to text file
    # text_filename = os.path.join(output_dir, f"faculty_loading_{timestamp}.txt")
    # save_faculty_load_to_text(faculty_load_result, text_filename)

    # # Save faculty loading to JSON file
    # json_filename = os.path.join(output_dir, f"faculty_loading_{timestamp}.json")
    # save_faculty_load_to_json(faculty_load_result, json_filename)

    # # Save schedule to text file
    # schedule_text_filename = os.path.join(output_dir, f"schedule_{timestamp}.txt")
    # save_schedule_to_text(complete_schedule, unscheduled_meetings, schedule_text_filename)

    # Save schedule to JSON file
    schedule_json_filename = os.path.join(
        output_dir, f"schedule_{timestamp}.json")
    save_schedule_to_json(
        complete_schedule, unscheduled_meetings, schedule_json_filename)

    # Save schedule to Excel file
    schedule_excel_filename = os.path.join(
        output_dir, f"schedule_{timestamp}.xlsx")
    save_schedule_to_excel(complete_schedule, unscheduled_meetings,
                           faculty_load_result, schedule_excel_filename)
    total_meetings = len(complete_schedule)
    print(f"Total meetings scheduled: {total_meetings}")
    print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")

    print(f"\n{'='*80}")
    print("✓ Faculty loading and scheduling completed successfully!")
    print(f"✓ Files saved in '{output_dir}/' directory:")
    # print(f"  - {text_filename}")
    # print(f"  - {json_filename}")
    # print(f"  - {schedule_text_filename}")
    # print(f"  - {schedule_json_filename}")
    print(f"{'='*80}")
