
def bomber_man(n, grid):
    rows, cols = len(grid), len(grid[0])
    # Convert grid to a list of lists for easier manipulation
    grid_list = [list(row) for row in grid]

    # Helper function to plant bombs
    def plant_bombs():
        for i in range(rows):
            for j in range(cols):
                if grid_list[i][j] == '.':
                    grid_list[i][j] = 'O'

    # Helper function to detonate bombs
    def detonate_bombs():
        for i in range(rows):
            for j in range(cols):
                if grid_list[i][j] == 'O':
                    # Detonate bomb
                    grid_list[i][j] = '.'
                    if i > 0:
                        grid_list[i - 1][j] = '.'  # Up
                    if i < rows - 1:
                        grid_list[i + 1][j] = '.'  # Down
                    if j > 0:
                        grid_list[i][j - 1] = '.'  # Left
                    if j < cols - 1:
                        grid_list[i][j + 1] = '.'  # Right

    # Initial setup
    for i in range(rows):
        for j in range(cols):
            if grid_list[i][j] == 'O':
                # Bomb detonates in 3 seconds, so we can ignore bombs that were already planted
                grid_list[i][j] = 'D'  # Mark bomb as detonating in 3 seconds

    # First second passes, nothing happens
    # Second second passes, all empty cells are filled with bombs
    plant_bombs()

    if n == 1:
        # Only one second has passed, return current state of grid
        return [''.join(row) for row in grid_list]

    # Third second passes, bombs planted 3 seconds ago detonate
    detonate_bombs()

    if n == 2:
        # Only two seconds have passed, return current state of grid
        return [''.join(row) for row in grid_list]

    # After the first cycle, the pattern repeats every 4 seconds
    # The grid state after 4 seconds is the same as after 2 seconds
    # The grid state after 5 seconds is the same as after 1 second
    # The grid state after 6 seconds is the same as after 2 seconds
    # And so on...
    grid_states = [grid_list]
    while len(grid_states) < 4:
        plant_bombs()
        detonate_bombs()
        grid_states.append([row[:] for row in grid_list])

    # Return grid state after n seconds
    return [''.join(grid_states[(n - 3) % 4][i]) for i in range(rows)]

n = 3
grid = [    '. . . . . . .',    '. . . O . . .',    '. . . . O . .',    '. . . . . . .',    'O O . . . . .',    'O O . . . . .']
result = bomber_man(n, grid)
for row in result:
    print(row)
