"""
Tests package for slot_game_utils.

This package contains unit and integration tests for the slot game utilities.
Tests are organized by module and functionality.

Test modules:
- test_core.py: Tests for core game functions including winline extraction,
                game detail formatting, wild symbol detection, and win calculation.

Running tests:
    pytest                    # Run all tests
    pytest -v                 # Run with verbose output
    pytest -k "test_name"     # Run specific test
    pytest --cov=slot_game_utils  # Run with coverage report
"""

# Import key test utilities if needed
import pytest
import numpy as np

# Test configuration
TEST_CONFIG = {
    "default_wild_ids": [0, 5, 10],
    "sample_pay_table": {
        2: {1: 10, 2: 15, 3: 20, 5: 25},
        3: {1: 20, 2: 30, 3: 40, 5: 50},
        4: {1: 40, 2: 60, 3: 80, 5: 100},
        5: {1: 100, 2: 150, 3: 200, 5: 250}
    }
}


def create_test_matrix(rows=5, cols=3, fill_value=None):
    """
    Create a test matrix for slot game testing.
    
    Args:
        rows (int): Number of rows (reels)
        cols (int): Number of columns
        fill_value: If provided, fill matrix with this value.
                   Otherwise, fill with sequential numbers.
    
    Returns:
        list: 2D matrix
    """
    if fill_value is not None:
        return [[fill_value] * cols for _ in range(rows)]
    
    counter = 0
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(counter)
            counter += 1
        matrix.append(row)
    return matrix


def create_test_paylines(matrix):
    """
    Create standard paylines from a slot matrix.
    
    Creates horizontal lines (top, middle, bottom) for a 5-reel slot.
    
    Args:
        matrix (list): 2D slot matrix
    
    Returns:
        list: List of paylines
    """
    if not matrix or len(matrix) < 5:
        return []
    
    paylines = []
    num_rows = len(matrix[0])
    
    # Horizontal lines
    for row_idx in range(num_rows):
        line = [matrix[col][row_idx] for col in range(5)]
        paylines.append(line)
    
    return paylines


# Test data generators
def generate_test_codes():
    """Generate various test codes for winline testing."""
    return [
        ("B-3-0-02-1", True),      # Valid basic code
        ("TF-5-1-10-2", True),     # Valid with trigger flag
        ("B-2-1-5-1", True),       # Valid with wild
        ("B-4-0-03-1", True),      # Valid 4-combination
        ("INVALID", False),         # Invalid format
        ("B-2", False),            # Too few segments
        ("B-a-b-c-d", False),      # Non-numeric values
        ("", False),               # Empty string
    ]


def generate_wild_test_cases():
    """Generate test cases for wild symbol detection."""
    return [
        # (line, wild_ids, expected_wild_positions, expected_presence)
        ([1, 2, 3, 4, 5], [10, 11], [False, False, False, False, False], 0),
        ([1, 5, 3, 5, 2], [5, 10], [False, True, False, True, False], 1),
        ([5, 10, 5, 10, 5], [5, 10], [True, True, True, True, True], 1),
        ([], [5, 10], [], 0),
        ([1, 2, 3], [], [False, False, False], 0),
    ]


# Fixtures for common test data
@pytest.fixture
def sample_game_state():
    """Provide a complete game state for testing."""
    return {
        "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]],
        "paylines": [
            [1, 4, 7, 10, 13],    # Top row
            [2, 5, 8, 11, 14],    # Middle row
            [3, 6, 9, 12, 15],    # Bottom row
        ],
        "wild_ids": [5, 10],
        "pay_table": TEST_CONFIG["sample_pay_table"],
        "trigger_type": "normal",
    }


@pytest.fixture
def empty_game_state():
    """Provide an empty game state for edge case testing."""
    return {
        "matrix": [],
        "paylines": [],
        "wild_ids": [],
        "pay_table": {},
        "trigger_type": "bonus",
    }