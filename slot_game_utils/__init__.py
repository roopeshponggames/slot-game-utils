"""
Slot Game Utils - A utility package for slot game simulations.

This package provides functions for:
- Extracting winline and spin win data
- Processing game details and formatting tickets
- Detecting wild symbols and calculating wins
"""

from .core import (
    extract_winline_spinwin_data,
    extract_game_detail,
    check_wild_symbols,
    check_wild_presence,
    check_win,
)

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "extract_winline_spinwin_data",
    "extract_game_detail",
    "check_wild_symbols",
    "check_wild_presence",
    "check_win",
]