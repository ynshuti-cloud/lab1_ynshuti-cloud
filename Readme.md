# Lab 1: Grade Evaluator & Archiver

## Project Overview

This project automates the process of grading a student's coursework and
keeping the grading workspace organized between batches. It's made up of 
two
parts that work together: a Python program that reads a CSV of assignment
scores and classifies the student's overall academic standing, and a Bash
script that archives that CSV once grading is done so a fresh one is ready
for the next batch of grades.

## Files

- `grade-evaluator.py` — reads `grades.csv`, validates it, calculates the
  final grade/GPA, classifies the student as Pass or Fail, and reports any
  formative assignments eligible for resubmission.
- `organizer.sh` — archives the current `grades.csv` with a timestamp, 
creates
  a fresh `grades.csv` (header row only), and logs the action to
  `organizer.log`.
- `grades.csv` — the source data (assignment, group, score, weight).

## How the Script and Python File Work Together

The two files form a simple pipeline built around one shared file,
`grades.csv`:

1. `grade-evaluator.py` reads and classifies whatever is currently in
   `grades.csv`, printing the results to the terminal.
2. Once that batch has been reviewed, `organizer.sh` is run to close it 
out —
   it moves the used `grades.csv` into `archive/` under a timestamped 
name,
   and puts a new, empty `grades.csv` (with just the header row) back in 
its
   place.
3. Because the reset file already has the header row, the next batch of
   grades can be typed straight in without needing to recreate the CSV
   structure — `grade-evaluator.py` is ready to run again immediately.
4. Every run of `organizer.sh` is recorded in `organizer.log`, so there's 
a
   running history of which `grades.csv` was archived as which file, and
   when.

In short: `grade-evaluator.py` handles evaluating a batch, and 
`organizer.sh`
handles closing it out and preparing the workspace for the next one — 
neither
file touches the other's job.

## What `grade-evaluator.py` Does

The program takes the CSV filename (either typed in when prompted, or 
passed
as a command-line argument) and reads every row into memory, converting 
the
score and weight columns into numbers.

It then classifies the student's grade in a series of checks:

**1. Score validation** — every score must fall between 0 and 100. If any
assignment fails this, the program stops and reports which one.

**2. Weight validation** — the weights must add up to exactly 100 overall,
with Formative assignments totaling exactly 60 and Summative assignments
totaling exactly 40. If any of these don't match, the program stops and
reports which rule failed.

**3. Grade and GPA calculation** — each assignment's contribution to the
final grade is `(score × weight) / 100`. These are summed into a Formative
total, a Summative total, and an overall Final Grade, from which the GPA 
is
derived as `GPA = (Final Grade / 100) × 5.0`.

**4. Pass/Fail classification** — the program calculates what percentage 
of
the *possible* Formative and Summative marks were actually earned. A 
student
is classified as **PASSED** only if both percentages are at least 50%;
otherwise, **FAILED**.

**5. Resubmission eligibility** — separately from the pass/fail decision, 
any
Formative assignment scoring below 50 is flagged. Among those, only the 
one(s)
with the highest weight are listed as eligible for resubmission, since 
those
matter most to the final grade.

## Requirements

- Python 3
- Bash (Linux/macOS terminal, or WSL/Git Bash on Windows)

## Running the Python Application

1. Make sure `grades.csv` is in the same folder as `grade-evaluator.py`.
2. Run:

   ```bash
   python3 grade-evaluator.py
   ```

3. When prompted, type the CSV filename (e.g. `grades.csv`) and press 
Enter.
4. The script will print:
   - The Formative and Summative category scores
   - The overall Final Grade
   - The final GPA (on a 5.0 scale)
   - The final status: `PASSED` or `FAILED`
   - Any formative assignment(s) eligible for resubmission

## Running the Shell Script

1. Make the script executable (only needed once):

   ```bash
   chmod +x organizer.sh
   ```

2. Run it from the folder containing `grades.csv`:

   ```bash
   ./organizer.sh
   ```

3. What it does:
   - Creates an `archive/` folder if it doesn't already exist.
   - Renames the current `grades.csv` with a timestamp (e.g.
     `grades_20260720-093033.csv`) and moves it into `archive/`.
   - Creates a new `grades.csv` (header row only) so it's ready for the 
next
     batch of grades.
   - Appends a line to `organizer.log` recording the timestamp, original
     filename, and archived filename for that run.

## Typical Workflow

```bash
# 1. Evaluate the current batch of grades
python3 grade-evaluator.py
# -> enter: grades.csv

# 2. Archive that batch and reset the workspace
./organizer.sh

# 3. Fill the new grades.csv with the next batch, then repeat
```

## Author

Name: Nshuti Yakim
