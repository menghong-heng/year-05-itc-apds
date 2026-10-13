"""Clean Code Demonstration: Dirty Code vs. Refactored Code.

This script contrasts common code smells against clean code practices
emphasized in 'The Art of Readable Code' and PEP 8 guidelines.
"""

from data_processor.models import StudentRecord
from data_processor.utils import format_student_summary


# ==============================================================================
# ANTI-PATTERN: Dirty Code Example (Poor naming, nested logic, magic numbers)
# ==============================================================================
def proc_data(d):
    # bad: ambiguous names 'd', 'res', 'x', magic numbers 3.5, 50
    res = []
    if d is not None:
        if len(d) > 0:
            for x in d:
                if x[1] >= 3.5:  # magic number, indexing without context
                    # formatting mixed with business logic
                    res.append(x[0].upper() + " PASSED WITH " + str(x[1]))
    return res


# ==============================================================================
# CLEAN CODE: Refactored with Domain Objects, Guard Clauses, and Clear Names
# ==============================================================================
MINIMUM_HONOR_GPA: float = 3.50


def process_honor_roll_students(
    students: list[StudentRecord],
) -> list[str]:
    """Processes honor roll students and returns standardized report strings.

    Key improvements:
    - Type annotations prevent runtime type ambiguity.
    - Guard clause eliminates deep nesting.
    - Domain object (StudentRecord) replaces fragile raw tuples.
    - Constant MINIMUM_HONOR_GPA eliminates magic numbers.

    Args:
        students: Collection of StudentRecord instances.

    Returns:
        list[str]: Formatted summary strings for qualifying students.
    """
    if not students:
        return []

    return [
        format_student_summary(student)
        for student in students
        if student.gpa >= MINIMUM_HONOR_GPA
    ]


def main() -> None:
    """Runs clean code demonstration comparison."""
    sample_students = [
        StudentRecord("e20220258", "Heng Menghong", 3.85),
        StudentRecord("e20220101", "Chan Dara", 3.20),
        StudentRecord("e20220102", "Sok Piseth", 3.92),
        StudentRecord("e20220103", "Keo Bopha", 2.85),
    ]

    print("=== Clean Code Execution Report ===")
    summaries = process_honor_roll_students(sample_students)
    for summary in summaries:
        print(summary)


if __name__ == "__main__":
    main()
