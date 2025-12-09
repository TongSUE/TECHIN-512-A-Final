import os

class ScoreManager:
    def __init__(self, filename="scores.txt"):
        self.filename = filename
        
        if not self._file_exists():
            self._init_empty_file()

    def _file_exists(self):
        try:
            os.stat(self.filename)
            return True
        except OSError:
            return False

    def _init_empty_file(self):
        with open(self.filename, "w") as f:
            f.write("")   

    def _load_scores(self):
        scores = []
        
        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    print("Empty!")
                # format：Madoka,200
                name, score_str = line.split(",")
                scores.append((name, int(score_str)))

        
        print(scores)

        return scores

    def _save_scores(self, scores):
        with open(self.filename, "w") as f:
            for name, score in scores:
                f.write(f"{name},{score}\n")

    # --------------------------------------
    # 对外功能
    # --------------------------------------

    def add_score(self, character, score):
        """
        return: True -> top3
        """
        all_scores = self._load_scores()

        # add new
        all_scores.append((character, score))

        # sort
        all_scores.sort(key=lambda x: x[1], reverse=True)

        # top 3?
        is_new_high = False
        if (character, score) in all_scores[:3]:
            is_new_high = True

        # save top 3
        trimmed = all_scores[:3]

        self._save_scores(trimmed)

        return is_new_high

    def get_highscore_display(self):
        """
        return high score list
        format:
        [
            "< High Score >",
            "1 Madoka 200",
            "2 Homura 140",
            "-----"
        ]
        """
        lines = []

        scores = self._load_scores()

        if len(scores) == 0:
            lines.append("-----")
            return lines

        # sort (in case
        scores.sort(key=lambda x: x[1], reverse=True)

        for idx, (name, score) in enumerate(scores):
            # format: 1 Madoka 200
            lines.append(f"{idx+1} {name} {score}")

        # empty: "-----"
        if len(scores) < 3:
            lines.append("-----")
        

        return lines

