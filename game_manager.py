import random

class GameManager:
    def __init__(self):

        # difficulties
        self.difficulties = [
            {"name": "Easy",   "speed": "Slow", "density": "+--"},
            {"name": "Medium", "speed": "Medium", "density": "++-"},
            {"name": "Hard",   "speed": "Fast", "density": "+++"}
        ]

        self.current_diff_idx = 0
        self.chosen_difficulty = None
        self.step_time = 2.5
        self.offset = 40
        self.score = 0


    def current_difficulty(self):
        return self.difficulties[self.current_diff_idx]

    def next_difficulty(self, delta=1):
        self.current_diff_idx = (self.current_diff_idx + delta) % len(self.difficulties)

    def set_step_time(self,t):
        self.step_time = t
        
    def get_step_time(self):
        return self.step_time
    
    def update_offset(self,uo):
        self.offset -= uo
        
    def get_offset(self):
        return self.offset
    
    def update_score(self,score):
        self.score += score
        
    def get_score(self):
        return self.score
    
    
    def generate_map(self):

        difficulty = self.difficulties[self.current_diff_idx]

        if difficulty == "easy":
            rows = 20
            prob = 0.1
            self.step_time = 2.5
            
        elif difficulty == "medium":
            rows = 30
            prob = 0.15
            self.step_time = 2.0
        else:
            rows = 40
            prob = 0.3
            self.step_time = 1.5

        # map grid：list of list，5*N
        grid = []

        for _ in range(rows):
            row = []

            # random
            for _ in range(5):
                if random.random() < prob:
                    row.append("X")
                else:
                    row.append(" ")

            # 1 space (easier)
            if all(c == "X" for c in row):
                idx = random.randint(0, 4)
                row[idx] = " "

            grid.append(row)
            self.offset = len(grid)

        return grid
    
    def check_collision(self, grid, offset, player_col):

        player_row = offset + 4

        # if finish / wall -> no collision
        if player_row < 0 or player_row >= len(grid):
            return False

        if player_col < 0 or player_col > 4:
            return False

        cell = grid[player_row][player_col]

        return cell == "X"
    

