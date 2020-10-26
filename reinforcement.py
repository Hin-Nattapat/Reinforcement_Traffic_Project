class Reinforcement:
    def __init__(self):
        # self.phases = phases
        self.reward = 0.0
        self.state = [15, 15, 15]
        # self.aaa = value(self.state)
        self.stateSpace = []
        self.action = [
            [self.state[0]+15, self.state[1], self.state[2]],
            [self.state[0]-15, self.state[1], self.state[2]],
            [self.state[0], self.state[1]+15, self.state[2]],
            [self.state[0], self.state[1]-15, self.state[2]],
            [self.state[0], self.state[1], self.state[2]+15],
            [self.state[0], self.state[1], self.state[2]-15],
        ]
        self.maxQ = 0.0
        self.initStateSpace()
        print(self.state)

    def legalAction(self, action):
        State = self.state
        if action == 0:
            State = [State[0]+15, State[1], State[2]]
        elif action == 1:
            State = [State[0]-15, State[1], State[2]]
        elif action == 2:
            State = [State[0], State[1]+15, State[2]]
        elif action == 3:
            State = [State[0], State[1]-15, State[2]]
        elif action == 4:
            State = [State[0], State[1], State[2]+15]
        else:
            State = [State[0], State[1], State[2]-15]

        if State[0] == 0 or State[1] == 0 or State[2] == 0:
            return False
        else:
            return True

    def randomAction(self):
        while True:
            action = randrange(0, 6)
            if self.legalAction(action):
                break
        return action

    def takeAction(self,action):
        if action == 0:
            self.state = [self.state[0]+15, self.state[1], self.state[2]]
        elif action == 1:
            self.state = [self.state[0]-15, self.state[1], self.state[2]]
        elif action == 2:
            self.state = [self.state[0], self.state[1]+15, self.state[2]]
        elif action == 3:
            self.state = [self.state[0], self.state[1]-15, self.state[2]]
        elif action == 4:
            self.state = [self.state[0], self.state[1], self.state[2]+15]
        else:
            self.state = [self.state[0], self.state[1], self.state[2]-15]
        return self.state 

    def initStateSpace(self):
        self.stateSpace.append(
            [[self.state[0], self.state[1], self.state[2]], 0])
        while self.stateSpace[-1][0] != [75, 15, 15]:
            self.add_State(self.stateSpace[-1][0])
        print(self.stateSpace)
        return self.stateSpace
    
    def add_State(self, state):
        state[2] += 15
        if state[2] == 90:
            state[2] = 15
            state[1] += 15
            if state[1] == 90:
                state[1] = 15
                state[0] += 15
        if sum(state) <= 105:
            print(state)
            self.stateSpace.append([state, 0])

    def findMaxQ(self):
        for i in range(6):
            TLS.takeAction(i)
            TLS.setTLS()

