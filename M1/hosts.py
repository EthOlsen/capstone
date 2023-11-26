class host:
    def __init__(self, addr):
        self.addr = addr
        self.talkWith = []

    def __str__(self):
        return f"{self.addr}{print(self.talkWith)}"


