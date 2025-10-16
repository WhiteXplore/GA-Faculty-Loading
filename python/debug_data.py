#!/usr/bin/env python3
"""
Debug script to check why schedules are empty
"""
from sqlalchemy import create_engine, Table, MetaData, select
import json

DB_USER = "root"
DB_PASS = "root"
DB_HOST = "127.0.0.2"
DB_PORT = 3306
DB_NAME = "dnsc_class_scheduler_ga"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
    echo=False,
)
metadata = MetaData()

# Load tables
assigned_set_courses_table = Table("assigned_set_courses", metadata, autoload_with=engine)
courses_table = Table("course_view", metadata, autoload_with=engine)
faculty_expertise_table = Table("faculty_expertise", metadata, autoload_with=engine)
faculty_table = Table("faculty", metadata, autoload_with=engine)
rooms_table = Table("rooms", metadata, autoload_with=engine)

def fetch_table_data(table):
    try:
        with engine.connect() as conn:
            return [dict(row._mapping) for row in conn.execute(select(table))]
    except Exception as e:
        print(f"Failed to load {table.name}:", e)
        return []

print("\n" + "="*80)
print("DATABASE DATA ANALYSIS")
print("="*80)

# Check assigned_set_courses
assigned_set_courses = fetch_table_data(assigned_set_courses_table)
print(f"\n1. ASSIGNED SET COURSES: {len(assigned_set_courses)} records")
if assigned_set_courses:
    sets = set(a.get("set") for a in assigned_set_courses)
    print(f"   Sets found: {sorted(sets)}")
    for s in sorted(sets):
        count = len([a for a in assigned_set_courses if a.get("set") == s])
        print(f"   - Set '{s}': {count} courses")
    print(f"\n   Sample data:")
    print(json.dumps(assigned_set_courses[:3], indent=2, default=str))
else:
    print("   ⚠️  WARNING: No data in assigned_set_courses table!")

# Check courses
courses = fetch_table_data(courses_table)
print(f"\n2. COURSES: {len(courses)} records")
if courses:
    print(f"   Sample course:")
    sample = courses[0]
    print(f"   - course_id: {sample.get('course_id')}")
    print(f"   - course_code: {sample.get('course_code')}")
    print(f"   - course_lec: {sample.get('course_lec')}")
    print(f"   - course_lab: {sample.get('course_lab')}")
    print(f"   - Fields available: {list(sample.keys())}")
else:
    print("   ⚠️  WARNING: No courses found!")

# Check faculty expertise
faculty_expertise = fetch_table_data(faculty_expertise_table)
print(f"\n3. FACULTY EXPERTISE: {len(faculty_expertise)} records")
if faculty_expertise:
    print(f"   Sample data:")
    print(json.dumps(faculty_expertise[:3], indent=2, default=str))
else:
    print("   ⚠️  WARNING: No faculty expertise data!")

# Check faculty
faculty = fetch_table_data(faculty_table)
print(f"\n4. FACULTY: {len(faculty)} records")
if faculty:
    print(f"   Sample faculty:")
    sample = faculty[0]
    print(f"   - faculty_id: {sample.get('faculty_id')}")
    print(f"   - name: {sample.get('name') or sample.get('first_name')}")
else:
    print("   ⚠️  WARNING: No faculty found!")

# Check rooms
rooms = fetch_table_data(rooms_table)
print(f"\n5. ROOMS: {len(rooms)} records")
if rooms:
    for room in rooms:
        print(f"   - ID {room.get('room_id')}: {room.get('room_name')} ({room.get('room_type')})")
else:
    print("   ⚠️  WARNING: No rooms found!")

# Cross-reference check
print("\n" + "="*80)
print("CROSS-REFERENCE CHECK")
print("="*80)

if assigned_set_courses and courses:
    assigned_course_ids = set(a.get('course_id') for a in assigned_set_courses)
    course_ids = set(c.get('course_id') for c in courses)
    print(f"\nAssigned course IDs: {assigned_course_ids}")
    print(f"Available course IDs: {course_ids}")
    matched = assigned_course_ids & course_ids
    print(f"Matched courses: {matched}")
    if not matched:
        print("⚠️  WARNING: No matching courses between assigned_set_courses and courses!")

if assigned_set_courses and faculty_expertise:
    assigned_course_ids = set(a.get('course_id') for a in assigned_set_courses)
    expertise_course_ids = set(e.get('course_id') for e in faculty_expertise)
    print(f"\nCourses needing faculty: {assigned_course_ids}")
    print(f"Courses with faculty expertise: {expertise_course_ids}")
    matched = assigned_course_ids & expertise_course_ids
    print(f"Courses with assigned faculty: {matched}")
    if not matched:
        print("⚠️  WARNING: No faculty expertise for assigned courses!")

print("\n" + "="*80)


