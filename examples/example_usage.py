"""
Example usage of slot_game_utils package.
"""

from slot_game_utils import (
    extract_winline_spinwin_data,
    extract_game_detail,
    check_wild_symbols,
    check_wild_presence,
    check_win,
)


def example_basic_usage():
    """Basic usage example of the slot game utilities."""
    
    print("=== Slot Game Utils Example ===\n")
    
    # Example 1: Extract winline data
    print("1. Extracting winline data:")
    winline_id = 1
    code = "B-3-0-02-1"  # 3 combinations, no wild, symbol 02
    win_amount = 50.0
    
    winlines, spin_wins = extract_winline_spinwin_data(winline_id, code, win_amount)
    print(f"   Code: {code}")
    print(f"   Winlines: {winlines}")
    print(f"   Spin wins: {spin_wins}\n")
    
    # Example 2: Check wild symbols
    print("2. Checking wild symbols:")
    line = [1, 5, 3, 5, 2]
    wild_ids = [5, 10]
    
    wild_positions = check_wild_symbols(line, wild_ids)
    print(f"   Line: {line}")
    print(f"   Wild IDs: {wild_ids}")
    print(f"   Wild positions: {wild_positions}\n")
    
    # Example 3: Check wild presence
    print("3. Checking wild presence:")
    has_wild = check_wild_presence(line, wild_ids)
    print(f"   Has wild: {'Yes' if has_wild else 'No'}\n")
    
    # Example 4: Calculate win
    print("4. Calculating win:")
    pay_table = {
        2: {1: 10, 2: 15, 3: 20, 5: 25},
        3: {1: 20, 2: 30, 3: 40, 5: 50},
        4: {1: 40, 2: 60, 3: 80, 5: 100},
        5: {1: 100, 2: 150, 3: 200, 5: 250}
    }
    
    line = [2, 2, 5, 1, 3]
    line_id = 1
    wilds = check_wild_symbols(line, wild_ids)
    
    win, code, winlines, spinWins = check_win(line, line_id, wilds, wild_ids, pay_table)
    print(f"   Line: {line}")
    print(f"   Win amount: {win}")
    print(f"   Win code: {code}")
    print(f"   Winlines: {winlines}\n")
    
    # Example 5: Format game details
    print("5. Formatting game details:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    total_win = 150.0
    trigger_type = "normal"
    all_spin_wins = [50.0, 100.0]
    
    game_ticket = extract_game_detail(
        total_win=total_win,
        trigger_type=trigger_type,
        matrix=matrix,
        winlines=[],
        spin_wins=all_spin_wins
    )
    
    print(f"   Matrix: {matrix}")
    print(f"   Game ticket:")
    for key, value in game_ticket.items():
        print(f"      {key}: {value}")


def example_complex_scenario():
    """Example of a more complex slot game scenario."""
    
    print("\n\n=== Complex Scenario: Multi-line Slot Game ===\n")
    
    # Game configuration
    wild_ids = [0]  # Symbol 0 is wild
    pay_table = {
        3: {0: 50, 1: 30, 2: 25, 3: 20, 4: 15},
        4: {0: 100, 1: 60, 2: 50, 3: 40, 4: 30},
        5: {0: 200, 1: 120, 2: 100, 3: 80, 4: 60}
    }
    
    # Game matrix (5x3 slot)
    matrix = [
        [0, 1, 2],  # Reel 1
        [1, 0, 3],  # Reel 2
        [1, 2, 0],  # Reel 3
        [3, 1, 2],  # Reel 4
        [2, 3, 1]   # Reel 5
    ]
    
    # Define paylines (simplified - just 3 horizontal lines)
    paylines = [
        [matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0], matrix[4][0]],  # Top row
        [matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1], matrix[4][1]],  # Middle row
        [matrix[0][2], matrix[1][2], matrix[2][2], matrix[3][2], matrix[4][2]]   # Bottom row
    ]
    
    total_win = 0
    all_winlines = []
    all_spin_wins = []
    
    print("Checking paylines:")
    for idx, line in enumerate(paylines):
        line_id = idx + 1
        wilds = check_wild_symbols(line, wild_ids)
        
        win, code, winlines, spinWins = check_win(line, line_id, wilds, wild_ids, pay_table)
        
        if win > 0:
            print(f"\nPayline {line_id}: {line}")
            print(f"   Wild positions: {wilds}")
            print(f"   Win: {win}")
            print(f"   Code: {code}")
            
            total_win += win
            all_winlines.append(winlines)
            all_spin_wins.extend(spinWins)
    
    # Create final game ticket
    game_ticket = extract_game_detail(
        total_win=total_win,
        trigger_type="normal",
        matrix=matrix,
        winlines=all_winlines,
        spin_wins=all_spin_wins
    )
    
    print(f"\n\nFinal Game Ticket:")
    print(f"   Total Win: ${game_ticket['win']}")
    print(f"   Trigger Type: {game_ticket['triggerType']}")
    print(f"   Reels: {game_ticket['reels']}")
    print(f"   Individual Wins: {game_ticket['spinWins']}")


def example_error_handling():
    """Example showing error handling."""
    
    print("\n\n=== Error Handling Examples ===\n")
    
    # Invalid code format
    print("1. Handling invalid code format:")
    winline_id = 1
    invalid_code = "INVALID"
    win_amount = 50.0
    
    winlines, spin_wins = extract_winline_spinwin_data(winline_id, invalid_code, win_amount)
    print(f"   Invalid code: {invalid_code}")
    print(f"   Winlines (empty due to error): {winlines}")
    print(f"   Spin wins (still recorded): {spin_wins}\n")
    
    # Missing pay table entry
    print("2. Handling missing pay table entry:")
    pay_table = {2: {1: 10}}  # Very limited pay table
    line = [9, 9, 9, 9, 9]  # Symbol 9 not in pay table
    line_id = 1
    wilds = [False] * 5
    wild_ids = []
    
    win, code, winlines, spinWins = check_win(line, line_id, wilds, wild_ids, pay_table)
    print(f"   Line with missing symbols: {line}")
    print(f"   Win (0 due to missing entry): {win}")
    print(f"   Code: {code}")


if __name__ == "__main__":
    example_basic_usage()
    example_complex_scenario()
    example_error_handling()