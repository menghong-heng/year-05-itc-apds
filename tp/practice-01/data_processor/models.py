"""Data models demonstrating OOP principles, class methods, static methods, and properties.

Follows PEP 8 conventions, descriptive naming, and Google-style docstrings.
"""

from typing import Any
from data_processor.constants import DEFAULT_BATCH_SIZE


class StudentRecord:
    """Represents an academic student record in the APDS data pipeline.

    Attributes:
        student_id: Unique university student identifier (e.g., 'e20220258').
        name: Full legal name of the student.
        gpa: Grade point average on a 4.0 scale.
    """

    def __init__(self, student_id: str, name: str, gpa: float = 0.0) -> None:
        """Initializes a new StudentRecord instance.

        Args:
            student_id: The unique student identifier string.
            name: Full name of the student.
            gpa: Cumulative GPA, defaults to 0.0.

        Raises:
            ValueError: If student_id is empty or GPA is outside [0.0, 4.0].
        """
        if not student_id or not student_id.strip():
            raise ValueError("Student ID cannot be empty.")
        self.student_id: str = student_id.strip()
        self.name: str = name.strip()
        self._gpa: float = 0.0
        self.gpa = gpa  # Utilize property setter validation

    @property
    def gpa(self) -> float:
        """float: The cumulative GPA of the student."""
        return self._gpa

    @gpa.setter
    def gpa(self, value: float) -> None:
        """Sets and validates the cumulative GPA.

        Args:
            value: Float numeric GPA value.

        Raises:
            ValueError: If value is not between 0.0 and 4.0.
        """
        if not (0.0 <= value <= 4.0):
            raise ValueError(f"GPA must be between 0.0 and 4.0. Received: {value}")
        self._gpa = round(value, 2)

    def is_honor_roll(self) -> bool:
        """Evaluates whether the student qualifies for honor roll distinction.

        Returns:
            bool: True if GPA is 3.50 or higher, False otherwise.
        """
        return self.gpa >= 3.50

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StudentRecord":
        """Alternative constructor to instantiate a StudentRecord from a dictionary.

        Args:
            data: Dictionary containing 'student_id', 'name', and optional 'gpa'.

        Returns:
            StudentRecord: Newly created student record object.

        Raises:
            KeyError: If required keys are missing.
        """
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            gpa=float(data.get("gpa", 0.0)),
        )

    @staticmethod
    def validate_id_format(student_id: str) -> bool:
        """Static helper to verify if an ID follows ITC convention (e.g. 'e' + 7 digits).

        Args:
            student_id: Student ID string to evaluate.

        Returns:
            bool: True if valid pattern, False otherwise.
        """
        cleaned = student_id.strip().lower()
        return len(cleaned) == 9 and cleaned.startswith("e") and cleaned[1:].isdigit()

    def __repr__(self) -> str:
        """Unambiguous string representation for debugging and logging."""
        return (
            f"StudentRecord(student_id='{self.student_id}', "
            f"name='{self.name}', gpa={self.gpa})"
        )

    def __str__(self) -> str:
        """Readable student record presentation."""
        return f"{self.name} ({self.student_id}) - GPA: {self.gpa:.2f}"


class BatchProcessor:
    """Manages batch ingestion and processing for data streams."""

    def __init__(self, batch_size: int = DEFAULT_BATCH_SIZE) -> None:
        """Initializes batch processor with a validated batch size."""
        if batch_size <= 0:
            raise ValueError(f"Batch size must be positive. Received: {batch_size}")
        self.batch_size: int = batch_size
        self._records: list[StudentRecord] = []

    def add_record(self, record: StudentRecord) -> None:
        """Appends a valid student record to the current batch."""
        self._records.append(record)

    @property
    def record_count(self) -> int:
        """Returns total records queued."""
        return len(self._records)

    def calculate_average_gpa(self) -> float:
        """Computes the mean GPA across all stored records.

        Returns:
            float: Mean GPA, or 0.0 if no records exist.
        """
        if not self._records:
            return 0.0
        total_gpa = sum(record.gpa for record in self._records)
        return round(total_gpa / len(self._records), 2)
