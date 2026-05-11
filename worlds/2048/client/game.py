import math
import random


class TwoThousandAndFortyEightGame:
    score: int
    grid: list[list[int]]

    def __init__(self, missing_locations: set[int]) -> None:
        self.checked_locations: set[int] = set()
        self.owned_merges: set[int] = set()
        self.unmet_score_thresholds: list[int] = sorted(
            [location for location in missing_locations if not math.log2(location).is_integer()]
        )
        self.luck = 1
        self.got_2048 = False
        self.reset_grid()

    def reset_grid(self) -> None:
        self.score = 0
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self, cell_value: int = 0) -> None:
        """Finds an empty cell and places a 2 or 4."""
        empty_cells = [(x, y) for x in range(4) for y in range(4) if self.grid[y][x] == 0]
        assert empty_cells
        x, y = random.choice(empty_cells)
        if cell_value == 0:
            wanted = 4
            if 4 not in self.checked_locations:
                pass
            elif 2 not in self.checked_locations:
                wanted = 2
            elif 2 not in self.owned_merges:
                pass
            elif 4 not in self.owned_merges:
                wanted = 2
            else:
                for i in range(x-1, -1, -1):
                    if self.grid[y][i] == 2:
                        wanted = 2
                        break
                    if self.grid[y][i] != 0:
                        break

                if wanted == 4:
                    for i in range(x+1, 4, 1):
                        if self.grid[y][i] == 2:
                            wanted = 2
                            break
                        if self.grid[y][i] != 0:
                            break

                if wanted == 4:
                    for i in range(y-1, -1, -1):
                        if self.grid[i][x] == 2:
                            wanted = 2
                            break
                        if self.grid[i][x] != 0:
                            break

                if wanted == 4:
                    for i in range(y+1, 4, 1):
                        if self.grid[i][x] == 2:
                            wanted = 2
                            break
                        if self.grid[i][x] != 0:
                            break

                if wanted == 4 and self.unmet_score_thresholds:
                    max_value = 2
                    grid_space = 14
                    while max_value in self.owned_merges:
                        max_value *= 2
                        grid_space -= 1.5
                        if max_value not in self.checked_locations or (max_value == 2048 and not self.got_2048):
                            break
                    else:
                        log = math.log2(max_value) - 2
                        score_4s = max_value * grid_space * log
                        score_2s = max_value * (grid_space - 2) * 2 * log
                        if score_4s < self.unmet_score_thresholds[0] < score_2s:
                            wanted = 2

            if wanted == 2:
                luck = (0.11 - 0.01 * self.luck)
            else:
                luck = 0.1 * self.luck
            cell_value = 4 if random.random() < luck else 2
        self.grid[y][x] = cell_value
        self.checked_locations.add(cell_value)

    def apply_move_on_line(self, line: list[int]) -> tuple[list[int], bool]:
        new_line = []
        updated = False
        saw_0 = False
        prev_digit = 0
        for i in range(4):
            digit = line[i]
            if digit == 0:
                saw_0 = True
                continue
            if saw_0:
                updated = True

            if digit == prev_digit and digit in self.owned_merges:
                new_digit = digit * 2
                self.checked_locations.add(new_digit)
                self.score += new_digit
                new_line.append(new_digit)
                updated = True
                prev_digit = 0
                if new_digit == 2048:
                    self.got_2048 = True
            elif prev_digit:
                new_line.append(prev_digit)
                prev_digit = digit
            else:
                prev_digit = digit

        if prev_digit:
            new_line.append(prev_digit)
        while len(new_line) < 4:
            new_line.append(0)
        return new_line, updated

    def input(self, key: str) -> bool:
        if key == "reset":
            self.reset_grid()
            return True

        refresh = False

        if key in ["left", "right"]:
            for y in range(4):
                row = self.grid[y]
                if key == "right":
                    row = row[::-1]  # Reverse for Right

                new_row, updated = self.apply_move_on_line(row)
                refresh = refresh or updated

                if key == "right":
                    new_row = new_row[::-1]  # Reverse back
                self.grid[y] = new_row

        elif key in ["up", "down"]:
            for x in range(4):
                # Extract column
                col = [self.grid[y][x] for y in range(4)]
                if key == "down":
                    col = col[::-1]  # Reverse for Down

                new_col, updated = self.apply_move_on_line(col)
                refresh = refresh or updated

                if key == "down":
                    new_col = new_col[::-1]  # Reverse back
                # Put back into column
                for y in range(4):
                    self.grid[y][x] = new_col[y]

        # Only spawn a new tile and return True if the board changed
        if refresh:
            while self.unmet_score_thresholds:
                score_goal = self.unmet_score_thresholds[0]
                if score_goal > self.score:
                    break
                del self.unmet_score_thresholds[0]
                self.checked_locations.add(score_goal)
            self.spawn_tile()
            return True

        return False

    def receive_item(self, item_id: int) -> None:
        if math.log2(item_id).is_integer():
            self.owned_merges.add(item_id)
        elif item_id == 13:
            self.luck += 1
        elif item_id == 666:
            all_tiles = []
            for line in self.grid:
                all_tiles.extend(line)
            random.shuffle(all_tiles)
            i = 0
            for y in range(4):
                for x in range(4):
                    self.grid[y][x] = all_tiles[i]
                    i += 1
        elif item_id < 100:
            self.spawn_tile(item_id)
