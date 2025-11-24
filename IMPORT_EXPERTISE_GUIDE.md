# User Expertise Import Guide

## Overview

The User Expertise Import feature allows administrators to bulk import instructor-course expertise assignments from an Excel file (XLSX format). This links faculty members with courses they can teach.

## Features

- ✅ Bulk import expertise assignments from XLSX files
- ✅ Automatic instructor name matching (flexible formats)
- ✅ Course code validation and matching
- ✅ Duplicate detection (prevents duplicate assignments)
- ✅ Detailed error reporting for failed imports
- ✅ Drag-and-drop file upload
- ✅ Downloadable import template
- ✅ Real-time import progress tracking

## How to Use

### Step 1: Access the Import Feature

1. Navigate to the **User Accounts** page in the admin panel
2. Click the **"Import Expertise"** button (purple button)

### Step 2: Download the Template (Recommended)

1. In the import modal, click **"Download Template"**
2. This will download a sample XLSX file with the correct format and example data
3. Use this template as a reference for formatting your data

### Step 3: Prepare Your XLSX File

Your Excel file must include the following columns:

#### Required Columns:
- **Instructors Name**: Full name of the instructor (e.g., "Acdal, April M." or "April Acdal")
- **Course Code**: The course code (e.g., "RR325", "ER327", "GEELECT1")

#### Example Data Format:

| Instructors Name        | Course Code |
|------------------------|-------------|
| Acdal, April M.        | RR325       |
| Acdal, April M.        | ER327       |
| Anobong Jr., Anselmo G.| GEELECT1    |
| Balio, Ariel, Jr. C.   | THE223      |
| Bangasin, Alneza M.    | LIT121      |

#### Name Format Support:
The system supports multiple name formats:
- "Last Name, First Name" (e.g., "Acdal, April")
- "First Name Last Name" (e.g., "April Acdal")
- With middle initials (e.g., "Acdal, April M.")
- With suffixes (e.g., "Balio, Ariel, Jr. C.")

### Step 4: Upload and Import

1. Click **"browse"** or drag-and-drop your XLSX file into the upload area
2. Verify the file name and size appear correctly
3. Click **"Import Expertise"** button
4. Wait for the import process to complete

### Step 5: Review Results

After import completion, you'll see:
- **Success count**: Number of expertise records successfully imported
- **Failed count**: Number of records that failed to import
- **Error details**: Specific reasons for failed imports (if any)

## Important Notes

### Instructor Matching
- Instructors must already exist in the system
- Name matching is case-insensitive and flexible
- The system tries multiple name format variations
- If an instructor is not found, the row will fail with an error

### Course Matching
- Courses must already exist in the system
- Course codes are matched case-insensitively
- Course codes must exactly match the `course_code` in the database

### Duplicate Prevention
- The system automatically checks for existing expertise assignments
- If an instructor is already assigned to a course, that row will be skipped
- Duplicates are reported in the error list

## Error Handling

The import system will flag the following issues:

### Common Errors:

1. **Missing Required Fields**
   - Error: "Missing required fields"
   - Solution: Ensure both Instructors Name and Course Code have values

2. **Instructor Not Found**
   - Error: "Instructor not found: [Name]"
   - Solution: Verify the instructor exists in the system and the name spelling matches

3. **Course Not Found**
   - Error: "Course not found: [Course Code]"
   - Solution: Verify the course exists and the course code matches exactly

4. **Expertise Already Exists**
   - Error: "Expertise already exists for [Instructor] - [Course Code]"
   - Solution: This assignment already exists in the database

## Technical Details

### Backend Endpoint

**POST** `/users/import-expertise`
- Accepts: multipart/form-data
- File parameter: `file`
- Returns: Import summary with success/failed counts and error details

### Column Mapping

The system supports multiple column name variations:
- "Instructors Name" or "Instructor Name" or "instructor_name" or "Instructor"
- "Course Code" or "course_code" or "Code"

### Matching Logic

#### Instructor Name Matching:
The system performs fuzzy matching to find instructors:
1. Exact match: "Last Name, First Name"
2. Contains match (partial name)
3. Reverse format: "First Name Last Name"
4. Case-insensitive comparison

#### Course Code Matching:
- Exact match (case-insensitive)
- Uppercase conversion for consistency

## Database Structure

### user_expertise Table:
- `id`: Primary key (auto-increment)
- `user_id`: Foreign key to user_accounts table
- `course_id`: Foreign key to courses table

### Relationships:
- Each expertise record links one user to one course
- Cascade delete: If user or course is deleted, expertise is also deleted
- Multiple expertise records allowed per user (one per course)

## Best Practices

1. **Test with Small Batches**: Start with a small file (5-10 records) to verify format
2. **Clean Data**: Remove empty rows and ensure consistent formatting
3. **Verify Names**: Ensure instructor names match exactly with database records
4. **Check Course Codes**: Verify course codes exist in the system
5. **Avoid Duplicates**: Check if expertise already exists before importing
6. **Use Template**: Always start with the downloaded template

## Example Use Cases

### Scenario 1: New Semester Setup
Import all faculty expertise assignments at the beginning of a new semester.

### Scenario 2: Bulk Assignment
Assign multiple courses to multiple instructors in one operation.

### Scenario 3: Data Migration
Transfer expertise data from another system or spreadsheet.

## Troubleshooting

### "Instructor not found" errors
**Possible causes:**
- Instructor name spelling doesn't match database
- Instructor not yet created in the system
- Extra spaces or special characters in name

**Solutions:**
- Verify instructor exists in User Accounts
- Check name spelling and format
- Remove extra spaces or special characters

### "Course not found" errors
**Possible causes:**
- Course code doesn't exist in the system
- Typo in course code
- Case sensitivity issues (shouldn't happen, but check)

**Solutions:**
- Verify course exists in Courses section
- Check course code spelling
- Ensure no extra spaces

### "File is empty or has no valid data"
**Possible causes:**
- Excel file has no data rows
- Only header row present
- File is corrupted

**Solutions:**
- Add at least one data row below headers
- Verify file isn't corrupted
- Re-save file in XLSX format

### Import is slow
**Note:** Large imports may take time as each record is validated and checked for duplicates.

**Tips:**
- Break large files into smaller batches
- Import during off-peak hours
- Be patient with files containing hundreds of records

## User Interface

### Import Button Location
The **"Import Expertise"** button (purple) is located on the User Accounts page, positioned between the "Import Users" and "Add Accounts" buttons.

### Import Modal Features
- **Instructions panel**: Clear import guidelines
- **Template download**: Quick access to sample file
- **Drag-and-drop upload area**: Easy file selection
- **Progress bar**: Visual feedback during import
- **Results display**: Success/failure summary with detailed error list

## Support

For additional assistance:
1. Download and examine the template file
2. Verify instructor and course data in the system
3. Test with a small subset of data first
4. Contact system administrator for database-related issues

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Feature Status**: Complete ✅


