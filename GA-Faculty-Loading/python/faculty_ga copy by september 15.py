import random
import copy
import json

# =========================
# SAMPLE DATA (your data preserved)
# =========================
institutes = [
    {"institute_id": 1, "institute_code": "IC",
        "institute_name": "Institute of Computing"},
    {"institute_id": 2, "institute_code": "ITED",
        "institute_name": "Institution of Teacher Education"}
]

programs = [
    {"program_id": 1, "institute_id": 1, "program_code": "BSIT",
        "program_name": "BS in Information Technology"},
    {"program_id": 2, "institute_id": 2, "program_code": "BSED",
        "program_name": "BS in Secondary Education"}
]

specializations = [
    {"specialization_id": 1, "specialization_name": "Computing"},
    {"specialization_id": 2, "specialization_name": "Education"}
]

expertise = [
    {"expertise_id": 1, "specialization_id": 1, "expertise_name": "AI"},
    {"expertise_id": 2, "specialization_id": 1, "expertise_name": "Networking"},
    {"expertise_id": 3, "specialization_id": 2, "expertise_name": "Math"},
    {"expertise_id": 4, "specialization_id": 2, "expertise_name": "Science"}
]

faculty = [
    {"faculty_id": 1, "faculty_fname": "Alice", "faculty_mname": "B.", "faculty_lname": "Cruz",
     "faculty_institute_id": 1, "faculty_program_id": 1, "faculty_specialization": 1,
     "faculty_expertise": [1, 2], "max_units": 18, "max_preparations": 2},
    {"faculty_id": 2, "faculty_fname": "Bob", "faculty_mname": "C.", "faculty_lname": "Reyes",
     "faculty_institute_id": 1, "faculty_program_id": 1, "faculty_specialization": 1,
     "faculty_expertise": [2], "max_units": 18, "max_preparations": 2},
    {"faculty_id": 3, "faculty_fname": "Charlie", "faculty_mname": "D.", "faculty_lname": "Santos",
     "faculty_institute_id": 2, "faculty_program_id": 2, "faculty_specialization": 2,
     "faculty_expertise": [3], "max_units": 18, "max_preparations": 2},
    {"faculty_id": 4, "faculty_fname": "Diana", "faculty_mname": "E.", "faculty_lname": "Mendoza",
     "faculty_institute_id": 2, "faculty_program_id": 2, "faculty_specialization": 2,
     "faculty_expertise": [4], "max_units": 18, "max_preparations": 2}
]

curriculum = [
    {
        "curriculum_id": 1,
        "program_id": 1,
        "curriculum_name": "BSIT 2025 Curriculum",
        "curriculum_since": "2025",
        "curriculum_effective": "2025-06-01",
        "curriculum_cmo": "CMO 2025",
        "active": True
    },
    {
        "curriculum_id": 2,
        "program_id": 2,
        "curriculum_name": "BSED 2025 Curriculum",
        "curriculum_since": "2025",
        "curriculum_effective": "2025-06-01",
        "curriculum_cmo": "CMO 2025",
        "active": True
    }
]

courses = [
    # =========================
    # BSIT Courses (CURR1)
    # =========================
    {"course_id": 1, "curriculum_id": 1, "program_id": 1, "course_code": "IT101",
     "course_description": "Introduction to IT", "course_level": 1, "course_semester": 1,
     "course_lecture": 3, "course_laboratory": 0, "course_requisite": None,
     "tags": [1], "room_type": "Lecture", "hours": 3},

    {"course_id": 2, "curriculum_id": 1, "program_id": 1, "course_code": "IT102",
     "course_description": "Programming Fundamentals", "course_level": 1, "course_semester": 1,
     "course_lecture": 3, "course_laboratory": 1, "course_requisite": None,
     "tags": [1], "room_type": "Mixed", "hours": 4},

    {"course_id": 3, "curriculum_id": 1, "program_id": 1, "course_code": "IT201",
     "course_description": "Data Structures", "course_level": 2, "course_semester": 1,
     "course_lecture": 3, "course_laboratory": 1, "course_requisite": None,
     "tags": [1], "room_type": "Mixed", "hours": 4},

    {"course_id": 4, "curriculum_id": 1, "program_id": 1, "course_code": "AI301",
     "course_description": "Artificial Intelligence", "course_level": 3, "course_semester": 2,
     "course_lecture": 3, "course_laboratory": 2, "course_requisite": None,
     "tags": [1], "room_type": "Mixed", "hours": 5},

    # Networking
    {"course_id": 5, "curriculum_id": 1, "program_id": 1, "course_code": "NET201",
     "course_description": "Networking Basics", "course_level": 2, "course_semester": 1,
     "course_lecture": 3, "course_laboratory": 0, "course_requisite": None,
     "tags": [2], "room_type": "Lecture", "hours": 3},

    {"course_id": 6, "curriculum_id": 1, "program_id": 1, "course_code": "NET202",
     "course_description": "Advanced Networking", "course_level": 3, "course_semester": 2,
     "course_lecture": 3, "course_laboratory": 3, "course_requisite": None,
     "tags": [2], "room_type": "Mixed", "hours": 5},

    {"course_id": 7, "curriculum_id": 1, "program_id": 1, "course_code": "NETLAB203",
     "course_description": "Network Lab", "course_level": 2, "course_semester": 2,
     "course_lecture": 2, "course_laboratory": 3, "course_requisite": None,
     "tags": [2], "room_type": "Mixed", "hours": 5},

    {"course_id": 15, "curriculum_id": 1, "program_id": 1, "course_code": "CLOUD401",
     "course_description": "Cloud Computing", "course_level": 4, "course_semester": 1,
     "course_lecture": 3, "course_laboratory": 2, "course_requisite": None,
     "tags": [1, 2], "room_type": "Mixed", "hours": 5},

    # =========================
    # BSED Courses (CURR2)
    # =========================
    {"course_id": 8, "curriculum_id": 2, "program_id": 2, "course_code": "MATH101",
     "course_description": "College Algebra", "course_level": 1, "course_semester": 1,
     "course_lecture": 3, "course_laboratory": 0, "course_requisite": None,
     "tags": [3], "room_type": "Lecture", "hours": 3},

    {"course_id": 9, "curriculum_id": 2, "program_id": 2, "course_code": "MATH201",
     "course_description": "Calculus I", "course_level": 2, "course_semester": 1,
     "course_lecture": 3, "course_laboratory": 0, "course_requisite": None,
     "tags": [3], "room_type": "Lecture", "hours": 3},

    {"course_id": 10, "curriculum_id": 2, "program_id": 2, "course_code": "MATH301",
     "course_description": "Advanced Math", "course_level": 3, "course_semester": 2,
     "course_lecture": 3, "course_laboratory": 0, "course_requisite": None,
     "tags": [3], "room_type": "Lecture", "hours": 3},

    {"course_id": 11, "curriculum_id": 2, "program_id": 2, "course_code": "SCI101",
     "course_description": "General Science", "course_level": 1, "course_semester": 1,
     "course_lecture": 3, "course_laboratory": 0, "course_requisite": None,
     "tags": [4], "room_type": "Lecture", "hours": 3},

    {"course_id": 12, "curriculum_id": 2, "program_id": 2, "course_code": "SCI201",
     "course_description": "Physics", "course_level": 2, "course_semester": 2,
     "course_lecture": 3, "course_laboratory": 2, "course_requisite": None,
     "tags": [4], "room_type": "Mixed", "hours": 5},

    {"course_id": 13, "curriculum_id": 2, "program_id": 2, "course_code": "SCI301",
     "course_description": "Chemistry", "course_level": 3, "course_semester": 2,
     "course_lecture": 3, "course_laboratory": 2, "course_requisite": None,
     "tags": [4], "room_type": "Mixed", "hours": 5},

    {"course_id": 14, "curriculum_id": 2, "program_id": 2, "course_code": "SCI401",
     "course_description": "Biology", "course_level": 4, "course_semester": 1,
     "course_lecture": 3, "course_laboratory": 2, "course_requisite": None,
     "tags": [4], "room_type": "Mixed", "hours": 5},
]

rooms = [
    {"room_id": 1, "room_name": "IC Room 101",
        "room_category": "Lecture", "room_program_tags": [1]},
    {"room_id": 2, "room_name": "IC Lab 102",
        "room_category": "Laboratory", "room_program_tags": [1]},
    {"room_id": 3, "room_name": "ITED Room 201",
        "room_category": "Lecture", "room_program_tags": [2]},
]

sets = [
    {"set_id": 1, "set_name": "Set A"},
    {"set_id": 2, "set_name": "Set B"},
    {"set_id": 3, "set_name": "Set C"},
    {"set_id": 4, "set_name": "Set D"}
]

assign_set_courses = [
    {"assign_set_id": 1, "course_id": 1, "set_id": 1},
    {"assign_set_id": 2, "course_id": 2, "set_id": 1},
    {"assign_set_id": 3, "course_id": 3, "set_id": 2},
    {"assign_set_id": 4, "course_id": 4, "set_id": 3},
    {"assign_set_id": 5, "course_id": 5, "set_id": 3},
    {"assign_set_id": 6, "course_id": 5, "set_id": 4},
    {"assign_set_id": 7, "course_id": 11, "set_id": 1},
]


# =========================
# GA PARAMETERS
# =========================
POPULATION_SIZE = 40
GENERATIONS = 100
MUTATION_RATE = 0.25
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = [
    ("08:00:00", "10:00:00"),
    ("10:00:00", "12:00:00"),
    ("13:00:00", "15:00:00"),
    ("15:00:00", "17:00:00")
]

# -------------------------
# Build course -> set map
# -------------------------
course_set_map = {entry["course_id"]: entry["set_id"]
                  for entry in assign_set_courses}

# =========================
# HELPERS
# =========================


def faculty_by_id(fid):
    return next((f for f in faculty if f["faculty_id"] == fid), None)


def course_by_id(cid):
    return next((c for c in courses if c["course_id"] == cid), None)


def room_by_id(rid):
    return next((r for r in rooms if r["room_id"] == rid), None)


# compute current load (units) per faculty
def compute_faculty_loads(schedule):
    loads = {f["faculty_id"]: 0 for f in faculty}
    for cid, s in schedule.items():
        if s is None or s.get("instructor") is None:
            continue
        course = course_by_id(cid)
        if course:
            loads[s["instructor"]] += course["hours"]
    return loads


def find_faculty_with_capacity(course, loads):
    # Only faculties with matching expertise AND enough load
    candidates = [f for f in faculty if loads[f["faculty_id"]] + course["hours"] <= f["max_units"]
                  and any(tag in f["faculty_expertise"] for tag in course["tags"])]
    return candidates  # return empty list if none


# =========================
# HELPER: check if slot available
# =========================


def is_slot_available(schedule, instructor_id, room_id, day, start, end):
    for s in schedule.values():
        if s is None:
            continue
        # Check instructor
        if s.get("instructor") == instructor_id:
            for slot_type in ["lecture_slot", "lab_slot"]:
                slot = s.get(slot_type)
                if slot:
                    # slot may be tuple or dict (pre/ post transform). Accept both.
                    if isinstance(slot, dict):
                        s_day = slot.get("day")
                        s_start = slot.get("time_start")
                        s_end = slot.get("time_end")
                    else:
                        s_day, s_start, s_end = slot
                    if s_day == day and not (end <= s_start or start >= s_end):
                        return False
        # Check room
        if room_id in s.get("rooms", {}).values():
            for slot_type in ["lecture_slot", "lab_slot"]:
                slot = s.get(slot_type)
                if slot:
                    if isinstance(slot, dict):
                        s_day = slot.get("day")
                        s_start = slot.get("time_start")
                        s_end = slot.get("time_end")
                    else:
                        s_day, s_start, s_end = slot
                    if s_day == day and not (end <= s_start or start >= s_end):
                        return False
    return True


# =========================
# HELPER: pick a random available slot (prevent overlaps)
# =========================


def random_available_slot(schedule, instructor_id, room_id, blocked_slots=None):
    if blocked_slots is None:
        blocked_slots = []
    days = DAYS[:]
    time_slots = TIME_SLOTS[:]
    random.shuffle(days)
    random.shuffle(time_slots)
    for day in days:
        for ts in time_slots:
            start, end = ts
            # Check instructor and room availability
            if not is_slot_available(schedule, instructor_id, room_id, day, start, end):
                continue
            # Check blocked slots (e.g., same course lecture/lab)
            conflict = False
            for b in blocked_slots:
                if isinstance(b, dict):
                    b_day = b.get("day")
                    b_start = b.get("time_start")
                    b_end = b.get("time_end")
                else:
                    b_day, b_start, b_end = b
                if b_day == day and not (end <= b_start or start >= b_end):
                    conflict = True
                    break
            if not conflict:
                return (day, start, end)
    return None


# =========================
# ROOM ASSIGNMENT (Lecture/Lab)
# =========================


def pick_rooms_for_course(course):
    """
    Returns a dict: {"Lecture": room_id, "Laboratory": room_id}
    Ensures Lecture goes only to Lecture rooms, Lab only to Laboratory rooms.
    """
    rooms_assigned = {}
    if course["course_lecture"] > 0:
        lec_rooms = [r for r in rooms if r["room_category"] == "Lecture"]
        rooms_assigned["Lecture"] = random.choice(
            lec_rooms)["room_id"] if lec_rooms else None
    if course["course_laboratory"] > 0:
        lab_rooms = [r for r in rooms if r["room_category"] == "Laboratory"]
        rooms_assigned["Laboratory"] = random.choice(
            lab_rooms)["room_id"] if lab_rooms else None
    return rooms_assigned

# =========================
# HELPER: find faculty with expertise & capacity
# =========================


def find_faculty_with_expertise(course, loads):
    """
    Returns only faculties who have at least one matching tag and enough capacity.
    """
    candidates = [
        f for f in faculty
        if loads[f["faculty_id"]] + course["hours"] <= f["max_units"]
        and any(tag in f["faculty_expertise"] for tag in course["tags"])
    ]
    return candidates
# =========================
# REPAIR SCHEDULE (expertise-enforced)
# =========================


def repair_schedule(schedule):
    schedule = copy.deepcopy(schedule)
    loads = compute_faculty_loads(schedule)
    changed = True
    while changed:
        changed = False
        for fid, load in list(loads.items()):
            f = faculty_by_id(fid)
            if f is None or load <= f["max_units"]:
                continue
            # get assigned courses for this faculty
            assigned_courses = [
                cid for cid, s in schedule.items() if s and s.get("instructor") == fid]
            assigned_courses.sort(key=lambda cid: course_by_id(cid)[
                                  "hours"], reverse=True)
            moved_any = False
            for cid in assigned_courses:
                course = course_by_id(cid)
                if not course:
                    continue
                targets = [t for t in find_faculty_with_expertise(
                    course, loads) if t["faculty_id"] != fid]
                if not targets:
                    continue  # cannot move if no faculty matches expertise
                targets.sort(key=lambda t: loads[t["faculty_id"]])
                target = targets[0]

                set_id = course_set_map.get(cid)
                moved_with_set = False
                if set_id:
                    same_set_courses = [c for c, sid in course_set_map.items(
                    ) if sid == set_id and schedule.get(c) and schedule[c].get("instructor") == fid]
                    total_hours = sum(course_by_id(
                        c)["hours"] for c in same_set_courses)
                    if loads[target["faculty_id"]] + total_hours <= target["max_units"]:
                        for c in same_set_courses:
                            schedule[c]["instructor"] = target["faculty_id"]
                            loads[fid] -= course_by_id(c)["hours"]
                            loads[target["faculty_id"]
                                  ] += course_by_id(c)["hours"]
                        moved_any = True
                        moved_with_set = True
                        changed = True

                if not moved_with_set:
                    schedule[cid]["instructor"] = target["faculty_id"]
                    loads[fid] -= course["hours"]
                    loads[target["faculty_id"]] += course["hours"]
                    moved_any = True
                    changed = True

                if moved_any:
                    break

            if not moved_any and assigned_courses:
                cid = assigned_courses[0]
                course = course_by_id(cid)
                schedule[cid] = None
                loads[fid] -= course["hours"]
                changed = True
    return schedule
# =========================
# RANDOM ASSIGNMENT (set-aware, expertise-enforced)
# =========================


def random_assignment(courses_subset, faculty_subset):
    schedule = {}
    loads = {f["faculty_id"]: 0 for f in faculty_subset}

    # group courses by set
    set_groups = {}
    assigned_course_ids = set()
    for c in courses_subset:
        cid = c["course_id"]
        sid = course_set_map.get(cid)
        if sid:
            set_groups.setdefault(sid, []).append(c)
            assigned_course_ids.add(cid)

    # singleton groups for courses not in any set
    singletons = [[c] for c in courses_subset if c["course_id"]
                  not in assigned_course_ids]

    all_groups = list(set_groups.values()) + singletons
    random.shuffle(all_groups)

    for group in all_groups:
        group_hours = sum(g["hours"] for g in group)

        # find faculty who can take the group AND match expertise for all courses
        candidates = []
        for f in faculty_subset:
            if loads[f["faculty_id"]] + group_hours <= f["max_units"]:
                if all(any(tag in f["faculty_expertise"] for tag in g["tags"]) for g in group):
                    candidates.append(f)

        if not candidates:
            # Hard constraint: leave unassigned
            for g in group:
                schedule[g["course_id"]] = None
            continue

        # pick best candidate (lowest load)
        candidates.sort(key=lambda f: loads[f["faculty_id"]])
        instructor = candidates[0]["faculty_id"]

        group_assigned_slots = []
        for course in group:
            rooms_assigned = pick_rooms_for_course(course)
            lec_time = None
            lab_time = None
            if "Lecture" in rooms_assigned:
                lec_time = random_available_slot(schedule, instructor, rooms_assigned["Lecture"],
                                                 blocked_slots=group_assigned_slots)
            if "Laboratory" in rooms_assigned:
                lab_time = random_available_slot(schedule, instructor, rooms_assigned["Laboratory"],
                                                 blocked_slots=group_assigned_slots + ([lec_time] if lec_time else []))
            schedule[course["course_id"]] = {
                "instructor": instructor,
                "rooms": rooms_assigned,
                "lecture_slot": lec_time,
                "lab_slot": lab_time
            }

            if lec_time:
                group_assigned_slots.append(lec_time)
            if lab_time:
                group_assigned_slots.append(lab_time)

            loads[instructor] += course["hours"]

    schedule = repair_schedule(schedule)
    return schedule
    schedule = {}
    loads = {f["faculty_id"]: 0 for f in faculty_subset}

    # group courses by set; courses without set become singleton groups
    set_groups = {}
    assigned_course_ids = set()
    for c in courses_subset:
        cid = c["course_id"]
        sid = course_set_map.get(cid)
        if sid:
            set_groups.setdefault(sid, []).append(c)
            assigned_course_ids.add(cid)

    singletons = [[c] for c in courses_subset if c["course_id"]
                  not in assigned_course_ids]
    all_groups = list(set_groups.values()) + singletons
    random.shuffle(all_groups)

    for group in all_groups:
        group_hours = sum(g["hours"] for g in group)

        # Filter only faculties who have expertise for **all courses in group**
        candidates = [
            f for f in faculty_subset
            if loads[f["faculty_id"]] + group_hours <= f["max_units"]
            and all(any(tag in f["faculty_expertise"] for tag in g["tags"]) for g in group)
        ]

        if not candidates:
            # No faculty can teach this group: leave unassigned
            for g in group:
                schedule[g["course_id"]] = None
            continue

        # Score candidates by expertise matches and load
        def cand_score(f):
            match_count = sum(
                1 for g in group if any(tag in f["faculty_expertise"] for tag in g["tags"])
            )
            return (-match_count, loads[f["faculty_id"]])

        candidates.sort(key=cand_score)
        instructor = candidates[0]["faculty_id"]  # pick best-scoring faculty

        # Assign courses in group
        group_assigned_slots = []
        for course in group:
            rooms_assigned = pick_rooms_for_course(course)
            lec_time = None
            lab_time = None
            if "Lecture" in rooms_assigned:
                lec_time = random_available_slot(schedule, instructor, rooms_assigned["Lecture"],
                                                 blocked_slots=group_assigned_slots)
            if "Laboratory" in rooms_assigned:
                lab_time = random_available_slot(schedule, instructor, rooms_assigned["Laboratory"],
                                                 blocked_slots=group_assigned_slots + ([lec_time] if lec_time else []))

            schedule[course["course_id"]] = {
                "instructor": instructor,
                "rooms": rooms_assigned,
                "lecture_slot": lec_time,
                "lab_slot": lab_time
            }

            # update assigned slots
            if lec_time:
                group_assigned_slots.append(lec_time)
            if lab_time:
                group_assigned_slots.append(lab_time)

            loads[instructor] += course["hours"]

    # Repair schedule to fix overloads/discrepancies (still expertise-safe)
    schedule = repair_schedule(schedule)
    return schedule


# =========================
# MUTATE (expertise-enforced)
# =========================
def mutate(schedule, courses_subset, faculty_subset):
    schedule = copy.deepcopy(schedule)
    for cid in list(schedule.keys()):
        if random.random() < MUTATION_RATE:
            course = course_by_id(cid)
            loads = compute_faculty_loads(schedule)
            candidates = find_faculty_with_expertise(course, loads)
            if not candidates:
                continue  # skip if no faculty has expertise
            instructor = random.choice(candidates)["faculty_id"]

            rooms_assigned = pick_rooms_for_course(course)
            lec_time = random_available_slot(schedule, instructor, rooms_assigned.get(
                "Lecture")) if "Lecture" in rooms_assigned else None
            lab_time = random_available_slot(schedule, instructor, rooms_assigned.get("Laboratory"),
                                             blocked_slots=[lec_time] if lec_time else []) if "Laboratory" in rooms_assigned else None

            schedule[cid] = {
                "instructor": instructor,
                "rooms": rooms_assigned,
                "lecture_slot": lec_time,
                "lab_slot": lab_time
            }

    schedule = repair_schedule(schedule)
    return schedule


# =========================
# CROSSOVER
# =========================


def crossover(p1, p2):
    child = {}
    cids = sorted(list(set(list(p1.keys()) + list(p2.keys()))))
    point = random.randint(1, max(1, len(cids)-1))
    left = set(cids[:point])
    for cid in cids:
        if cid in left:
            child[cid] = copy.deepcopy(p1.get(cid))
        else:
            child[cid] = copy.deepcopy(p2.get(cid))
    child = repair_schedule(child)
    return child


# =========================
# FITNESS (set-aware)
# =========================


def fitness(schedule, courses_subset, faculty_subset, max_units=18):
    if schedule is None:
        return -9999
    base = 1000.0
    score = base
    loads = {f["faculty_id"]: 0 for f in faculty_subset}
    preparations = {f["faculty_id"]: set() for f in faculty_subset}
    missing_courses = 0

    for course in courses_subset:
        cid = course["course_id"]
        if cid not in schedule or schedule[cid] is None or schedule[cid].get("instructor") is None:
            missing_courses += 1
            continue
        s = schedule[cid]
        loads[s["instructor"]] += course["hours"]
        preparations[s["instructor"]].add(course["course_code"])

    score -= missing_courses * 1000

    # Instructor & Room conflicts
    course_ids = [c["course_id"] for c in courses_subset if c["course_id"]
                  in schedule and schedule[c["course_id"]] is not None]
    for i in range(len(course_ids)):
        cid1 = course_ids[i]
        s1 = schedule[cid1]
        for j in range(i+1, len(course_ids)):
            cid2 = course_ids[j]
            s2 = schedule[cid2]
            # Check lecture overlap
            if s1.get("lecture_slot") and s2.get("lecture_slot") and s1["lecture_slot"][0] == s2["lecture_slot"][0]:
                overlap = not (s1["lecture_slot"][2] <= s2["lecture_slot"]
                               [1] or s2["lecture_slot"][2] <= s1["lecture_slot"][1])
                if overlap:
                    if s1["instructor"] == s2["instructor"]:
                        score -= 400
                    if s1["rooms"].get("Lecture") == s2["rooms"].get("Lecture"):
                        score -= 300
            # Check lab overlap
            if s1.get("lab_slot") and s2.get("lab_slot") and s1["lab_slot"][0] == s2["lab_slot"][0]:
                overlap = not (s1["lab_slot"][2] <= s2["lab_slot"]
                               [1] or s2["lab_slot"][2] <= s1["lab_slot"][1])
                if overlap:
                    if s1["instructor"] == s2["instructor"]:
                        score -= 400
                    if s1["rooms"].get("Laboratory") == s2["rooms"].get("Laboratory"):
                        score -= 300

    # Room type mismatch penalty
    for cid in course_ids:
        course = course_by_id(cid)
        s = schedule[cid]
        if course["course_lecture"] > 0:
            lec_room_id = s["rooms"].get("Lecture")
            if lec_room_id:
                room_cat = room_by_id(lec_room_id)["room_category"]
                if room_cat != "Lecture":
                    score -= 300
        if course["course_laboratory"] > 0:
            lab_room_id = s["rooms"].get("Laboratory")
            if lab_room_id:
                room_cat = room_by_id(lab_room_id)[
                    "room_category"]
                if room_cat != "Laboratory":
                    score -= 300

    # Expertise soft penalty
    for cid in course_ids:
        course = course_by_id(cid)
        s = schedule[cid]
        inst = faculty_by_id(s["instructor"])
        if not any(tag in inst["faculty_expertise"] for tag in course["tags"]):
            score -= 50

    # Preparation limit penalty
    for f in faculty_subset:
        prep = len(preparations[f["faculty_id"]])
        if prep > f["max_preparations"]:
            score -= (prep - f["max_preparations"]) * 200

    # Faculty overload penalty
    for f in faculty_subset:
        load = loads[f["faculty_id"]]
        if load > f["max_units"]:
            score -= (load - f["max_units"]) * 1000

    # === New: set consistency penalty (prefer same instructor for courses in same set) ===
    # For each set, penalize if courses belonging to it are taught by multiple instructors.
    sets_in_courses = {}
    for cid in course_ids:
        sid = course_set_map.get(cid)
        if sid:
            sets_in_courses.setdefault(sid, []).append(cid)
    for sid, cids in sets_in_courses.items():
        instructors = set(schedule[c]["instructor"]
                          for c in cids if schedule[c])
        if len(instructors) > 1:
            # small penalty per split (soft constraint)
            score -= (len(instructors) - 1) * 200

    return score


# =========================
# CONFLICT CHECKER (human-friendly)
# =========================

def check_conflicts(schedule):
    conflicts = []
    for fid in [f["faculty_id"] for f in faculty]:
        sessions = []
        for cid, s in schedule.items():
            if not s:
                continue
            if s.get("instructor") == fid:
                if s.get("lecture_slot") and s.get("rooms", {}).get("Lecture"):
                    sessions.append(
                        ("Lecture", s["rooms"]["Lecture"], s["lecture_slot"], cid))
                if s.get("lab_slot") and s.get("rooms", {}).get("Laboratory"):
                    sessions.append(
                        ("Lab", s["rooms"]["Laboratory"], s["lab_slot"], cid))
        # check overlaps
        for i in range(len(sessions)):
            t1, r1, slot1, c1 = sessions[i]
            # normalize slot to tuple (day,start,end)
            if isinstance(slot1, dict):
                day1, start1, end1 = slot1["day"], slot1["time_start"], slot1["time_end"]
            else:
                day1, start1, end1 = slot1
            for j in range(i+1, len(sessions)):
                t2, r2, slot2, c2 = sessions[j]
                if isinstance(slot2, dict):
                    day2, start2, end2 = slot2["day"], slot2["time_start"], slot2["time_end"]
                else:
                    day2, start2, end2 = slot2
                if day1 == day2 and not (end1 <= start2 or end2 <= start1):
                    conflicts.append(
                        f"Instructor {faculty_by_id(fid)['faculty_fname']} has conflict between {c1} ({t1}) and {c2} ({t2})")
    return conflicts


# =========================
# GENETIC ALGORITHM (Final Part)
# =========================


def genetic_algorithm(courses_subset, faculty_subset):
    population = [random_assignment(courses_subset, faculty_subset)
                  for _ in range(POPULATION_SIZE)]
    best_schedule = None
    best_score = float("-inf")

    for gen in range(GENERATIONS):
        scored_pop = [(s, fitness(s, courses_subset, faculty_subset))
                      for s in population]
        scored_pop.sort(key=lambda x: x[1], reverse=True)

        if scored_pop[0][1] > best_score:
            best_schedule, best_score = scored_pop[0]

        # Elitism + Crossover
        new_pop = [copy.deepcopy(scored_pop[0][0])]
        while len(new_pop) < POPULATION_SIZE:
            p1, _ = random.choice(scored_pop[:10])
            p2, _ = random.choice(scored_pop[:10])
            child = crossover(p1, p2)
            child = mutate(child, courses_subset, faculty_subset)
            new_pop.append(child)

        population = new_pop

    return best_schedule, best_score


# =========================
# RUN GA
# =========================

if __name__ == "__main__":
    import json  # ensure json is imported

    # FILTER COURSES BY ACTIVE CURRICULA
    active_curriculum_ids = {c["curriculum_id"]
                             for c in curriculum if c["active"]}
    active_courses = [
        course for course in courses if course["curriculum_id"] in active_curriculum_ids]

    # =========================
    # NEW: Filter faculty by active curricula' program_id
    # If a curriculum is active, only faculties whose faculty_program_id == that curriculum.program_id
    # will be used in generation. If none found, fallback to using all faculty (with a warning).
    # =========================
    active_program_ids = {c["program_id"] for c in curriculum if c["active"]}
    filtered_faculty = [
        f for f in faculty if f["faculty_program_id"] in active_program_ids]

    if not filtered_faculty:
        print("Warning: No faculty found for active curricula programs. Falling back to all faculty.")
        filtered_faculty = faculty[:]  # fallback to all faculty

    # Temporarily replace global `faculty` with filtered_faculty so helper functions that reference the global work correctly
    original_faculty = faculty
    faculty = filtered_faculty

    try:
        # RUN THE GA ON ACTIVE COURSES ONLY, using filtered faculty
        best_schedule, best_score = genetic_algorithm(active_courses, faculty)
    finally:
        # Restore original faculty variable (cleanup)
        faculty = original_faculty

    # Transform lecture_slot and lab_slot to named dicts
    for cid, details in best_schedule.items():
        if details is None:
            continue
        if details.get("lecture_slot"):
            lecture = details["lecture_slot"]
            if isinstance(lecture, tuple):
                best_schedule[cid]["lecture_slot"] = {
                    "day": lecture[0],
                    "time_start": lecture[1],
                    "time_end": lecture[2]
                }
        if details.get("lab_slot"):
            lab = details["lab_slot"]
            if isinstance(lab, tuple):
                best_schedule[cid]["lab_slot"] = {
                    "day": lab[0],
                    "time_start": lab[1],
                    "time_end": lab[2]
                }

    # ===================================================
    # FILTER best_schedule to only include assigned courses
    # ===================================================
    assigned_course_ids = {a["course_id"] for a in assign_set_courses}
    best_schedule = {cid: s for cid, s in best_schedule.items()
                     if cid in assigned_course_ids}

    # Calculate total units per faculty
    faculty_units = {f['faculty_id']: 0 for f in original_faculty}
    for cid, s in best_schedule.items():
        if s and s.get('instructor'):
            course = course_by_id(cid)
            faculty_units[s['instructor']] += course['hours']

    # Basic conflict check
    conflicts_basic = check_conflicts(best_schedule)

    # Detailed instructor conflicts
    def detailed_conflict_report(schedule):
        conflicts = []
        for f in original_faculty:
            fid = f["faculty_id"]
            fname = f["faculty_fname"]
            institute = next((i['institute_name'] for i in institutes
                              if i['institute_id'] == f['faculty_institute_id']), "N/A")
            program = next((p['program_name'] for p in programs
                            if p['program_id'] == f['faculty_program_id']), "N/A")

            sessions = []
            for cid, details in schedule.items():
                if details is None or details.get("instructor") != fid:
                    continue
                if details.get("lecture_slot") and details.get("rooms", {}).get("Lecture"):
                    sessions.append({
                        "course_id": cid,
                        "type": "Lecture",
                        "room": details["rooms"]["Lecture"],
                        "time": details["lecture_slot"]
                    })
                if details.get("lab_slot") and details.get("rooms", {}).get("Laboratory"):
                    sessions.append({
                        "course_id": cid,
                        "type": "Lab",
                        "room": details["rooms"]["Laboratory"],
                        "time": details["lab_slot"]
                    })

            # Check for overlapping sessions
            for i in range(len(sessions)):
                s1 = sessions[i]
                day1 = s1["time"]["day"]
                start1 = s1["time"]["time_start"]
                end1 = s1["time"]["time_end"]
                for j in range(i + 1, len(sessions)):
                    s2 = sessions[j]
                    day2 = s2["time"]["day"]
                    start2 = s2["time"]["time_start"]
                    end2 = s2["time"]["time_end"]
                    if day1 != day2:
                        continue
                    if not (end1 <= start2 or end2 <= start1):
                        conflicts.append({
                            "instructor": fname,
                            "institute": institute,
                            "program": program,
                            "conflict": {
                                "session1": s1,
                                "session2": s2
                            }
                        })
        return conflicts

    conflicts_detailed = detailed_conflict_report(best_schedule)

    # Final JSON result
    result = {
        "best_schedule": best_schedule,
        "best_score": best_score,
        "faculty_units": faculty_units,
        "conflicts_basic": conflicts_basic,
        "conflicts_detailed": conflicts_detailed
    }

    print(json.dumps(result, indent=2))
