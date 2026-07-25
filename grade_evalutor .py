#!/usr/bin/python3
import csv
import sys
import os
 
# Grading policy: these define what counts as a valid, well-formed grade sheet.
REQUIRED_TOTAL_WEIGHT = 100
REQUIRED_FORMATIVE_WEIGHT = 60
REQUIRED_SUMMATIVE_WEIGHT = 40
PASSING_THRESHOLD = 50
 
 
def load_csv_data():
    """
    Prompts the user for a filename (or accepts it as a command-line argument),
    checks if it exists, and extracts all fields into a list of dictionaries.
    """
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
 
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
 
    assignments = []
 
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    assignments.append({
                        'assignment': row['assignment'],
                        'group': row['group'],
                        'score': float(row['score']),
                        'weight': float(row['weight'])
                    })
                except KeyError as missing_column:
                    print(f"Error: CSV is missing expected column {missing_column}.")
                    sys.exit(1)
                except ValueError:
                    print(f"Error: '{row.get('assignment', 'unknown assignment')}' has a non-numeric score or weight.")
                    sys.exit(1)
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)
 
 
def evaluate_grades(data):
    """
    Validates and scores a list of assignment records.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
 
    if not data:
        print("Error: No assignment records found. The CSV file is empty.")
        return
 
    total_weight = 0
    formative_weight = 0
    summative_weight = 0
 
    final_grade = 0
 
    formative_marks = 0
    summative_marks = 0
 
    failed_formative = []
 
    for assignment in data:
        score = assignment["score"]
        weight = assignment["weight"]
        group = assignment["group"]
 
        if score < 0 or score > 100:
            print(f"Error: '{assignment['assignment']}' has an invalid score of {score}.")
            return
 
        contribution = (score * weight) / 100
        final_grade += contribution
 
        total_weight += weight
 
        if group == "Formative":
            formative_weight += weight
            formative_marks += contribution
 
            if score < PASSING_THRESHOLD:
                failed_formative.append(assignment)
 
        elif group == "Summative":
            summative_weight += weight
            summative_marks += contribution
 
        else:
            print(f"Warning: '{assignment['assignment']}' has an unrecognized group '{group}' "
                  f"(expected 'Formative' or 'Summative'). It will not count toward weight totals.")
 
    print("All scores are valid!")
 
    print(f"Total Weight: {total_weight}")
    print(f"Formative Weight: {formative_weight}")
    print(f"Summative Weight: {summative_weight}")
 
    if total_weight != REQUIRED_TOTAL_WEIGHT:
        print(f"Error: Total assignment weight must equal {REQUIRED_TOTAL_WEIGHT}.")
        return
 
    if formative_weight != REQUIRED_FORMATIVE_WEIGHT:
        print(f"Error: Formative assignments must total {REQUIRED_FORMATIVE_WEIGHT}.")
        return
 
    if summative_weight != REQUIRED_SUMMATIVE_WEIGHT:
        print(f"Error: Summative assignments must total {REQUIRED_SUMMATIVE_WEIGHT}.")
        return
 
    print("Weight validation passed!")
    print(f"\nFormative marks: {formative_marks:.2f}")
    print(f"Summative marks: {summative_marks:.2f}")
    print(f"Final Grade: {final_grade:.2f}%")
 
    gpa = (final_grade / 100) * 5.0
    print(f"GPA: {gpa:.2f}")
 
    formative_percentage = (formative_marks / formative_weight) * 100
    summative_percentage = (summative_marks / summative_weight) * 100
 
    print(f"\nFormative Percentage: {formative_percentage:.2f}%")
    print(f"Summative Percentage: {summative_percentage:.2f}%")
 
    if formative_percentage >= PASSING_THRESHOLD and summative_percentage >= PASSING_THRESHOLD:
        print("Status: PASSED")
    else:
        print("Status: FAILED")
 
    print("\nFailed Formative Assignments:")
 
    for assignment in failed_formative:
        print(
            f"{assignment['assignment']} "
            f"(Score: {assignment['score']}, Weight: {assignment['weight']})"
        )
 
    if len(failed_formative) == 0:
        print("\nNo formative assignments require resubmission.")
 
    else:
        highest_weight = failed_formative[0]["weight"]
 
        for assignment in failed_formative:
            if assignment["weight"] > highest_weight:
                highest_weight = assignment["weight"]
 
        print("\nAssignment(s) eligible for resubmission:")
 
        for assignment in failed_formative:
            if assignment["weight"] == highest_weight:
                print(
                    f"- {assignment['assignment']} "
                    f"(Score: {assignment['score']}, Weight: {assignment['weight']})"
                )
 
 
if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
 
    # 2. Process the features
    evaluate_grades(course_data)

