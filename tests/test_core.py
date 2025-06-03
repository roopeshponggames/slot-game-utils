"""
Unit tests for slot_game_utils.core module.
"""

import pytest
import numpy as np
from slot_game_utils import (
    extract_winline_spinwin_data,
    extract_game_detail,
    check_wild_symbols,
    check_wild_presence,
    check_win,
)


class TestExtractWinlineSpinwinData:
    """Test cases for extract_winline_spinwin_data function."""
    
    def test_empty_matrix(self):
        """Test handling of empty matrix."""
        total_win = 0.0
        trigger_type = "bonus"
        matrix = []
        winlines = []
        spin_wins = []
        
        result = extract_game_detail(total_win, trigger_type, matrix, winlines, spin_wins)
        
        assert result["win"] == 0.0
        assert result["triggerType"] == "bonus"
        assert result["reels"] == []
        assert result["spinWins"] == []
    
    def test_different_trigger_types(self):
        """Test with different trigger types."""
        matrix = [[1, 2], [3, 4]]
        
        for trigger in ["normal", "bonus", "free_spin"]:
            result = extract_game_detail(100.0, trigger, matrix, [], [100.0])
            assert result["triggerType"] == trigger


class TestCheckWildSymbols:
    """Test cases for check_wild_symbols function."""
    
    def test_no_wilds(self):
        """Test line with no wild symbols."""
        line = [1, 2, 3, 4, 5]
        wild_ids = [10, 11]
        
        result = check_wild_symbols(line, wild_ids)
        
        assert result == [False, False, False, False, False]
    
    def test_some_wilds(self):
        """Test line with some wild symbols."""
        line = [1, 5, 3, 5, 2]
        wild_ids = [5, 10]
        
        result = check_wild_symbols(line, wild_ids)
        
        assert result == [False, True, False, True, False]
    
    def test_all_wilds(self):
        """Test line with all wild symbols."""
        line = [5, 10, 5, 10, 5]
        wild_ids = [5, 10]
        
        result = check_wild_symbols(line, wild_ids)
        
        assert result == [True, True, True, True, True]
    
    def test_empty_line(self):
        """Test empty line."""
        line = []
        wild_ids = [5, 10]
        
        result = check_wild_symbols(line, wild_ids)
        
        assert result == []


class TestCheckWildPresence:
    """Test cases for check_wild_presence function."""
    
    def test_wild_present_list(self):
        """Test wild presence detection with list input."""
        line = [1, 2, 3, 4]
        wild_ids = [3, 5]
        
        result = check_wild_presence(line, wild_ids)
        
        assert result == 1
    
    def test_no_wild_present_list(self):
        """Test no wild presence with list input."""
        line = [1, 2, 6, 4]
        wild_ids = [3, 5]
        
        result = check_wild_presence(line, wild_ids)
        
        assert result == 0
    
    def test_wild_present_numpy(self):
        """Test wild presence detection with numpy array input."""
        line = np.array([1, 2, 3, 4])
        wild_ids = [3, 5]
        
        result = check_wild_presence(line, wild_ids)
        
        assert result == 1
    
    def test_empty_wild_ids(self):
        """Test with empty wild IDs list."""
        line = [1, 2, 3, 4]
        wild_ids = []
        
        result = check_wild_presence(line, wild_ids)
        
        assert result == 0


class TestCheckWin:
    """Test cases for check_win function."""
    
    @pytest.fixture
    def sample_pay_table(self):
        """Sample pay table for testing."""
        return {
            2: {1: 10, 2: 15, 3: 20, 5: 25},
            3: {1: 20, 2: 30, 3: 40, 5: 50},
            4: {1: 40, 2: 60, 3: 80, 5: 100},
            5: {1: 100, 2: 150, 3: 200, 5: 250}
        }
    
    def test_regular_win_no_wilds(self, sample_pay_table):
        """Test regular win without wild symbols."""
        line = [2, 2, 2, 1, 3]
        line_id = 1
        wilds = [False, False, False, False, False]
        wild_ids = [5]
        
        win, code, winlines, spinWins = check_win(
            line, line_id, wilds, wild_ids, sample_pay_table
        )
        
        assert win == 30  # 3 symbols of type 2
        assert code == "B-3-0-2"
        assert winlines == [1, 3, 2, 30]
        assert spinWins == [30]
    
    def test_win_with_wilds(self, sample_pay_table):
        """Test win with wild substitution."""
        line = [5, 2, 2, 1, 3]
        line_id = 2
        wilds = [True, False, False, False, False]
        wild_ids = [5]
        
        win, code, winlines, spinWins = check_win(
            line, line_id, wilds, wild_ids, sample_pay_table
        )
        
        assert win == 30  # Wild + 2 symbols of type 2
        assert code == "B-3-1-2"
        assert winlines == [2, 3, 2, 30]
        assert spinWins == [30]
    
    def test_all_wilds(self, sample_pay_table):
        """Test win with all wild symbols."""
        line = [5, 5, 5, 5, 5]
        line_id = 3
        wilds = [True, True, True, True, True]
        wild_ids = [5]
        
        win, code, winlines, spinWins = check_win(
            line, line_id, wilds, wild_ids, sample_pay_table
        )
        
        assert win == 250  # 5 wilds
        assert code == "B-5-1-5"
        assert winlines == [3, 5, 5, 250]
        assert spinWins == [250]
    
    def test_alternative_wild_pattern(self, sample_pay_table):
        """Test alternative wild pattern win."""
        line = [5, 5, 3, 2, 1]
        line_id = 4
        wilds = [True, True, False, False, False]
        wild_ids = [5]
        
        win, code, winlines, spinWins = check_win(
            line, line_id, wilds, wild_ids, sample_pay_table
        )
        
        # Should check if 2 wilds (25) is better than wild+wild+3 (40)
        assert win == 40  # 3 symbols (2 wilds + symbol 3)
        assert code == "B-3-1-3"
    
    def test_no_win(self, sample_pay_table):
        """Test line with no winning combination."""
        line = [1, 2, 3, 4, 6]
        line_id = 5
        wilds = [False, False, False, False, False]
        wild_ids = [5]
        
        # Single symbol doesn't win
        minimal_pay_table = {1: {}}
        
        win, code, winlines, spinWins = check_win(
            line, line_id, wilds, wild_ids, minimal_pay_table
        )
        
        assert win == 0
    
    def test_missing_pay_table_entry(self, sample_pay_table):
        """Test handling of missing pay table entries."""
        line = [9, 9, 9, 9, 9]  # Symbol 9 not in pay table
        line_id = 6
        wilds = [False, False, False, False, False]
        wild_ids = [5]
        
        win, code, winlines, spinWins = check_win(
            line, line_id, wilds, wild_ids, sample_pay_table
        )
        
        assert win == 0  # No payout for missing symbol
        assert "B-5-0-9" in code


def test_integration_flow():
    """Test integrated flow of multiple functions."""
    # Set up test data
    line = [5, 2, 2, 5, 1]
    wild_ids = [5]
    pay_table = {
        2: {2: 10, 5: 15},
        3: {2: 25, 5: 30},
        4: {2: 50, 5: 60}
    }
    
    # Check wild symbols
    wilds = check_wild_symbols(line, wild_ids)
    assert wilds == [True, False, False, True, False]
    
    # Check wild presence
    has_wild = check_wild_presence(line, wild_ids)
    assert has_wild == 1
    
    # Calculate win
    win, code, winlines, spinWins = check_win(line, 1, wilds, wild_ids, pay_table)
    
    # Create game detail
    matrix = [[5, 2, 2], [5, 1, 3]]
    game_detail = extract_game_detail(win, "normal", matrix, [winlines], spinWins)
    
    assert game_detail["win"] == win
    assert game_detail["reels"] == [5, 2, 2, 5, 1, 3]
    assert game_detail["spinWins"] == spinWins


if __name__ == "__main__":
    pytest.main([__file__]) test_valid_code_parsing(self):
        """Test parsing of valid code string."""
        winline_id = 1
        code = "B-3-0-02-1"
        win_amount = 50.0
        
        winlines, spin_wins = extract_winline_spinwin_data(winline_id, code, win_amount)
        
        assert winlines == [1, 3, 2, 50.0]
        assert spin_wins == [50.0]
    
    def test_invalid_code_format(self):
        """Test handling of invalid code format."""
        winline_id = 1
        code = "B-3"  # Too few segments
        win_amount = 50.0
        
        winlines, spin_wins = extract_winline_spinwin_data(winline_id, code, win_amount)
        
        assert winlines == []
        assert spin_wins == [50.0]
    
    def test_code_with_wild_win(self):
        """Test code indicating win by wild."""
        winline_id = 5
        code = "TF-5-1-10-2"
        win_amount = 100.0
        
        winlines, spin_wins = extract_winline_spinwin_data(winline_id, code, win_amount)
        
        assert winlines == [5, 5, 10, 100.0]
        assert spin_wins == [100.0]


class TestExtractGameDetail:
    """Test cases for extract_game_detail function."""
    
    def test_basic_game_detail_extraction(self):
        """Test basic game detail extraction and formatting."""
        total_win = 150.0
        trigger_type = "normal"
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        winlines = [[1, 3, 2, 50.0], [2, 4, 5, 100.0]]
        spin_wins = [50.0, 100.0]
        
        result = extract_game_detail(total_win, trigger_type, matrix, winlines, spin_wins)
        
        assert result["win"] == 150.0
        assert result["triggerType"] == "normal"
        assert result["reels"] == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert result["spinWins"] == [50.0, 100.0]
    
    def