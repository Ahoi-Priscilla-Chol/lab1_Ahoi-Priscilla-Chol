import csv
import sys
import os


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input(
        "Enter the name of the CSV file to process (e.g., grades.csv): "
    )

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row.get('assignment') or not row.get('group'):
                    print("Warning: Skipping a row with missing fields.")
                    continue
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Evaluates a list of assignment dictionaries: validates scores and
    weights, computes the final grade and GPA, determines pass/fail
    per category, and flags resubmission targets when applicable.
    """
    print("\n--- Processing Grades ---")

    if not data:
        print("Error: No assignment data to process.")
        return

    invalid_scores = [d for d in data if not (0 <= d['score'] <= 100)]
    if invalid_scores:
        names = ", ".join(d['assignment'] for d in invalid_scores)
        print(f"Error: These assignments have scores outside 0-100: {names}")
        return

    formative = [d for d in data if d['group'] == 'Formative']
    summative = [d for d in data if d['group'] == 'Summative']

    formative_weight = sum(d['weight'] for d in formative)
    summative_weight = sum(d['weight'] for d in summative)
    total_weight = formative_weight + summative_weight

    if total_weight != 100 or formative_weight != 60 or summative_weight != 40:
        print(
            "Warning: Weights do not match the expected split "
            "(Total=100, Formative=60, Summative=40). "
            "Using actual weights for calculation."
        )

    if formative_weight == 0 or summative_weight == 0:
        print("Error: Missing Formative or Summative data; cannot evaluate.")
        return

    weighted_sum = sum(d['score'] * d['weight'] for d in data)
    final_grade = weighted_sum / total_weight
    gpa = (final_grade / 100) * 5.0

    formative_pct = (
        sum(d['score'] * d['weight'] for d in formative) / formative_weight
    )
    summative_pct = (
        sum(d['score'] * d['weight'] for d in summative) / summative_weight
    )

    print(f"Final Grade: {final_grade:.2f}%")
    print(f"GPA: {gpa:.2f}")
    print(f"Formative Average: {formative_pct:.2f}%")
    print(f"Summative Average: {summative_pct:.2f}%")

    passed = formative_pct >= 50 and summative_pct >= 50

    if passed:
        print("Result: PASSED")
    else:
        print("Result: FAILED")
        failed_formatives = [d for d in formative if d['score'] < 50]
        if failed_formatives:
            max_weight = max(d['weight'] for d in failed_formatives)
            resubmit = [
                d['assignment']
                for d in failed_formatives
                if d['weight'] == max_weight
            ]
            print("Resubmission required (highest-weight failed formative):")
            for name in resubmit:
                print(f"  - {name}")
        else:
            print("Failure driven by the Summative category.")


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
