# Quick Start: Import Users Feature

## 🎯 What Was Built

A complete XLSX import system to bulk-create user accounts with program assignments.

## 📁 XLSX File Format

Your Excel file should have these columns:

```
┌─────────────┬────────────┬──────────────────────────────┬─────────────┬─────────┐
│ Last Name   │ First Name │ Email                        │ Designation │ Program │
├─────────────┼────────────┼──────────────────────────────┼─────────────┼─────────┤
│ Acdal       │ April      │ acdal.april@dnsc.edu.ph      │ Faculty     │ BSDRM   │
│ Anobong Jr. │ Anselmo    │ anobong.jr.anselmo@dnsc.edu │ Faculty     │ BSEDSCI │
│ Balio       │ Ariel      │ balio.ariel@dnsc.edu.ph      │ Faculty     │ BTLEd   │
└─────────────┴────────────┴──────────────────────────────┴─────────────┴─────────┘
```

## 🚀 How to Use (3 Steps)

### 1️⃣ Open Import Modal
- Go to **User Accounts** page
- Click **"Import Users"** (blue button)

### 2️⃣ Download Template (Optional)
- Click **"Download Template"** in modal
- Use it as a reference for your data

### 3️⃣ Upload & Import
- Drag-drop or browse your XLSX file
- Click **"Import Users"**
- Review results

## ✅ What Happens

1. **Email Validation**: Checks for valid format
2. **Duplicate Check**: Prevents duplicate emails
3. **Program Matching**: Links users to their programs
4. **Password Creation**: Sets default password (`Password123!`)
5. **Result Report**: Shows success/failures with details

## 🎨 UI Features

### Import Button
```
┌──────────────────────────────────────────────────────┐
│  📥 Import Users  |  ➕ Add Accounts                  │
│  (Blue Button)    |  (Green Button)                   │
└──────────────────────────────────────────────────────┘
```

### Import Modal
```
┌─────────────────────────────────────────────────────┐
│ 📤 Import Users                              ✕      │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ℹ️ Instructions:                                     │
│   • File must be XLSX format                        │
│   • Required: Last Name, First Name, Email, Role    │
│   • Optional: Program                               │
│   • Default password: Password123!                  │
│                                                      │
│  ┌────────────────────────────────┐                │
│  │  📥 Download Template          │                │
│  └────────────────────────────────┘                │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  📄 Drag & drop XLSX file here            │    │
│  │       or browse                            │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ✅ Successfully imported 25 users                  │
│  ❌ Failed: 2 users (see details below)            │
│                                                      │
│  [ Cancel ]              [ Import Users ]          │
└─────────────────────────────────────────────────────┘
```

## 📊 Results Display

### Success
```
✓ Successfully imported 25 users
```

### Errors (if any)
```
✗ Failed to import 2 users

Row 5: Email already exists
Email: duplicate@example.com

Row 12: Missing required fields
```

## 🔐 Default Password

All imported users get:
```
Password123!
```
*(Users should change on first login)*

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| "Email already exists" | Remove/update duplicate emails |
| "Missing required fields" | Fill all required columns |
| "File format invalid" | Save as `.xlsx` (not `.xls` or `.csv`) |
| "Program not found" | Check program name/code spelling |

## 📦 What Was Implemented

### Backend
- ✅ POST endpoint: `/users/import-users`
- ✅ XLSX parsing
- ✅ Email validation & duplicate checking
- ✅ Program auto-matching
- ✅ Default password hashing
- ✅ Detailed error reporting

### Frontend
- ✅ Import button on User Accounts page
- ✅ Import modal with drag-drop
- ✅ Template download feature
- ✅ Progress tracking
- ✅ Results display
- ✅ Toast notifications

## 🧪 Test It

1. Download the template
2. Edit the sample data
3. Import the file
4. Check the User Accounts table
5. Try logging in with imported user (password: `Password123!`)

## 📝 Notes

- Program names must match existing programs in the system
- Institute is auto-assigned based on program
- Import is atomic per user (one failure doesn't affect others)
- All columns are case-insensitive

## 📚 More Details

For detailed documentation, see:
- `IMPORT_USERS_GUIDE.md` - Complete user guide
- `IMPORT_IMPLEMENTATION_SUMMARY.md` - Technical details

---

**Ready to use!** 🎉


