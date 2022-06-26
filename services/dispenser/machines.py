from transitions import Machine

class DVR(Machine):
    def __init__(self, state):

        states = "deb dec nld".split()
        Machine.__init__(self, states=states, initial=state)

        self.add_transition("advance", "deb", "dec")
        self.add_transition("advance", "dec", "nld")
        self.add_transition("advance", "nld", "dec")


class Live(Machine):
    def __init__(self, state, local):

        states = "deu nld est cdnv".split()
        Machine.__init__(self, states=states, initial=state)

        self.add_transition("advance", "deu", "nld")
        self.add_transition("advance", "nld", "cdnv")
        self.add_transition("advance", "cdnv", "deu")
        self.add_transition("advance", "est", "nld")
