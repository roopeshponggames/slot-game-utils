"""
Core functions for slot game simulation utilities.
"""

from itertools import chain
from typing import List, Dict, Any, Union, Tuple
import numpy as np


def extract_winline_spinwin_data(
    winline_id: int, code: str, win_amount: float
) -> tuple[List[Union[int, float]], List[float]]:
    """
    Extract winline and spin win data from a formatted code string.
    
    This function parses a specially formatted code string to extract game-related
    information including combination count, wild win status, and symbol information.
    
    Args:
        winline_id (int): The unique identifier for the winline
        code (str): Formatted string following the pattern:
                   <B or TF>-#combination-<1 if win is by wild, else 0>-symbol_id-multiplier
                   Example: "B-3-0-02-1"
        win_amount (float): The amount won on this winline
    
    Returns:
        tuple: A tuple containing two lists:
            - winlines (list): Contains [winline_id, combination_count, symbol_id, win_amount]
            - spinWins (list): Contains [win_amount]
    """
    # Initialize return lists
    winlines = []
    spinWins = []
    
    # Parse the code string
    code_parts = code.split('-')
    
    try:
        # Validate that we have the expected number of parts
        if len(code_parts) < 4:
            raise ValueError("Insufficient code segments")
        
        # Extract relevant data from parsed code
        combination_count = int(code_parts[1])  # Number of winning combinations
        symbol_id = int(code_parts[3])          # ID of the winning symbol
        
        # Build the winlines data structure
        winlines = [
            winline_id,         # Unique winline identifier
            combination_count,  # Number of combinations in this win
            symbol_id,          # Symbol that created the win
            win_amount         # Amount won on this line
        ]
        
    except (IndexError, ValueError) as e:
        # Log error with descriptive message
        error_msg = (
            "-E- Error parsing code. Expected format: "
            "<B or TF>-#combination-<1 if win is by wild, else 0>-symbol_id-multiplier  "
            "Example: B-3-0-02-1"
        )
        print(error_msg)
        # Return empty winlines list on error
        winlines = []
    
    # Spin wins always contains the win amount (even on error)
    spinWins = [win_amount]
    
    return winlines, spinWins


def extract_game_detail(
    total_win: float,
    trigger_type: str,
    matrix: List[List[Any]],
    winlines: List[List[Union[int, float]]],
    spin_wins: List[float]
) -> Dict[str, Any]:
    """
    Extract and format game details into a structured ticket format.
    
    This function takes game state information and formats it into a standardized
    game ticket dictionary. The matrix is flattened from 2D to 1D for serialization.
    
    Args:
        total_win (float): The total amount won in this game round
        trigger_type (str): The type of trigger that initiated this game
                           (e.g., 'normal', 'bonus', 'free_spin')
        matrix (List[List[Any]]): 2D matrix representing the game reels/grid
                                  Will be flattened to 1D in the output
        winlines (List[List[Union[int, float]]]): List of winning line details
                                                  (Note: Currently unused in output)
        spin_wins (List[float]): List of individual spin win amounts
    
    Returns:
        Dict[str, Any]: A game ticket dictionary containing:
            - win: Total win amount
            - triggerType: Type of game trigger
            - reels: Flattened 1D list of reel symbols
            - spinWins: List of individual spin wins
    
    """
    # Flatten the 2D matrix into a 1D list for easier serialization
    # This converts [[1,2,3], [4,5,6]] into [1,2,3,4,5,6]
    flattened_matrix = list(chain.from_iterable(matrix))
    
    # Construct the game ticket with standardized field names
    game_ticket = {
        "win": total_win,
        "triggerType": trigger_type,
        "reels": flattened_matrix,
        "spinWins": spin_wins
    }
    
    return game_ticket


def check_wild_symbols(line: List[int], wild_ids: List[int]) -> List[bool]:
    """
    Check which symbols in a line are wild symbols.
    
    Creates a boolean mask indicating the position of wild symbols in the given line.
    This is useful for identifying wild symbol patterns in winning combinations.
    
    Args:
        line (List[int]): List of symbol IDs representing a payline
        wild_ids (List[int]): List of symbol IDs that are considered wild symbols
    
    Returns:
        List[bool]: Boolean list where True indicates a wild symbol at that position
    
    Example:
        >>> line = [1, 5, 3, 5, 2]
        >>> wild_ids = [5, 10]
        >>> check_wild_symbols(line, wild_ids)
        [False, True, False, True, False]
    """
    # Create boolean mask for wild positions
    wilds = [symbol in wild_ids for symbol in line]
    return wilds


def check_wild_presence(line: Union[List[int], np.ndarray], wild_ids: List[int]) -> int:
    """
    Check if any wild symbols are present in the line.
    
    Efficiently checks for the presence of wild symbols using NumPy operations.
    
    Args:
        line (Union[List[int], np.ndarray]): Sequence of symbol IDs to check
        wild_ids (List[int]): List of symbol IDs that are considered wild
    
    Returns:
        int: 1 if at least one wild symbol is present, 0 otherwise
    
    Example:
        >>> line = [1, 2, 3, 4]
        >>> wild_ids = [3, 5]
        >>> check_wild_presence(line, wild_ids)
        1
    """
    # Convert to numpy array if needed and check for wild presence
    line_array = np.array(line) if not isinstance(line, np.ndarray) else line
    has_wild = np.any(np.isin(line_array, wild_ids))
    
    return int(has_wild)


def check_win(
    line: List[int],
    line_id: int,
    wilds: List[bool],
    wild_ids: List[int],
    pay_table: Dict[int, Dict[int, float]]
) -> Tuple[float, str, List[Union[int, float]], List[float]]:
    """
    Calculate winning combinations and payouts for a given payline.
    
    This function implements the core win detection logic, handling both regular
    symbol matches and wild symbol substitutions. It finds the highest paying
    combination possible on the line.
    
    Args:
        line (List[int]): List of symbol IDs on the payline
        line_id (int): Unique identifier for this payline
        wilds (List[bool]): Boolean mask indicating wild positions (from check_wild_symbols)
        wild_ids (List[int]): List of symbol IDs that are considered wild
        pay_table (Dict[int, Dict[int, float]]): Nested dict mapping 
                                                  [sequence_length][symbol_id] -> payout
    
    Returns:
        Tuple containing:
            - win (float): The calculated win amount
            - code_01 (str): Formatted code describing the win
            - winlines (List): Extracted winline data
            - spinWins (List[float]): List containing the win amount
    
    Win Detection Logic:
        1. All wilds: Pays based on the first wild symbol
        2. Mixed symbols: Finds longest sequence of matching symbols (with wild substitution)
        3. Alternative patterns: Checks if leading wilds form a better paying combination
    
    Code Format:
        "B-{length}-{wild_flag}-{symbol_id}"
        - length: Number of matching symbols
        - wild_flag: 1 if combination includes wilds, 0 otherwise
        - symbol_id: The symbol that formed the winning combination
    """
    line_len = len(line)
    
    # Find position of first non-wild symbol
    first_non_wild = line_len
    for i in range(line_len):
        if not wilds[i]:
            first_non_wild = i
            break
    
    # All wilds case
    if first_non_wild == line_len:
        symbol_to_match = line[0]
        try:
            win = pay_table[line_len][symbol_to_match]
        except Exception as e:
            print(f"Error in extract_winline_spinwin_data (main) payTable key error: {e}")
            win = 0
        code_01 = f"B-{str(line_len)}-1-{str(symbol_to_match)}"
        
        winlines, spinWins = extract_winline_spinwin_data(line_id, code_01, win)
        return win, code_01, winlines, spinWins
    
    # First symbol is the symbol to match for wilds
    symbol_to_match = line[first_non_wild]
    
    # Find the longest sequence of matching symbols or wilds
    sequence_length = 1
    for i in range(first_non_wild + 1, line_len):
        if wilds[i] or line[i] == symbol_to_match:
            sequence_length += 1
        else:
            break
    
    # Calculate win for this sequence
    try:
        main_win = pay_table[sequence_length + first_non_wild][symbol_to_match]
    except Exception as e:
        print(f"Error in extract_winline_spinwin_data (main) payTable key error: {e}")
        main_win = 0
    wild_presence = check_wild_presence(line[0:sequence_length + first_non_wild], wild_ids)
    code_01 = f"B-{str(sequence_length + first_non_wild)}-{str(wild_presence)}-{str(symbol_to_match)}"
    
    # Check for alternative win patterns based on original logic
    if first_non_wild > 0:
        # Try using the first symbol with wilds
        first_symbol = line[0]
        
        wild_sequence = first_non_wild
        
        if wild_sequence >= 2:  # Need at least 2 for a win
            try:
                alt_win = pay_table[wild_sequence][first_symbol]
            except Exception as e:
                print(f"Error in extract_winline_spinwin_data (main) payTable key error: {e}")
                alt_win = 0
            # Compare with main win, take the higher value
            if alt_win > main_win:
                wild_presence = check_wild_presence(line[0:wild_sequence], wild_ids)
                code_01 = f"B-{str(wild_sequence)}-{str(wild_presence)}-{str(first_symbol)}"
                
                winlines, spinWins = extract_winline_spinwin_data(line_id, code_01, alt_win)
                return alt_win, code_01, winlines, spinWins
    
    winlines, spinWins = extract_winline_spinwin_data(line_id, code_01, main_win)
    
    return main_win, code_01, winlines, spinWins