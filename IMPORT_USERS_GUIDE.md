# User Import Functionality Guide

## Overview

The User Import feature allows administrators to bulk import user accounts from an Excel file (XLSX format). This functionality supports importing faculty and staff members with their personal information, roles, and program assignments.

## Features

- ✅ Bulk import users from XLSX files
- ✅ Automatic program matching by name or code
- ✅ Email validation and duplicate detection
- ✅ Default password generation for new users
- ✅ Detailed error reporting for failed imports
- ✅ Drag-and-drop file upload
- ✅ Downloadable import template
- ✅ Real-time import progress tracking

## How to Use

### Step 1: Access the Import Feature

1. Navigate to the **User Accounts** page in the admin panel
2. Click the **"Import Users"** button (blue button with upload icon)

### Step 2: Download the Template (Optional)

1. In the import modal, click **"Download Template"**
2. This will download a sample XLSX file with the correct format and example data
3. Use this template as a reference for formatting your data

### Step 3: Prepare Your XLSX File

Your Excel file must include the following columns:

#### Required Columns:
- **Last Name**: User's last name (e.g., "Acdal")
- **First Name**: User's first name (e.g., "April")
- **Email**: User's email address (e.g., "acdal.april@dnsc.edu.ph")
- **Designation**: User's role (Options: "Faculty", "Admin", "Program Chairperson")

#### Optional Columns:
- **Program**: Program name or code (e.g., "BSDRM", "BSEDSCI", "BTLEd")
  - Must match an existing program in the system
  - Can match either the program name or program code
  - Case-insensitive matching

#### Example Data Format:

| Last Name    | First Name | Email                              | Designation | Program  |
|--------------|------------|-----------------------------------|-------------|----------|
| Acdal        | April      | acdal.april@dnsc.edu.ph           | Faculty     | BSDRM    |
| Anobong Jr.  | Anselmo    | anobong.jr..anselmo@dnsc.edu.ph   | Faculty     | BSEDSCI  |
| Balio        | Ariel      | balio.ariel.@dnsc.edu.ph          | Faculty     | BTLEd    |

### Step 4: Upload and Import

1. Click **"browse"** or drag-and-drop your XLSX file into the upload area
2. Verify the file name and size appear correctly
3. Click **"Import Users"** button
4. Wait for the import process to complete

### Step 5: Review Results

After import completion, you'll see:
- **Success count**: Number of users successfully imported
- **Failed count**: Number of users that failed to import
- **Error details**: Specific reasons for failed imports (if any)

## Default Settings

### Default Password
All imported users will have the default password:
```
Password123!
```
**Important:** Users should change their password upon first login.

### Institute Assignment
If a program is specified and found in the system, the user will be automatically assigned to that program's institute.

## Error Handling

The import system will flag the following issues:

### Common Errors:

1. **Missing Required Fields**
   - Error: "Missing required fields"
   - Solution: Ensure all required columns (Last Name, First Name, Email, Designation) have values

2. **Email Already Exists**
   - Error: "Email already exists"
   - Solution: The email is already registered. Update or remove the duplicate entry

3. **Invalid Email Format**
   - Error: Validation error
   - Solution: Ensure email follows proper format (e.g., user@domain.com)

4. **Program Not Found**
   - Note: This won't fail the import, but the user won't be assigned to a program
   - Solution: Verify program names/codes match existing programs in the system

## Technical Details

### Backend Endpoints

**POST** `/users/import-users`
- Accepts: multipart/form-data
- File parameter: `file`
- Returns: Import summary with success/failed counts and error details

### Column Mapping

The system supports multiple column name variations:
- "Last Name" or "last_name"
- "First Name" or "first_name"  
- "Email" or "email"
- "Designation" or "designation" or "role"
- "Program" or "program"

### Program Matching Logic

Programs are matched using case-insensitive comparison of:
1. Program Name (e.g., "Bachelor of Science in Data Resource Management")
2. Program Code (e.g., "BSDRM")

## Best Practices

1. **Test with Small Batches**: Start with a small file (5-10 users) to verify format
2. **Clean Data**: Remove empty rows and ensure consistent formatting
3. **Verify Programs**: Ensure program names/codes match exactly with existing programs
4. **Unique Emails**: Each email address must be unique across all users
5. **Backup First**: Consider exporting existing users before large imports

## Troubleshooting

### "File is empty or has no valid data"
- Check that your Excel file has data rows (not just headers)
- Verify the file isn't corrupted
- Try saving the file again in XLSX format

### "Please select a valid XLSX file"
- Ensure file extension is `.xlsx` (not `.xls` or `.csv`)
- Re-save the file in Excel as "Excel Workbook (.xlsx)"

### "Failed to process file"
- Check that column headers match expected names
- Verify there are no special characters in column names
- Ensure file isn't password-protected

## Support

For additional assistance:
1. Check the downloaded template for proper formatting
2. Verify your program names match existing programs in the system
3. Contact system administrator for program-specific issues

## Screenshots

### Import Button Location
The "Import Users" button (blue) is located next to the "Add Accounts" button on the User Accounts page.

### Import Modal
The modal provides:
- Instructions for file format
- Template download button
- Drag-and-drop upload area
- Progress tracking
- Detailed results display

---

**Last Updated**: November 2025  
**Version**: 1.0


