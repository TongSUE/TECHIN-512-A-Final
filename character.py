characters = [
    {
        "name": "Homura",
        "skill": "Time Slow",
        "shape": "diamond",
        "color": (150, 0, 220)
    },
    {
        "name": "Madoka",
        "skill": "Full Screen Purify",
        "shape": "circle",
        "color": (200, 50, 70)
    },
    {
        "name": "Mami",
        "skill": "Long-range Attack",
        "shape": "flower",
        "color": (230, 160, 10)
    },
    {
        "name": "Sayaka",
        "skill": "Self Heal",
        "shape": "square",
        "color": (60, 140, 255)
    },
    {
        "name": "Kyouko",
        "skill": "Fast Dash",
        "shape": "triangle",
        "color": (230, 10, 10)
    }
]
from game_manager import GameManager

class CharacterManager:
    def __init__(self):
        self.list = characters
        self.index = 0
        self.charge = 0
        self.max_charge = 100

    def current(self):
        return self.list[self.index]

    def next(self):
        self.index = (self.index + 1) % len(self.list)

    def prev(self):
        self.index = (self.index - 1) % len(self.list)

    def get_color(self):
        return self.current()["color"]
    
    def get_charge(self):
        return self.charge
    
    def add_charge(self, amount):
        self.charge = min(self.max_charge, self.charge + amount)
    
    def try_use_skill(self, game_manager,grid,offset, player_col):


        if self.charge < self.max_charge:
            return None

        # recharge
        self.charge = 0

        # skills
        if self.index == 0:
            self.skill_homura(game_manager)
        elif self.index == 1:
            self.skill_madoka(grid, offset)
        elif self.index == 2:
            self.skill_mami(grid, offset,player_col)
        elif self.index == 3:
            self.skill_sayaka(game_manager)
        elif self.index == 4:
            self.skill_kyoko(game_manager)
            
        print("Skill!")

        return None
    
    
    # Skills
    
    # Madoka — clear offset~offset+5
    def skill_madoka(self, grid, offset):
        up_to = min(len(grid), offset + 6)
        for r in range(offset, up_to):
            for c in range(5):
                grid[r][c] = " "

    # Homura — step_time = 4 for this level
    def skill_homura(self,game_manager):
        game_manager.set_step_time(4)

    # Sayaka — HP(Score) + 200
    def skill_sayaka(self,game_manager):
        game_manager.update_score(200)

    # Mami — clear this col offset~offset+9
    def skill_mami(self, grid, offset,player_col):
        up_to = min(len(grid), offset + 10)
        for r in range(offset, up_to):
            grid[r][player_col] = " "

    # Kyoko — offset -= 3 dash
    def skill_kyoko(self, game_manager):
        game_manager.update_offset(3)
