import random
import json
from sqlalchemy import create_engine, Table, MetaData, select, Column, String, Time, ForeignKey

# =========================
# MySQL Connection
# =========================
DB_USER = "root"
DB_PASS = "admin12345.."
DB_HOST = "127.0.0.2"
DB_PORT = 3306
DB_NAME = "test_for_ga"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
metadata = MetaData()

# =========================
# Load Tables
# =========================
instructors_table = Table("instructors", metadata, autoload_with=engine)
courses_table = Table("courses", metadata, autoload_with=engine)
rooms_table = Table("rooms", metadata, autoload_with=engine)

# =========================
# Fetch data from MySQL
# =========================
with engine.connect() as conn:
    instructors = [dict(row._mapping) for row in conn.execute(select(instructors_table))]
    courses = [dict(row._mapping) for row in conn.execute(select(courses_table))]
    rooms = [dict(row._mapping) for row in conn.execute(select(rooms_table))]

# Parse JSON fields
for inst in instructors:
    if isinstance(inst.get("expertise"), str):
        inst["expertise"] = json.loads(inst["expertise"])
for course in courses:
    if isinstance(course.get("tags"), str):
        course["tags"] = json.loads(course["tags"])

# =========================
# GA Parameters
# =========================
POPULATION_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.2

# =========================
# Define days and time slots
# =========================
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = [
    ("08:00:00", "10:00:00"),
    ("10:00:00", "12:00:00"),
    ("13:00:00", "15:00:00"),
    ("15:00:00", "17:00:00")
]

# =========================
# Random Assignment
# =========================
def random_assignment():
    assignment = {}
    for course in courses:
        instructor = random.choice(instructors)["id"]
        possible_rooms = [r for r in rooms if r.get("type") == course.get("room_type")]
        room = random.choice(possible_rooms)["id"]
        day, time_start, time_end = random.choice([(d, ts[0], ts[1]) for d in DAYS for ts in TIME_SLOTS])
        assignment[course["id"]] = {
            "instructor": instructor,
            "room": room,
            "day": day,
            "time_start": time_start,
            "time_end": time_end
        }
    return assignment

# =========================
# Fitness Function
# =========================
def fitness(schedule):
    hours_count = {inst["id"]: 0 for inst in instructors}
    hard_penalty = 0
    soft_penalty = 0

    for c1 in courses:
        s1 = schedule[c1["id"]]
        inst_id = s1["instructor"]
        room_id = s1["room"]
        hours_count[inst_id] += c1.get("hours", 0)

        # Max hours violation
        inst_max = next(i.get("max_hours", 0) for i in instructors if i.get("id") == inst_id)
        if hours_count[inst_id] > inst_max:
            hard_penalty += 10

        # Room type match
        room_type = next(r.get("type") for r in rooms if r.get("id") == room_id)
        if room_type != c1.get("room_type"):
            hard_penalty += 10

        # Expertise match (soft)
        inst_expertise = next(i.get("expertise", []) for i in instructors if i.get("id") == inst_id)
        if not any(tag in inst_expertise for tag in c1.get("tags", [])):
            soft_penalty += 1

        # Check for conflicts
        for c2 in courses:
            if c1["id"] == c2["id"]:
                continue
            s2 = schedule[c2["id"]]
            if s1["day"] == s2["day"]:
                overlap = not (s1["time_end"] <= s2["time_start"] or s2["time_end"] <= s1["time_start"])
                if overlap:
                    # Same instructor or same room
                    if s1["instructor"] == s2["instructor"] or s1["room"] == s2["room"]:
                        hard_penalty += 20

    total_penalty = hard_penalty + soft_penalty
    return 1 / (1 + total_penalty)

# =========================
# GA Operators
# =========================
def crossover(parent1, parent2):
    child = {}
    for cid in parent1:
        child[cid] = random.choice([parent1[cid], parent2[cid]])
    return child

def mutate(schedule):
    for cid in schedule:
        if random.random() < MUTATION_RATE:
            schedule[cid]["instructor"] = random.choice(instructors)["id"]
            course_type = next(c.get("room_type") for c in courses if c.get("id") == cid)
            possible_rooms = [r for r in rooms if r.get("type") == course_type]
            schedule[cid]["room"] = random.choice(possible_rooms)["id"]
            day, time_start, time_end = random.choice([(d, ts[0], ts[1]) for d in DAYS for ts in TIME_SLOTS])
            schedule[cid]["day"] = day
            schedule[cid]["time_start"] = time_start
            schedule[cid]["time_end"] = time_end
    return schedule

# =========================
# GA Main
# =========================
def genetic_algorithm():
    population = [random_assignment() for _ in range(POPULATION_SIZE)]

    for _ in range(GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        next_gen = population[:2]  # Elitism

        while len(next_gen) < POPULATION_SIZE:
            p1, p2 = random.sample(population[:4], 2)
            child = crossover(p1, p2)
            child = mutate(child)
            next_gen.append(child)

        population = next_gen

    best_schedule = max(population, key=fitness)
    return best_schedule

# =========================
# Main Execution
# =========================
if __name__ == "__main__":
    schedule = genetic_algorithm()

    # Convert schedule dict to list with unique IDs for MySQL insertion
    schedule_list = []
    for idx, (cid, assignment) in enumerate(schedule.items(), start=1):
        course = next(c for c in courses if c.get("id") == cid)
        instructor = next(i for i in instructors if i.get("id") == assignment["instructor"])
        room = next(r for r in rooms if r.get("id") == assignment["room"])

        schedule_list.append({
            "id": f"S{idx}",
            "course_id": cid,
            "course_name": course.get("name", "Unknown"),
            "hours": course.get("hours", 0),
            "room_type": course.get("room_type", "Unknown"),
            "tags": course.get("tags", []),
            "instructor": {
                "id": instructor.get("id"),
                "name": instructor.get("name", "Unknown"),
                "max_hours": instructor.get("max_hours", 0),
                "expertise": instructor.get("expertise", [])
            },
            "room": {
                "id": room.get("id"),
                "name": room.get("room_name", "Unknown"),
                "type": room.get("type", "Unknown")
            },
            "day": assignment["day"],
            "time_start": assignment["time_start"],
            "time_end": assignment["time_end"]
        })

    print(json.dumps(schedule_list, indent=2))
