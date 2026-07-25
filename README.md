# pmfby_automation

# PMFBY Bulk Uploader

## Overview

PMFBY Bulk Uploader is a desktop automation application developed for Andhra Pradesh Grameena Bank to automate the creation of crop insurance policies in the Pradhan Mantri Fasal Bima Yojana (PMFBY) portal.

The application reads crop loan data from a predefined Excel template, performs all required validations, automatically fills the PMFBY portal using Playwright browser automation, and generates detailed reports and execution logs for verification and audit purposes.

The objective of this project is to eliminate repetitive manual data entry, reduce human errors, improve processing speed, and provide complete traceability of every uploaded record.

---

# Features

- Secure login to PMFBY Portal
- Excel based bulk upload
- Automatic Aadhaar verification
- Automatic location selection
- Automatic crop details entry
- Automatic land verification
- Automatic preview generation
- Automatic policy submission
- Automatic navigation back to KCC Beneficiary page
- Handles multiple survey numbers
- Handles validation failures gracefully
- Automatic recovery from common failures
- Generates Excel execution report
- Generates detailed execution logs
- User friendly desktop interface (Tkinter)
- Portable Windows executable (.exe)

---

# Project Structure

```
pmfby_automation/

│
├── processors/          # Business Processors
├── workers/             # Background Workers
├── ui/                  # Tkinter User Interface
├── templates/           # Excel Templates
├── reports/             # Generated Reports
├── logs/                # Execution Logs
├── main.py              # Application Entry Point
├── requirements.txt
└── README.md
```

---

# Workflow

```
Login

↓

Select Scheme & Branch

↓

Read Excel

↓

Search Account

↓

Create Policy

↓

Verify Aadhaar

↓

Select Location

↓

Enter Crop Details

↓

Verify Land Records

↓

Preview Policy

↓

Final Submission

↓

Generate Report & Logs
```

---

# Reports Generated

The application generates detailed reports after every execution.

## Excel Report

Location:

```
reports/
```

Example:

```
PMFBY_Report_20260724_104500.xlsx
```

The report contains:

- Account Number
- Crop
- Khata Number
- Survey Number
- Farmer Name
- Father / Husband Name
- Individual Area
- Total Area
- Processing Status
- Error Message (if any)

---

## Execution Log

Location:

```
logs/
```

Contains:

- Complete execution history
- Processing milestones
- Validation failures
- Navigation details
- Exception details
- Final upload summary

Useful for troubleshooting and audit verification.

---

# Excel Template

Users can download the latest template directly from the application.

Template Location:

```
templates/
```

---

# Technology Stack

- Python 3.12+
- Playwright
- Tkinter
- OpenPyXL
- PyInstaller

---

# Installation (Development)

## 1. Clone Project

```bash
git clone <repository-url>

cd pmfby_automation
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

Command Prompt

```bash
venv\Scripts\activate
```

PowerShell

```powershell
Set-ExecutionPolicy -Scope Process Bypass

.\venv\Scripts\Activate.ps1
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Install Playwright Browser

```bash
playwright install chromium
```

---

## 6. Run Application

```bash
python main.py
```

---

# Build Executable

```bash
pyinstaller PmfbyAutoLoader.spec
```

Generated executable:

```
dist/
    PmfbyAutoLoader/
```

Distribute only the **PmfbyAutoLoader** folder.

---

# Usage

1. Launch the application.
2. Login using PMFBY credentials.
3. Complete CAPTCHA and OTP verification.
4. Select Scheme and Branch.
5. Download the Excel template (if required).
6. Fill the template with crop loan details.
7. Select the Excel file.
8. Click Validate.
9. Click Upload.
10. Review the generated report after completion.

---

# Error Handling

The application automatically handles:

- Invalid accounts
- Aadhaar verification failures
- Duplicate mobile validation
- Land verification failures
- Missing survey numbers
- Navigation failures
- Browser recovery
- Unexpected exceptions

Processing continues with the next account whenever possible.

---

# Notes

- Do not modify the Excel template structure.
- Ensure PMFBY portal is accessible before starting.
- Reports are generated automatically after every execution.
- Generated reports should be verified before reconciliation.
- Users should extract the ZIP completely before running the executable.
- Do not run the executable directly from inside the ZIP archive.

---

# Requirements

- Windows 10 / Windows 11
- Internet Connection
- PMFBY User Credentials
- Chromium Browser (bundled with the executable)

---

# Dependencies

```
playwright
openpyxl
pyinstaller
```

---

# License

Internal Application

Developed for

**Andhra Pradesh Grameena Bank**

This software is intended exclusively for internal banking operations and is not intended for public distribution.

---

# Author

Developed by

**Siva Kumar Reddy**

In-House Web Developer

Andhra Pradesh Grameena Bank
