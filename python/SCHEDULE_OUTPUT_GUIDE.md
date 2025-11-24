# Schedule Output Guide

## Overview

The genetic algorithm (`faculty_ga_jhomel_v2.py`) now automatically saves generated schedules to files in the `generated_schedules/` directory.

## What Gets Saved

After each run, two timestamped files are created:

### 1. Text File (`schedule_YYYYMMDD_HHMMSS.txt`)
**Purpose**: Human-readable schedule for review

**Contains**:
- Complete day-by-day schedule
- Faculty assignments with courses
- Room allocations
- Time slots and durations
- Fitness score and statistics
- Generation timestamp

**Example Filename**: `schedule_20241120_153045.txt`

### 2. JSON File (`schedule_YYYYMMDD_HHMMSS.json`)
**Purpose**: Machine-readable format for backend import

**Contains**:
- Structured assignment data
- Faculty, room, and time mappings
- Ready for database insertion via backend API

**Example Filename**: `schedule_20241120_153045.json`

## File Location

```
GA-Faculty-Loading/
└── python/
    ├── faculty_ga_jhomel_v2.py
    └── generated_schedules/
        ├── README.md
        ├── schedule_20241120_143022.txt
        ├── schedule_20241120_143022.json
        ├── schedule_20241120_153045.txt
        └── schedule_20241120_153045.json
```

## How to Use

### Step 1: Run the Algorithm
```bash
python python/faculty_ga_jhomel_v2.py
```

### Step 2: Check Console Output
The script will display:
- Progress bars for population creation and evolution
- Generation-by-generation fitness updates
- ETA (estimated time remaining)
- File save confirmation at the end

### Step 3: Find Your Files
Look in `python/generated_schedules/` for the latest files (sorted by timestamp).

### Step 4: Review the Schedule
Open the `.txt` file in any text editor to review the human-readable schedule.

### Step 5: Import to Backend (Optional)
Use the `.json` file to import the schedule into your system via the backend API.

## File Management

### Automatic Features
- ✅ Automatic directory creation (no setup needed)
- ✅ Timestamped filenames (no overwrites)
- ✅ UTF-8 encoding (supports all characters)
- ✅ JSON formatted for easy parsing

### Manual Cleanup
Old files are preserved for comparison. To clean up:
```bash
# Delete all generated files (keep README)
cd python/generated_schedules
rm schedule_*.txt schedule_*.json
```

## Console Output

After the algorithm completes, you'll see:

```
============================================================
FILES SAVED SUCCESSFULLY!
============================================================
Text Schedule: python/generated_schedules/schedule_20241120_153045.txt
JSON Schedule: python/generated_schedules/schedule_20241120_153045.json
============================================================
```

## Troubleshooting

### Files Not Created
- **Check**: Ensure the script completed successfully
- **Fix**: Look for error messages in console output

### Permission Errors
- **Issue**: Cannot write to directory
- **Fix**: Run with appropriate permissions or check folder permissions

### Encoding Errors
- **Issue**: Special characters not displaying correctly
- **Fix**: Open files with UTF-8 encoding support

## Performance Notes

With **1913 teaching requirements**:
- **Population Size**: 50
- **Generations**: 100  
- **Estimated Time**: 5-15 minutes (depends on hardware)
- **Initial Fitness**: May start at 0.00 (normal for large datasets)
- **Final Fitness**: Should increase to 100+ by end

## Next Steps

1. **Review** the `.txt` file to verify the schedule
2. **Test** by importing the `.json` into your backend
3. **Compare** multiple runs to find the best schedule
4. **Archive** good schedules for future reference


