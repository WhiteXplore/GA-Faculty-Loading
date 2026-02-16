"""
Sample Hardcoded Input Data for Faculty Loading Algorithm

This file contains sample data structures that can be used to test the
faculty_loading_jhomel.py algorithm without requiring a database connection.

To use this data, replace the database fetch calls in the main script with:
    classes_course = SAMPLE_CLASSES_COURSE
    faculty_expertise_courses = SAMPLE_FACULTY_EXPERTISE_COURSES
    rooms = SAMPLE_ROOMS
"""

# ============================================================================
# SAMPLE CLASSES_COURSE DATA
# ============================================================================
# Structure: List of dictionaries, each representing a class/course to be scheduled
# Required fields: class_id, course_code, course_lec, course_lab, program_id, 
#                  institute_id, class_size, set_name, course_level

SAMPLE_CLASSES_COURSE = [
    # Main branch - more data
    {
        "class_id": 1,
        "course_code": "CS101",
        "course_lec": 3,          # 3 lecture hours per week
        "course_lab": 2,          # 2 lab units per week
        "program_id": 1,          # Computer Science Program
        "institute_id": 1,        # Institute of Technology
        "class_size": 40,
        "set_name": "CS101-A",
        "course_level": "First Year",
        "branch_name": "main"
    },
    {
        "class_id": 2,
        "course_code": "CS101",
        "course_lec": 3,
        "course_lab": 2,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 35,
        "set_name": "CS101-B",
        "course_level": "First Year",
        "branch_name": "main"
    },
    {
        "class_id": 3,
        "course_code": "CS201",
        "course_lec": 3,
        "course_lab": 1,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 30,
        "set_name": "CS201-A",
        "course_level": "Second Year",
        "branch_name": "main"
    },
    {
        "class_id": 4,
        "course_code": "CS301",
        "course_lec": 3,
        "course_lab": 3,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 25,
        "set_name": "CS301-A",
        "course_level": "Third Year",
        "branch_name": "main"
    },
    {
        "class_id": 5,
        "course_code": "MATH101",
        "course_lec": 3,
        "course_lab": 0,          # No lab component
        "program_id": 2,          # Mathematics Program
        "institute_id": 1,
        "class_size": 50,
        "set_name": "MATH101-A",
        "course_level": "First Year",
        "branch_name": "main"
    },
    {
        "class_id": 6,
        "course_code": "MATH201",
        "course_lec": 3,
        "course_lab": 0,
        "program_id": 2,
        "institute_id": 1,
        "class_size": 45,
        "set_name": "MATH201-A",
        "course_level": "Second Year",
        "branch_name": "main"
    },
    {
        "class_id": 7,
        "course_code": "PHYS101",
        "course_lec": 3,
        "course_lab": 0,
        "program_id": 3,          # Physics Program
        "institute_id": 1,
        "class_size": 30,
        "set_name": "PHYS101-A",
        "course_level": "First Year",
        "branch_name": "main"
    },
    {
        "class_id": 8,
        "course_code": "CS401",
        "course_lec": 3,
        "course_lab": 2,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 20,
        "set_name": "CS401-A",
        "course_level": "Fourth Year",
        "branch_name": "main"
    },
    {
        "class_id": 9,
        "course_code": "CS202",
        "course_lec": 3,
        "course_lab": 2,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 32,
        "set_name": "CS202-A",
        "course_level": "Second Year",
        "branch_name": "main"
    },
    {
        "class_id": 10,
        "course_code": "MATH301",
        "course_lec": 3,
        "course_lab": 0,
        "program_id": 2,
        "institute_id": 1,
        "class_size": 35,
        "set_name": "MATH301-A",
        "course_level": "Third Year",
        "branch_name": "main"
    },
    # Carmen branch
    {
        "class_id": 11,
        "course_code": "CS101",
        "course_lec": 3,
        "course_lab": 2,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 30,
        "set_name": "CS101-A",
        "course_level": "First Year",
        "branch_name": "carmen branch"
    },
    {
        "class_id": 12,
        "course_code": "MATH101",
        "course_lec": 3,
        "course_lab": 0,
        "program_id": 2,
        "institute_id": 1,
        "class_size": 35,
        "set_name": "MATH101-A",
        "course_level": "First Year",
        "branch_name": "carmen branch"
    },
    {
        "class_id": 13,
        "course_code": "CS201",
        "course_lec": 3,
        "course_lab": 1,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 25,
        "set_name": "CS201-A",
        "course_level": "Second Year",
        "branch_name": "carmen branch"
    },
    # Samal branch
    {
        "class_id": 14,
        "course_code": "CS101",
        "course_lec": 3,
        "course_lab": 2,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 28,
        "set_name": "CS101-A",
        "course_level": "First Year",
        "branch_name": "samal branch"
    },
    {
        "class_id": 15,
        "course_code": "MATH101",
        "course_lec": 3,
        "course_lab": 0,
        "program_id": 2,
        "institute_id": 1,
        "class_size": 32,
        "set_name": "MATH101-A",
        "course_level": "First Year",
        "branch_name": "samal branch"
    },
    {
        "class_id": 16,
        "course_code": "CS202",
        "course_lec": 3,
        "course_lab": 2,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 22,
        "set_name": "CS202-A",
        "course_level": "Second Year",
        "branch_name": "samal branch"
    },
    # Talaingod branch
    {
        "class_id": 17,
        "course_code": "CS101",
        "course_lec": 3,
        "course_lab": 2,
        "program_id": 1,
        "institute_id": 1,
        "class_size": 25,
        "set_name": "CS101-A",
        "course_level": "First Year",
        "branch_name": "talaingod branch"
    },
    {
        "class_id": 18,
        "course_code": "MATH101",
        "course_lec": 3,
        "course_lab": 0,
        "program_id": 2,
        "institute_id": 1,
        "class_size": 28,
        "set_name": "MATH101-A",
        "course_level": "First Year",
        "branch_name": "talaingod branch"
    }
]

# ============================================================================
# SAMPLE FACULTY_EXPERTISE_COURSES DATA
# ============================================================================
# Structure: List of dictionaries, each representing a faculty's expertise
# Required fields: faculty_id, faculty_name, course_code, program_id, employment_type, load_unit
# employment_type: "full time" or "part time"
# load_unit: 18 for full time, 9 for part time
# Note: A faculty can have multiple expertise entries (one per course they can teach)

SAMPLE_FACULTY_EXPERTISE_COURSES = [
    {
        "faculty_id": 1,
        "faculty_name": "Dr. John Smith",
        "course_code": "CS101",
        "program_id": 1,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 1,
        "faculty_name": "Dr. John Smith",
        "course_code": "CS201",
        "program_id": 1,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 1,
        "faculty_name": "Dr. John Smith",
        "course_code": "CS301",
        "program_id": 1,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 2,
        "faculty_name": "Prof. Jane Doe",
        "course_code": "CS101",
        "program_id": 1,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 2,
        "faculty_name": "Prof. Jane Doe",
        "course_code": "CS202",
        "program_id": 1,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 2,
        "faculty_name": "Prof. Jane Doe",
        "course_code": "CS401",
        "program_id": 1,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 3,
        "faculty_name": "Dr. Robert Johnson",
        "course_code": "MATH101",
        "program_id": 2,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 3,
        "faculty_name": "Dr. Robert Johnson",
        "course_code": "MATH201",
        "program_id": 2,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 3,
        "faculty_name": "Dr. Robert Johnson",
        "course_code": "MATH301",
        "program_id": 2,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 4,
        "faculty_name": "Prof. Emily Williams",
        "course_code": "MATH101",
        "program_id": 2,
        "employment_type": "part time",
        "load_unit": 9
    },
    {
        "faculty_id": 4,
        "faculty_name": "Prof. Emily Williams",
        "course_code": "MATH201",
        "program_id": 2,
        "employment_type": "part time",
        "load_unit": 9
    },
    {
        "faculty_id": 5,
        "faculty_name": "Dr. Michael Brown",
        "course_code": "PHYS101",
        "program_id": 3,
        "employment_type": "part time",
        "load_unit": 9
    },
    {
        "faculty_id": 6,
        "faculty_name": "Prof. Sarah Davis",
        "course_code": "CS201",
        "program_id": 1,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 6,
        "faculty_name": "Prof. Sarah Davis",
        "course_code": "CS301",
        "program_id": 1,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 6,
        "faculty_name": "Prof. Sarah Davis",
        "course_code": "CS401",
        "program_id": 1,
        "employment_type": "full time",
        "load_unit": 18
    },
    {
        "faculty_id": 7,
        "faculty_name": "Dr. David Wilson",
        "course_code": "CS101",
        "program_id": 1,
        "employment_type": "part time",
        "load_unit": 9
    },
    {
        "faculty_id": 7,
        "faculty_name": "Dr. David Wilson",
        "course_code": "CS202",
        "program_id": 1,
        "employment_type": "part time",
        "load_unit": 9
    }
]

# ============================================================================
# SAMPLE ROOMS DATA
# ============================================================================
# Structure: List of dictionaries, each representing an available room
# Required fields: room_id, room_name, room_type, room_capacity, institute_id
# room_type must be either "Lecture" or "Laboratory" (case-sensitive matching)

SAMPLE_ROOMS = [
    # Lecture Rooms
    {
        "room_id": 1,
        "room_name": "Lecture Hall A",
        "room_type": "Lecture",
        "room_capacity": 50,
        "institute_id": 1
    },
    {
        "room_id": 2,
        "room_name": "Lecture Hall B",
        "room_type": "Lecture",
        "room_capacity": 50,
        "institute_id": 1
    },
    {
        "room_id": 3,
        "room_name": "Lecture Hall C",
        "room_type": "Lecture",
        "room_capacity": 40,
        "institute_id": 1
    },
    {
        "room_id": 4,
        "room_name": "Lecture Room 101",
        "room_type": "Lecture",
        "room_capacity": 30,
        "institute_id": 1
    },
    {
        "room_id": 5,
        "room_name": "Lecture Room 102",
        "room_type": "Lecture",
        "room_capacity": 30,
        "institute_id": 1
    },
    {
        "room_id": 6,
        "room_name": "Lecture Room 201",
        "room_type": "Lecture",
        "room_capacity": 25,
        "institute_id": 1
    },
    {
        "room_id": 7,
        "room_name": "Lecture Room 202",
        "room_type": "Lecture",
        "room_capacity": 25,
        "institute_id": 1
    },
    {
        "room_id": 8,
        "room_name": "Large Lecture Hall",
        "room_type": "Lecture",
        "room_capacity": 100,
        "institute_id": 1
    },
    # Laboratory Rooms
    {
        "room_id": 9,
        "room_name": "Lab A",
        "room_type": "Laboratory",
        "room_capacity": 30,
        "institute_id": 1
    },
    {
        "room_id": 10,
        "room_name": "Lab B",
        "room_type": "Laboratory",
        "room_capacity": 30,
        "institute_id": 1
    },
    {
        "room_id": 11,
        "room_name": "Computer Lab 1",
        "room_type": "Laboratory",
        "room_capacity": 25,
        "institute_id": 1
    },
    {
        "room_id": 12,
        "room_name": "Computer Lab 2",
        "room_type": "Laboratory",
        "room_capacity": 25,
        "institute_id": 1
    },
    {
        "room_id": 13,
        "room_name": "Computer Lab 3",
        "room_type": "Laboratory",
        "room_capacity": 20,
        "institute_id": 1
    },
    {
        "room_id": 14,
        "room_name": "Physics Lab 1",
        "room_type": "Laboratory",
        "room_capacity": 30,
        "institute_id": 1
    },
    {
        "room_id": 15,
        "room_name": "Physics Lab 2",
        "room_type": "Laboratory",
        "room_capacity": 25,
        "institute_id": 1
    },
    {
        "room_id": 16,
        "room_name": "Advanced Lab",
        "room_type": "Laboratory",
        "room_capacity": 20,
        "institute_id": 1
    }
]

# ============================================================================
# USAGE EXAMPLE
# ============================================================================
"""
To use this sample data in your main script, replace the database fetch section:

    # OLD CODE (from database):
    # classes_course_table = Table("classes_course", metadata, autoload_with=engine)
    # faculty_expertise_courses_table = Table("faculty_expertise_courses", metadata, autoload_with=engine)
    # rooms_table = Table("rooms", metadata, autoload_with=engine)
    # classes_course = fetch_table_data(classes_course_table)
    # faculty_expertise_courses = fetch_table_data(faculty_expertise_courses_table)
    # rooms = fetch_table_data(rooms_table)

    # NEW CODE (using sample data):
    from sample_input_data import (
        SAMPLE_CLASSES_COURSE,
        SAMPLE_FACULTY_EXPERTISE_COURSES,
        SAMPLE_ROOMS
    )
    
    classes_course = SAMPLE_CLASSES_COURSE
    faculty_expertise_courses = SAMPLE_FACULTY_EXPERTISE_COURSES
    rooms = SAMPLE_ROOMS
"""

# ============================================================================
# DATA SUMMARY
# ============================================================================
"""
SAMPLE DATA SUMMARY:

Classes/Courses: 10 classes
- CS101: 2 sections (40 and 35 students)
- CS201: 1 section (30 students)
- CS301: 1 section (25 students)
- CS401: 1 section (20 students)
- CS202: 1 section (32 students)
- MATH101: 1 section (50 students)
- MATH201: 1 section (45 students)
- MATH301: 1 section (35 students)
- PHYS101: 1 section (30 students)

Faculty: 7 faculty members
- Dr. John Smith: Can teach CS101, CS201, CS301 (full time, 18 units)
- Prof. Jane Doe: Can teach CS101, CS202, CS401 (full time, 18 units)
- Dr. Robert Johnson: Can teach MATH101, MATH201, MATH301 (full time, 18 units)
- Prof. Emily Williams: Can teach MATH101, MATH201 (part time, 9 units)
- Dr. Michael Brown: Can teach PHYS101 (part time, 9 units)
- Prof. Sarah Davis: Can teach CS201, CS301, CS401 (full time, 18 units)
- Dr. David Wilson: Can teach CS101, CS202 (part time, 9 units)

Rooms: 16 rooms total
- 8 Lecture rooms (capacities: 25, 30, 40, 50, 100)
- 8 Laboratory rooms (capacities: 20, 25, 30)

Expected Behavior:
- Faculty will be assigned classes based on expertise matching
- Full time faculty can handle up to 18 units, part time faculty up to 9 units
- Classes will be scheduled into available time slots (8 AM - 9 PM, excluding 12-1 PM lunch)
- Rooms will be matched by type (Lecture/Laboratory) and institute_id
- Room capacity must accommodate class size (with 5 student tolerance)
"""

