"""Utility functions demonstrating clean code principles and guard clauses.

Key principles illustrated:
- Single Responsibility Principle (SRP)
- Early returns to eliminate deeply nested conditionals
- Explanatory variables instead of giant nested expressions
"""

from typing import Iterable
from data_processor.models import StudentRecord


def filter_honor_students(
    records: Iterable[StudentRecord],
    minimum_gpa: float = 3.50,
) -> list[StudentRecord]:
    """Filters students meeting the minimum honor roll threshold.

    Demonstrates clean code: early validation and descriptive list comprehension.

    Args:
        records: Iterable collection of StudentRecord instances.
        minimum_gpa: Float threshold for qualification (default 3.50).

    Returns:
        list[StudentRecord]: List of qualifying student records.
    """
    if not records:
        return []

    return [student for student in records if student.gpa >= minimum_gpa]


def calculate_grade_letter(gpa: float) -> str:
    """Converts a numerical GPA to an academic letter grade.

    Uses clean guard clauses / early returns to avoid cascading nested else blocks.

    Args:
        gpa: Numerical GPA between 0.0 and 4.0.

    Returns:
        str: Grade letter ('A', 'B', 'C', 'D', 'F').

    Raises:
        ValueError: If gpa is outside the [0.0, 4.0] interval.
    """
    if not (0.0 <= gpa <= 4.0):
        raise ValueError(f"Invalid GPA {gpa}. Must be between 0.0 and 4.0.")

    # Clean early returns
    if gpa >= 3.70:
        return "A"
    if gpa >= 3.00:
        return "B"
    if gpa >= 2.00:
        return "C"
    if gpa >= 1.00:
        return "D"
    return "F"


def format_student_summary(student: StudentRecord) -> str:
    """Formats student details into a standardized single-line report string.

    Args:
        student: StudentRecord instance.

    Returns:
        str: Cleanly structured summary string.
    """
    grade_letter = calculate_grade_letter(student.gpa)
    status_tag = "HONOR" if student.is_honor_roll() else "STANDARD"
    return (
        f"[{status_tag}] {student.name:<20} | "
        f"ID: {student.student_id} | "
        f"GPA: {student.gpa:.2f} ({grade_letter})"
    )
