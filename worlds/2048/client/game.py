import math
import random

from ..locations import SCORE_THRESHOLDS


class TwoThousandAndFortyEightGame:
    score: int
    grid: list[list[int]]

    def __init__(self) -> None:
        self.checked_locations: set[int] = set()
        self.owned_merges: set[int] = set()
        self.luck = 1
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
            if 2 not in self.checked_locations or (
                4 in self.checked_locations and 4 not in self.owned_merges and 2 in self.owned_merges
            ):
                # Never got a 2? Make help them get one (with 10 lucks, that check would otherwise be impossible)
                # Otherwise, if 4 are useless, make 2s more likely if they can be merged.
                # (If 2s can't merge, the player could be wanting to accumulate 4s for when that merge is unlocked)
                cell_value = 4 if random.random() < (0.11 - 0.01 * self.luck) else 2
            else:
                # Make 4s more likely
                cell_value = 4 if random.random() < 0.1 * self.luck else 2
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
            for score_goal in SCORE_THRESHOLDS:
                if score_goal <= self.score:
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
