# Slot Game Utils

A Python utility package for slot game simulations, providing functions for winline analysis, wild symbol detection, and payout calculations.

## Features

- **Winline Data Extraction**: Parse and extract winline information from formatted codes
- **Game Detail Processing**: Format game states into structured ticket formats
- **Wild Symbol Detection**: Identify and handle wild symbols in paylines
- **Win Calculation**: Calculate payouts based on symbol combinations and pay tables

## Installation

### From PyPI (when published)
```bash
pip install slot-game-utils
```

### From Source
```bash
git clone https://github.com/roopeshponggames/slot-game-utils
cd slot-game-utils
pip install -e .
```

### Development Installation
```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from slot_game_utils import (
    extract_winline_spinwin_data,
    extract_game_detail,
    check_wild_symbols,
    check_wild_presence,
    check_win
)

# Example: Extract winline data
winline_id = 1
code = "B-3-0-02-1"  # Format: <B or TF>-#combination-<wild_flag>-symbol_id-multiplier
win_amount = 50.0

winlines, spin_wins = extract_winline_spinwin_data(winline_id, code, win_amount)
print(f"Winlines: {winlines}")
print(f"Spin wins: {spin_wins}")

# Example: Check for wild symbols
line = [1, 5, 3, 5, 2]
wild_ids = [5, 10]
wild_positions = check_wild_symbols(line, wild_ids)
print(f"Wild positions: {wild_positions}")  # [False, True, False, True, False]

# Example: Format game details
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
total_win = 100.0
trigger_type = "normal"
spin_wins = [50.0, 50.0]

game_ticket = extract_game_detail(
    total_win=total_win,
    trigger_type=trigger_type,
    matrix=matrix,
    winlines=[],  # Currently unused in output
    spin_wins=spin_wins
)
print(f"Game ticket: {game_ticket}")
```

## API Reference

### `extract_winline_spinwin_data(winline_id, code, win_amount)`

Extract winline and spin win data from a formatted code string.

**Parameters:**
- `winline_id` (int): The unique identifier for the winline
- `code` (str): Formatted string (e.g., "B-3-0-02-1")
- `win_amount` (float): The amount won on this winline

**Returns:**
- `tuple`: (winlines, spinWins)

### `extract_game_detail(total_win, trigger_type, matrix, winlines, spin_wins)`

Format game details into a structured ticket format.

**Parameters:**
- `total_win` (float): Total amount won
- `trigger_type` (str): Type of game trigger
- `matrix` (List[List[Any]]): 2D game matrix
- `winlines` (List): Winning line details (currently unused)
- `spin_wins` (List[float]): Individual spin wins

**Returns:**
- `Dict`: Game ticket with win, triggerType, reels, and spinWins

### `check_wild_symbols(line, wild_ids)`

Create a boolean mask for wild symbol positions.

**Parameters:**
- `line` (List[int]): Symbol IDs on a payline
- `wild_ids` (List[int]): IDs of wild symbols

**Returns:**
- `List[bool]`: Boolean mask of wild positions

### `check_wild_presence(line, wild_ids)`

Check if any wild symbols are present in the line.

**Parameters:**
- `line` (List[int] or np.ndarray): Symbol IDs to check
- `wild_ids` (List[int]): IDs of wild symbols

**Returns:**
- `int`: 1 if wilds present, 0 otherwise

### `check_win(line, line_id, wilds, wild_ids, pay_table)`

Calculate winning combinations and payouts for a payline.

**Parameters:**
- `line` (List[int]): Symbol IDs on the payline
- `line_id` (int): Payline identifier
- `wilds` (List[bool]): Wild position mask
- `wild_ids` (List[int]): IDs of wild symbols
- `pay_table` (Dict): Nested dict of payouts

**Returns:**
- `tuple`: (win_amount, code, winlines, spinWins)

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black slot_game_utils/
```

### Linting
```bash
flake8 slot_game_utils/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Author

Roopesh Nair Perayil - roopesh.perayil@pongstudios.com

## Acknowledgments

- Thanks to all contributors who have helped with this project