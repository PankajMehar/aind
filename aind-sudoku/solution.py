# constants
ROWS = 'ABCDEFGHI'
COLS = '123456789'
DIGITS = '123456789'
NUM_SUDOKU_BOXES = 81
WITH_DIAG = 1 # change this to 0 to solve the classical sudoku

# assignments for animation with pygame
assignments = []


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [i + j for i in A for j in B]


def cross_diag(A, B):
    "Diagonal cross product of elements in A and elements in B."
    assert len(A) == len(B)
    return [i + j for i, j in zip(A, B)]

# init globals
boxes = cross(ROWS, COLS)
row_units = [cross(r, COLS) for r in ROWS]
column_units = [cross(ROWS, c) for c in COLS]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') \
                        for cs in ('123', '456', '789')]
diag1_units = cross_diag(ROWS, COLS)
diag2_units = cross_diag(ROWS[::-1], COLS)

unit_list = row_units + column_units + square_units
if WITH_DIAG:
    unit_list.append(diag1_units)
    unit_list.append(diag2_units)

units = dict((s, [u for u in unit_list if s in u]) \
                for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) \
                for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def find_twins(values):
    """Find twins boxes.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the list of twins pairs [box1, box2]
    """
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    return [[box, peer] for box in potential_twins \
                for peer in peers[box] \
                    if values[box] == values[peer]]


def eliminate_twins(values, twins):
    """Eliminate naked twins for their peers.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Eliminate the naked twins as possibilities for their peers
    for [box1, box2] in twins:
        peers_both = peers[box1] & peers[box2]

        for peer in peers_both:
            for val in values[box1]:
                if len(values[peer]) > 1:
                    values = assign_value(values, peer, values[peer].replace(val, ''))

    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    twins = find_twins(values)
    return eliminate_twins(values, twins)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
                    then the value will be '123456789'.
    """
    chars = []
    for ch in grid:
        if ch in '.0':
            chars.append(DIGITS)
        else:
            if ch in DIGITS:
                chars.append(ch)
            else:
                assert False

    assert len(chars) == NUM_SUDOKU_BOXES
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF':
            print(line)


def eliminate(values):
    """
    Go through all boxes and fliminates found unique values from the box peers
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        Modified sudoku dictionary
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit, ''))

    return values


def only_choice(values):
    """
    Go through all units and if there is a value that fits only into one box,
    assign it to this box
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        Modified sudoku dictionary
    """
    for unit in unit_list:
        for digit in DIGITS:
            digit_places = [box for box in unit if digit in values[box]]
            if len(digit_places) == 1:
                values = assign_value(values, digit_places[0], digit)

    return values


def reduce_puzzle(values):
    """
    Iterates over the puzzle calling eliminate and only_choice effectively reducing it.
    If after an iteration the sudoku remains unchagned, finish the loop
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        Modified sudoku dictionary
    """
    solved = len([box for box in values.keys() if len(values[box]) == 1])
    stalled = (solved == NUM_SUDOKU_BOXES)

    while not stalled:
        solved_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_before == solved_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    Implement deep-first-search to solve the sudoku puzzle
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        Modified sudoku dictionary
    """
    values = reduce_puzzle(values)
    if values == False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values

    _, min_val_box = \
        min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for val in values[min_val_box]:
        new_values = values.copy()
        new_values = assign_value(new_values, min_val_box, val)
        new_values = search(new_values)
        if new_values != False:
            return new_values

    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass

    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
