"""Constants module for APDS data_processor package.

This module defines system-wide constants using PEP 8 naming conventions
(UPPER_SNAKE_CASE) and type-hinted immutability with typing.Final.
"""

from typing import Final

# Numeric thresholds and configurations
DEFAULT_BATCH_SIZE: Final[int] = 64
MAX_RETRIES: Final[int] = 3
TIMEOUT_SECONDS: Final[float] = 30.0

# Supported export formats
SUPPORTED_FORMATS: Final[tuple[str, ...]] = ("json", "csv", "parquet")

# System default values
DEFAULT_ENCODING: Final[str] = "utf-8"
APP_NAME: Final[str] = "APDS_DataProcessor"
VERSION: Final[str] = "1.0.0"
