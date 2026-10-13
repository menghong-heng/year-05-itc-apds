"""Debugging and Defensive Programming Demonstration.

Illustrates:
1. Python's built-in breakpoint() and pdb mechanics.
2. Structured logging (logging module) vs. unformatted print() debugging.
3. Defensive assertions and explicit custom exception handling.
"""

import logging
import sys
from data_processor.models import StudentRecord

# Configure structured logging with standard formatting
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("APDS.DebugDemo")


class DataValidationError(Exception):
    """Raised when data records fail business rule validation."""


def parse_and_validate_student(raw_data: dict[str, str | float]) -> StudentRecord:
    """Parses raw input dictionaries into validated StudentRecord objects.

    Demonstrates defensive programming and structured logging.

    Args:
        raw_data: Dictionary containing student attributes.

    Returns:
        StudentRecord: Validated student record.

    Raises:
        DataValidationError: If mandatory fields are missing or invalid.
    """
    logger.debug("Received raw data dictionary: %s", raw_data)

    if "student_id" not in raw_data:
        logger.error("Missing mandatory key 'student_id' in record.")
        raise DataValidationError("Record is missing 'student_id'.")

    student_id = str(raw_data["student_id"])
    name = str(raw_data.get("name", "Unknown"))
    gpa = float(raw_data.get("gpa", 0.0))

    if not StudentRecord.validate_id_format(student_id):
        logger.warning("Student ID '%s' deviates from standard ITC format.", student_id)

    # Defensive assertion: GPA must satisfy bounded range
    assert 0.0 <= gpa <= 4.0, f"Critical constraint violated: GPA {gpa} out of bounds"

    student = StudentRecord(student_id=student_id, name=name, gpa=gpa)
    logger.info("Successfully instantiated student record: %s", student)
    return student


def demonstrate_debugging() -> None:
    """Runs a sequence of parsing operations demonstrating logging and error handling."""
    logger.info("Initiating APDS Debugging Demo...")

    valid_payload = {"student_id": "e20220258", "name": "Heng Menghong", "gpa": 3.88}
    record = parse_and_validate_student(valid_payload)
    print(f"Validated record string: {record}")

    # Handling errors defensively without crashing
    invalid_payload = {"name": "Anonymous Student", "gpa": 3.5}
    try:
        parse_and_validate_student(invalid_payload)
    except DataValidationError as err:
        logger.warning("Caught expected validation exception gracefully: %s", err)


if __name__ == "__main__":
    demonstrate_debugging()
