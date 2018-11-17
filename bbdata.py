class Participant:
    def __init__(self, name):
        self.name = name
        self.neutral = ['yoyo_modal', 0, 1, 1, 1]
        self.happy = Emotion('Happy', self.neutral)
        self.depressed = Emotion('Depressed', self.neutral)
        self.grief_stricken = Emotion('Grief-stricken', self.neutral)
        self.scared = Emotion('Scared', self.neutral)
        self.angry = Emotion('Angry', self.neutral)


class Emotion:
    def __init__(self, name, prototype):
        self.name = name
        self.prototype = prototype


class Answer:
    def __init__(self):
        self.val = 0.0
        self.a1, self.a, self.a2 = Choice(), Choice(), Choice()
        self.choices = [self.a1, self.a, self.a2]
        self.stage2 = []

    def set_winner(self, button, stage):
        choices = self.choices if stage == 0 else self.stage2
        for choice in choices:
            if choice.button == button:
                choice.winner = True
                return choice

    def get_winner(self):
        def search(choices):
            winner = Choice()
            for choice in choices:
                if choice.winner:
                    winner = choice
            return winner
        return search(self.choices) if not self.stage2 else search(self.stage2)

    def get_direction(self, choice, dim):
        if choice.euclid[dim] < self.a.euclid[dim]:
            direction = 0
        elif choice.euclid[dim] > self.a.euclid[dim]:
            direction = 1
        else:
            direction = -1
        return direction


class Choice:
    def __init__(self):
        # Euclidean coordinates
        self.euclid = []
        # Which button was pressed (-1: no button pressed, 0: left, 1: right, 2: middle(2nd stage))
        self.button = -1
        # Winner of the stage in an answer (corresponding button was pressed)
        self.winner = False
