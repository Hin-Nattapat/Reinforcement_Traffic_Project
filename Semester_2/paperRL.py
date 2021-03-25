import random
import math

class Reinforcement():
    def __init__(self, maxState):
        self.EXPLORE_RATE = 0.5
        self.LEARNING_RATE = 0.1
        self.DISCOUNT_RATE = 0.9
        self.MAX_ACTIONS = 3
        self.TAU = 0.8
        self.DELTA = 0.5
        self.stateSpace = {}

        for state in range(8):
            temp = {
                'qValue' : [0.0]*self.MAX_ACTIONS,
                'sumQ' : 0.0,
                'maxQ' : 0.0
            }
            self.stateSpace[state] = temp
        
    def printStateSpace(self):
        print('\nThis is result at end of simulation' ,end='')
        for state, data in self.stateSpace.items():
            print('\n----------------- state' ,state ,'-----------------')
            for key, value in data.items():
                print(key, '=' ,value)

    def setMaxQ(self):
        for i in range(len(self.stateSpace)):
            maxQ = max(self.stateSpace[i]['qValue'])
            self.stateSpace[i]['maxQ'] = maxQ
    
    def setSumQ(self):
        for i in range(len(self.stateSpace)):
            sumQ = sum(self.stateSpace[i]['qValue'])
            self.stateSpace[i]['maxQ'] = sumQ

    def getAction(self, policy, currentState):
        action = None
        if policy == "p_greedy":
            action = self.pGreedy(currentState)
        if policy == "e_greedy":
            action = self.eGreedy(currentState)
        return action

    def get_avgQ(self):
        total_sumQ = 0
        for i in range(len(self.stateSpace)):
            total_sumQ += sum(self.stateSpace[i]["qValue"])
        avg_sumQ = total_sumQ / (len(self.stateSpace) * (self.MAX_ACTIONS - 1))
        return round(avg_sumQ,3)

    def eGreedy(self, currentState):
        action = 0
        stateData = self.stateSpace[currentState]
        if (self.EXPLORE_RATE > random.uniform(0, 1)) or (stateData["sumQ"] == 0.0):
            #explore
            print('explore' ,end=' | ')
            action = self.randomAction(currentState)
        else:
            #exploit
            print('exploit' ,end=' | ')
            for count in range(self.MAX_ACTIONS):
                if self.actionVerify(currentState, count):
                    if (stateData["q_value"][count] == stateData["maxQ"]):
                        action = count
        return action

    def pGreedy(self, currentState):
        action = 0
        stateData = self.stateSpace[currentState]
        if (self.EXPLORE_RATE > random.uniform(0, 1)) or (stateData["sumQ"] == 0.0):
            #explore
            print('explore' ,end=' | ')
            action = self.randomAction(currentState)
        else:
            #exploit
            print('exploit' ,end=' | ')
            action = self.randomAction(currentState)
            for count in range(self.MAX_ACTIONS):
                if self.actionVerify(currentState, action):
                    prob = (stateData["q_value"][action]) / stateData["sumQ"]
                    if prob > random.uniform(0, 1):
                        return action
                action += 1
                if action == self.MAX_ACTIONS:
                    action = 0
            if count == self.MAX_ACTIONS:
                action = self.randomAction(currentState)
        return action
    
    def randomAction(self, state): #complete
        action = random.randint(0,2)
        while not(self.actionVerify(state, action)):
            action = random.randint(0,2)       
        return action

    def actionVerify(self, state, action): #complete
        if state % 2 == 0 and action in [0, 2]:
            return True
        elif state % 2 == 1 and action in [0, 1]:
            return True
        return False
    
    def takeAction(self, action, currentState):
        green_state = [currentState] #which state can go?
        phase = [[''],[''],0]

        if action == 0:
            green_state.append(currentState + (-2 * (currentState % 2)) + 1)
        else:
            green_state.append((currentState + 4) % 8)
        
        g_phase = ''
        y_phase = ''
        for i in [7,6,5,4,3,2,1,0]:
            if i in green_state:
                g_phase += 'G' * (1 + (i % 2))
                y_phase += 'y' * (1 + (i % 2))
            else:
                g_phase += 'r' * (1 + (i % 2))
                y_phase += 'r' * (1 + (i % 2))

        phase[0] = g_phase
        phase[1] = y_phase
        phase[2] = 60  
        
        return phase, green_state
    
    def getNextState(self, qLength, moveState):  
        length = qLength
        maxLength = max(length)
        nextState = length.index(maxLength)
        while nextState in moveState:
            length[nextState] = -1
            maxLength = max(length)
            nextState = length.index(maxLength)
        print(nextState)
        return nextState
    
    def getRandomState(self, moveState):
        nextState = random.randint(0, 7)
        while nextState in moveState:
            nextState = random.randint(0, 7)
        return nextState

    def update(self, currentState, nextState, action, data):
        reward = self.getReward(data)
        self.setMaxQ()
        currentData = self.stateSpace[currentState]
        nextData = self.stateSpace[nextState]

        currentData["qValue"][action] += round((self.LEARNING_RATE * (reward + (self.DISCOUNT_RATE * nextData["maxQ"])) - currentData["qValue"][action]), 5)
        self.stateSpace[currentState] = currentData
        self.setSumQ()

    def getReward(self, data):
        expo = -0.003930312 * (data['arrivalRate'] - 750)
        alpha = 1 / (1 + math.exp(expo))
        func = (alpha * data['qStd']) + ((1 - alpha) * (math.pow(self.TAU, data['flowRate'])))
        reward = math.log(func, self.DELTA)
        
        return reward
    
    