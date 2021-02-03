import random
import math
import statistics as st

class Reinforcement():
    def __init__(self, initState, lane, max_actions):
        self.EXPLORE_RATE = 0.5
        self.LEARNING_RATE = 0.1
        self.DISCOUNT_RATE = 0.9
        self.MAX_ACTIONS = max_actions
        self.TAU = 0.1
        self.DELTA = 0.5
        self.lane = lane
        self.current_state = initState
        self.stateSpace = {}
        self.moveState = None
        self.init_stateSpace(initState)

    def init_stateSpace(self, initState):
        for i in range(len(self.lane)):
            temp = {
                "q_value" : [0.0]*self.MAX_ACTIONS,
                "sumQ" : 0.0,
                "maxQ" : 0.0
            }
            self.stateSpace[initState + i] = temp
        print(self.stateSpace)

    def get_nextState(self, q_length):
        max_length = 0
        max_lane = ''
        for lane, length in q_length.items():
            if length > max_length and lane not in self.moveState:
                max_lane = lane
                max_length = length        
        return self.lane.index(max_lane) + 1

    def set_maxQ(self):
        for i in range(len(self.stateSpace)):
            maxQ = max(self.stateSpace[i+1]["q_value"])
            self.stateSpace[i+1]["maxQ"] = maxQ
    
    def set_sumQ(self):
        for i in range(len(self.stateSpace)):
            sumQ = sum(self.stateSpace[i+1]["q_value"])
            self.stateSpace[i+1]["sumQ"] = sumQ    

    def get_action(self, policy):
        action = None
        if policy == "p_greedy":
            action = self.p_greedy()
        return action

    def p_greedy(self):
        action = 0
        print('current state' ,end=' ')
        print(self.current_state ,end=' : ')
        print(self.stateSpace[self.current_state])
        current_state = self.stateSpace[self.current_state]
        if ((self.EXPLORE_RATE > random.uniform(0, 1)) or (current_state["sumQ"] == 0.0)):
            #explore
            action = self.random_action(self.current_state)
        else:
            #exploit
            action = self.random_action(self.current_state)
            for count in range(self.MAX_ACTIONS):
                if self.action_verify(self.current_state, action):
                    prob = (current_state["q_value"][action]) / current_state["sumQ"]
                    if prob > random.uniform(0, 1):
                        return action
                action += 1
                if action == self.MAX_ACTIONS:
                    action = 0
            if count == self.MAX_ACTIONS:
                action = self.random_action(self.current_state)
        return action
    
    def random_action(self, state): #complete
        action = random.randint(1,3)
        while not(self.action_verify(state, action)):
            action = random.randint(1,3)       
        return action

    def action_verify(self, state, action): #complete
        if state % 2 == 1 and action in [1, 3]:
            return True
        elif state % 2 == 0 and action in [1, 2]:
            return True
        return False
    
    def take_action(self, action):
        q_value = self.stateSpace[self.current_state]["q_value"]
        green_state = [self.current_state] #which state can go?
        phase = [[''],[''],0] #[0]-green , [1]-yellow

        #get phase
        if action == 1:
            green_state.append(self.current_state + ((self.current_state % 2) * 2) - 1)
        else:
            green_state.append(((self.current_state + 3) % 8) + 1)
        
        g_phase = ''
        y_phase = ''
        for i in [8,7,6,5,4,3,2,1]:
            if i in green_state:
                g_phase += 'G' * (2 - (i % 2))
                y_phase += 'y' * (2 - (i % 2))
            else:
                g_phase += 'r' * (2 - (i % 2))
                y_phase += 'r' * (2 - (i % 2))
        phase[0] = g_phase
        phase[1] = y_phase
        if action == q_value.index(max(q_value)):
            phase[2] = 90
        elif action == q_value.index(min(q_value)):
            phase[2] = 30
        else:
            phase[2] = 60    

        self.moveState = green_state
        return phase           

    def update(self, nextState, action, data):
        reward = self.get_reward(data)
        print('reward : ' ,end='')
        print(reward)
        self.set_maxQ()
        state = self.stateSpace[self.current_state]
        next_state = self.stateSpace[nextState]

        state["q_value"][action - 1] += (self.LEARNING_RATE * (reward + (self.DISCOUNT_RATE * next_state["maxQ"])) - state["q_value"][action - 1])

        self.set_sumQ()
        self.current_state = nextState

    def get_reward(self, data):
        expo = -0.003930312 * (data["arrival"] - 750)
        alpha = 1 / (1 + math.exp(expo))
        tp = sum(data["f_rate"]) / len(data["f_rate"])
        func = (alpha * st.stdev(data["q_length"])) + ((1 - alpha) * (math.pow(self.TAU, tp)))
        reward = math.log(func, self.DELTA)

        return reward



if __name__ == "__main__":
    agent = Reinforcement(1, ['gneE8', 'gneE10', 'gneE12', 'gneE14'], 3)
    q_length = {
        "gneE8" : 2.4,
        "gneE10" : 1.0,
        "gneE12" : 1.4,
        "gneE14" : 3.4
    }
    moved_lane = ['gneE10', 'gneE12']
    x = agent.take_action(1)
    print(x)
    
