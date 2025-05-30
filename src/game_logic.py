import random

class Game:
    def __init__(self, rows=13, cols=6):
        self.rows = rows
        self.cols = cols
        self.grid = [[" " for _ in range(cols)] for _ in range(rows)]
        self.faller = None
        self.faller_row = -1
        self.faller_col = None
        self.faller_state = None  # "falling", "landed", "frozen"
        self.game_over = False
        self.highlighting_matches = False
        self.score = 0
        self._last_match_count = 0

    def spawn_faller(self, col, jewels):
        valid_jewels = {'S', 'T', 'V', 'W', 'X', 'Y', 'Z'}
        if not all(jewel in valid_jewels for jewel in jewels):
            raise ValueError("Invalid jewel specified. Only S, T, V, W, X, Y, Z are allowed.")
        if self.grid[0][col - 1] != " ":
            return False
        self.faller = jewels[::-1]
        self.faller_row = -len(self.faller)
        self.faller_col = col - 1
        self.faller_state = "falling"
        self.render_faller()
        return True

    def rotate_faller(self):
        if self.faller:
            self.faller = self.faller[-1:] + self.faller[:-1]
            self.render_faller()

    def move_faller_left(self):
        if self.faller and self.faller_col > 0:
            for i, jewel in enumerate(self.faller):
                row = self.faller_row + i
                if row >= 0 and self.grid[row][self.faller_col - 1] != " ":
                    return
            self.faller_col -= 1
            self.render_faller()

    def move_faller_right(self):
        if self.faller and self.faller_col < self.cols - 1:
            for i, jewel in enumerate(self.faller):
                row = self.faller_row + i
                if row >= 0 and self.grid[row][self.faller_col + 1] != " ":
                    return
            self.faller_col += 1
            self.render_faller()

    def render_faller(self):
        if not self.faller:
            return
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.startswith("[") or cell.startswith("|"):
                    self.grid[r][c] = " "
        for i, jewel in enumerate(self.faller):
            row = self.faller_row + i
            if row < 0:
                continue
            mark = {"falling": f"[{jewel}]",
                    "landed": f"|{jewel}|",
                    "frozen": f"({jewel})"}[self.faller_state]
            self.grid[row][self.faller_col] = mark

    def update(self):
        if self.game_over or not self.faller:
            return
        if self.faller_state == "falling":
            nr = self.faller_row + 1
            if (nr + len(self.faller) - 1 >= self.rows or
                self.grid[nr + len(self.faller) - 1][self.faller_col] != " "):
                self.faller_state = "landed"
            else:
                self.faller_row += 1
        elif self.faller_state == "landed":
            nr = self.faller_row + len(self.faller)
            if nr >= self.rows or self.grid[nr][self.faller_col] != " ":
                self.faller_state = "frozen"
                self.freeze_faller()
            else:
                self.faller_state = "falling"
        self.render_faller()

    def mark_matches(self):
        matches = set()
        # horizontal
        for r in range(self.rows):
            for c in range(self.cols - 2):
                if (self.grid[r][c] != " " and
                    self.grid[r][c] == self.grid[r][c+1] == self.grid[r][c+2]):
                    matches.update({(r,c), (r,c+1), (r,c+2)})
        # vertical
        for c in range(self.cols):
            for r in range(self.rows - 2):
                if (self.grid[r][c] != " " and
                    self.grid[r][c] == self.grid[r+1][c] == self.grid[r+2][c]):
                    matches.update({(r,c), (r+1,c), (r+2,c)})
        # diagonals TL-BR
        for r in range(self.rows - 2):
            for c in range(self.cols - 2):
                if (self.grid[r][c] != " " and
                    self.grid[r][c] == self.grid[r+1][c+1] == self.grid[r+2][c+2]):
                    matches.update({(r,c), (r+1,c+1), (r+2,c+2)})
        # diagonals TR-BL
        for r in range(self.rows - 2):
            for c in range(2, self.cols):
                if (self.grid[r][c] != " " and
                    self.grid[r][c] == self.grid[r+1][c-1] == self.grid[r+2][c-2]):
                    matches.update({(r,c), (r+1,c-1), (r+2,c-2)})
        self._last_match_count = len(matches)
        for (r,c) in matches:
            jewel = self.grid[r][c].strip('[]| ')
            self.grid[r][c] = f"*{jewel}*"
        return len(matches) > 0

    def freeze_faller(self):
        for i, jewel in enumerate(self.faller):
            r = self.faller_row + i
            if r < 0:
                self.game_over = True
                return
            self.grid[r][self.faller_col] = f" {jewel} "
        self.faller = None
        self.resolve_matches()

    def clear_marked_matches(self):
        # award score based on last match count
        n = self._last_match_count
        if n >= 5:
            self.score += 50
        elif n == 4:
            self.score += 25
        elif n == 3:
            self.score += 10
        # clear
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].startswith('*'):
                    self.grid[r][c] = ' '
        self.drop_jewels()
        self.resolve_matches()
        self.highlighting_matches = False

    def drop_jewels(self):
        for c in range(self.cols):
            empty = self.rows - 1
            for r in range(self.rows-1, -1, -1):
                if self.grid[r][c] != ' ':
                    self.grid[empty][c] = self.grid[r][c]
                    if empty != r:
                        self.grid[r][c] = ' '
                    empty -= 1

    def resolve_matches(self):
        while self.mark_matches():
            self.highlighting_matches = True
            return