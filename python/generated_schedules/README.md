# Generated Schedules Directory

This directory contains automatically generated faculty loading schedules created by the Genetic Algorithm.

## Files Generated

After each run of `faculty_ga_jhomel_v2.py`, two files are created with timestamps:

### 1. Text Schedule (`schedule_YYYYMMDD_HHMMSS.txt`)
- **Format**: Human-readable text format
- **Contents**: Complete faculty loading schedule with:
  - Day-by-day breakdown
  - Faculty assignments with courses and rooms
  - Time slots and durations
  - Fitness score and generation statistics

### 2. JSON Schedule (`schedule_YYYYMMDD_HHMMSS.json`)
- **Format**: JSON format for backend integration
- **Contents**: Structured data including:
  - All course assignments
  - Faculty, room, and time slot mappings
  - Ready for import into the database via the backend API

## File Naming Convention

```
schedule_20241120_143022.txt   ← Generated on Nov 20, 2024 at 14:30:22
schedule_20241120_143022.json  ← Corresponding JSON file
```

## Usage

### For Review
Open the `.txt` file to review the generated schedule in a readable format.

### For Backend Import
Use the `.json` file to import the schedule into your system:
1. Locate the desired JSON file
2. Import via backend API or manual database insertion
3. Verify the schedule in your frontend interface

## Notes

- Files are automatically created in this directory
- Each run creates a new timestamped file (no overwrites)
- Old schedules are preserved for comparison
- You can safely delete old files if no longer needed


