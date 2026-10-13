"""APDS Data Processor Package.

This package provides clean, modular components demonstrating PEP 8 standards,
object-oriented architecture, and clean code practices for Data Science.
"""

from data_processor.constants import (
    APP_NAME,
    DEFAULT_BATCH_SIZE,
    MAX_RETRIES,
    VERSION,
)
from data_processor.models import BatchProcessor, StudentRecord
from data_processor.utils import (
    calculate_grade_letter,
    filter_honor_students,
    format_student_summary,
)

__all__ = [
    "APP_NAME",
    "DEFAULT_BATCH_SIZE",
    "MAX_RETRIES",
    "VERSION",
    "BatchProcessor",
    "StudentRecord",
    "calculate_grade_letter",
    "filter_honor_students",
    "format_student_summary",
]

__version__ = VERSION
