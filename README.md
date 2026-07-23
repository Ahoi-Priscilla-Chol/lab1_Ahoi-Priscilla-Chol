# Lab 1: Grade Evaluator & Archiver

This project calculates a student's final academic standing from a CSV
of course grades, and includes a shell script that archives grade data
and resets the workspace for the next batch of grades.

## Files

- `grade-evaluator.py` - Reads `grades.csv`, validates the data, and
  calculates the Final Grade, GPA, Pass/Fail status, and any
  resubmission requirements.
- `organizer.sh` - Archives the current `grades.csv` with a timestamp,
  resets `grades.csv` to an empty file, and logs the action to
  `organizer.log`.
- `grades.csv` - The current batch of grade data (assignment, group,
  score, weight).

## Running grade-evaluator.py

Run the script with Python 3, optionally passing the CSV filename as
an argument:

    python3 grade-evaluator.py grades.csv

If you don't pass a filename, the script will prompt you for one
interactively:

    python3 grade-evaluator.py
    Enter the name of the CSV file to process (e.g., grades.csv): grades.csv

The script will validate the scores (must be between 0-100) and weights
(must total 100, split 60 Formative / 40 Summative), then print the
Final Grade, GPA, category averages, and Pass/Fail result. If the
student fails, it lists which failed Formative assignment(s) (the
highest-weight one, including ties) should be resubmitted.

## Running organizer.sh

Make sure the script is executable, then run it:

    chmod +x organizer.sh
    ./organizer.sh

Each run will:

1. Create an `archive/` directory if one doesn't already exist.
2. Move the current `grades.csv` into `archive/` with a timestamped
   filename, e.g. `grades_20260723-090014.csv`.
3. Create a new, empty `grades.csv` in the current directory.
4. Append a log entry to `organizer.log` recording the timestamp,
   original filename, and archived filename.
