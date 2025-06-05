# ValidaSMTR - Student Record File Validator

A Python script that validates student record files (.avl format) containing CPF, student information, course data, and grades.

## Overview

ValidaSMTR validates structured text files containing student records with specific formatting requirements. The script performs comprehensive validation including CPF verification, data completeness checks, and format compliance.

## Usage

### Command Line
```bash
python validaSMTR.py <filename>
```

### Interactive Mode
```bash
python validaSMTR.py
```
The script will prompt for the filename if not provided as an argument.

## File Format Requirements

### File Structure
- Files must have `.avl` extension
- First line: Must match filename (without .avl extension)
- Subsequent lines: Student records with exactly 71 characters

### Record Format (71 characters per line)
```
Positions 0-10:  CPF (11 digits)
Positions 11-50: Student name (40 characters, cannot be blank)
Positions 51-66: Course start/end dates (16 characters)
Position 67:     Course type ('D' for online, 'P' for in-person)
Positions 68-70: Grade (3 digits, cannot be '000' or blank)
```

## Validation Rules

### CPF Validation
- Must be 11 digits
- Cannot be all identical digits (e.g., 11111111111)
- Must pass Brazilian CPF checksum algorithm

### Data Validation
- Lines cannot be blank
- Student names cannot be empty
- If course data exists, dates must be provided
- Course type must be 'D' (online) or 'P' (in-person)
- Grades cannot be '000' or blank

## Output

### Console Output
- Start/end processing messages
- Error count summary
- Success message if no errors found

### Analysis File
The script creates an analysis file named `analise_{original_filename}` containing:
- File encoding detection results
- Line-by-line validation results
- Detailed error descriptions for failed validations
- Success confirmations for valid lines

## Dependencies

- `chardet`: For automatic file encoding detection
- `sys`: For command line argument processing

## Examples

### Valid Record
```
12345678901JOÃO SILVA                     01/01/202301/06/2023D085
```

### Common Errors
- Invalid CPF: `11111111111MARIA SANTOS...`
- Wrong length: `12345678901JOSÉ` (too short)
- Missing course type: `12345678901ANA COSTA     01/01/202301/06/2023X085`
- Zero grade: `12345678901PEDRO LIMA     01/01/202301/06/2023D000`

## Error Messages

The script provides detailed Portuguese error messages including:
- Character count mismatches
- Invalid CPF formats
- Blank required fields
- Invalid course types
- Missing or invalid grades