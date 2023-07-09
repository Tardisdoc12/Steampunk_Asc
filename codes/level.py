class Level:
    def __init__(self,plateforms=None,entities=None,winFunctions=None,loseFunctions=None,cards=None):
        self.plateforms=plateforms
        self.entities=entities
        self.cards=cards
        self.winFunc=winFunctions
        self.loseFunc=loseFunctions
    def isWon(self):
        if self.winFunc is None:
            return False
        return self.winFunc(self)
    def isLost(self):
        if self.loseFunc is None:
            return False
        return self.loseFunc(self)
