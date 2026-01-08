# Score-assignment-converter
A subject score conversion tool for students and teachers in Zhejiang Province, which supports uploading raw score tables and score assignment rule tables to automatically complete score conversion and generate result files.

> Chinese Version: [README.md](README.md)

## 1. System Introduction
### Key Features
- Support uploading raw score tables and score assignment rule tables in Excel (.xlsx) and CSV (.csv) formats
- Automatically calculate the assigned score for each student's subject and count the total assigned score
- Customize the insertion position of assigned score columns (after the corresponding subject / at the end of the table)
- Generate uniquely named result files to avoid overwriting
- User-friendly web interface with simple and intuitive operation
- Provide test data generation tools for quick function verification

### Technology Stack
- Backend: Python + Flask
- Data Processing: Pandas
- Frontend: HTML + CSS
- Dependencies: openpyxl (Excel processing), Faker (test data generation)

## 2. Environment Preparation
### 1. Install Python Environment
Ensure Python 3.7 or above is installed (Python 3.8-3.10 is recommended).

### 2. Install Dependencies
```bash
pip install flask pandas openpyxl faker
```

## 3. Usage Instructions
### 1. Start the System
```bash
# Enter the project root directory (Score Assignment Program folder)
cd 赋分程序

# Run the Flask application
python app.py
```
After startup, access `http://localhost:5000` in your browser to enter the system page.

### 2. Operation Steps
#### Step 1: Prepare Table Files
- **Raw Score Table**: Must include column names (Name, Physics, Chemistry, Biology, Politics, History, Geography, Technology, etc.). Leave blank for empty values. Supported formats: .xlsx/.csv.
- **Score Assignment Rule Table**: The first column is fixed as "Assigned Score", other columns are subject names (consistent with the raw table). Each row value is the minimum raw score requirement for the corresponding assigned score. Supported formats: .xlsx/.csv.

#### Step 2: Upload Files and Configure
1. Upload the "Raw Score Table" and "Score Assignment Rule Table" on the system page
2. Select the insertion position of assigned score columns:
   - Insert after the corresponding subject column: Each assigned score column follows the original column of the subject
   - Append to the end of the table: All assigned score columns are uniformly placed at the end of the table
3. Click the "Start Score Assignment and Generate File" button

#### Step 3: Download Result File
The system automatically calculates the assigned scores and generates a downloadable file. The file name format is: `赋分结果表_YYYYMMDD_HHMMSS.xlsx`. After downloading, you can view:
- The assigned score corresponding to the raw score of each subject
- Statistics of the total score of all valid assigned scores

### 3. Generate Test Data (Quick Verification)
The project provides a test data generation tool to quickly generate simulated raw score tables for testing system functions:
```bash
# Enter the testfile directory
cd 赋分程序/testfile

# Run the test data generation script
python generate_test_data.py
```
#### Generation Rule Description
- Randomly generate information for 50 students (Chinese names)
- Each student randomly selects 3 subjects to generate scores (covering 0-100 points, divided into three levels: low/medium/high)
- The generated file name is: `原始分数表_RandomString.xlsx` (ensuring uniqueness)
- After generation, the file can be uploaded as the "Raw Score Table" and used with a custom "Score Assignment Rule Table" to test the score assignment function

## 4. Table Format Specifications
### 1. Example of Raw Score Table
| Name  | Physics | Chemistry | Biology | Politics | History | Geography | Technology |
|-------|---------|-----------|---------|----------|---------|-----------|------------|
| Zhang San | 85.5   |           | 78.2    |          |         |           |            |
| Li Si   |         | 62.0      |         | 88.8     |         |           |            |
| Wang Wu  | 45.3   | 56.7      | 90.1    |          |         |           |            |

### 2. Example of Score Assignment Rule Table
| Assigned Score | Physics | Chemistry | Biology | Politics | History | Geography | Technology |
|---------------|---------|-----------|---------|----------|---------|-----------|------------|
| 100           | 95      | 94        | 96      | 95       | 93      | 94        | 95         |
| 97            | 90      | 89        | 91      | 90       | 88      | 89        | 90         |
| 94            | 85      | 84        | 86      | 85       | 83      | 84        | 85         |
| 91            | 80      | 79        | 81      | 80       | 78      | 79        | 80         |
| ...           | ...     | ...       | ...     | ...      | ...     | ...       | ...        |
| 40            | 0       | 0         | 0       | 0        | 0       | 0         | 0          |

**Explanation**: In the score assignment rule table, the "Assigned Score" of each row corresponds to the score obtained when the subject reaches the "Minimum Raw Score". The system will match the highest assigned score where the raw score ≥ the minimum raw score.

## 5. Frequently Asked Questions
1. **File upload failed**: Check the file size (≤10MB) and format (only .xlsx/.csv are supported), and ensure the file is not damaged.
2. **Score assignment calculation is empty**: Confirm that the subject names in the score assignment rule table are consistent with the raw table, and the raw scores must be in numeric format (avoid text/special characters).
3. **Page unresponsive**: Check if the Flask service is running normally and if there are error messages in the browser console.
4. **Test data generation failed**: Ensure the Faker library is installed (`pip install faker`) and the Python environment is normal.

## 6. Directory Structure
```
赋分程序/
├── app.py              # Flask application entry
├── config.py           # System configuration (secret key, file limits, paths, etc.)
├── score_processor.py  # Core score assignment calculation logic
├── utils.py            # Tool functions (generate unique file names)
├── README.md           # Project documentation (Chinese)
├── README_EN.md        # Project documentation (English)
├── static/             # Static resources (CSS)
│   └── css/
│       └── style.css
├── templates/          # Frontend templates
│   └── index.html
└── testfile/           # Test-related files
    └── generate_test_data.py  # Test data generation script
```