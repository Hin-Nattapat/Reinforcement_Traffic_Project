import random
import math
import statistics as st

class Reinforcement():
    def __init__(self, lane, max_actions, avg_speed, avg_density, max_waiting_time):
        self.EXPLORE_RATE = 0.5
        self.LEARNING_RATE = 0.1
        self.DISCOUNT_RATE = 0.9
        self.MAX_ACTIONS = max_actions
        self.TAU = 0.8
        self.DELTA = 0.5
        self.lane = lane
        self.current_state = 0
        self.stateSpace = {}
        self.moveState = [-1, -1]
        self.greenTime = 60
        #####################################
        self.AVG_SPD = avg_speed
        self.DENSITY = avg_density
        self.MAX_WAITING_TIME = max_waiting_time
        #####################################
        self.init_stateSpace()

    def init_stateSpace(self):
        for i in range(len(self.lane)):
            temp = {
                "q_value" : [0.0]*self.MAX_ACTIONS,
                "sumQ" : 0.0,
                "maxQ" : 0.0
            }
            self.stateSpace[i] = temp
        #print(self.stateSpace)

    def printStateSpace(self):
        print(self.stateSpace)

    def get_nextState(self, q_length):
        max_length = 0
        max_lane = ''
        for lane, length in q_length.items():
            if length > max_length and lane not in self.moveState:
                max_lane = lane
                max_length = length
        if max_length > 0:
            return self.lane.index(max_lane)
        else:
            return None

    def set_maxQ(self):
        for i in range(len(self.stateSpace)):
            maxQ = max(self.stateSpace[i]["q_value"])
            self.stateSpace[i]["maxQ"] = maxQ
    
    def set_sumQ(self):
        for i in range(len(self.stateSpace)):
            sumQ = sum(self.stateSpace[i]["q_value"])
            self.stateSpace[i]["sumQ"] = sumQ    

    def get_action(self, policy):
        action = None
        if policy == "p_greedy":
            action = self.p_greedy()
        return action

    def e_greedy(self):
        action = 0
        current_state = self.stateSpace[self.current_state]
        if (self.EXPLORE_RATE > random.uniform(0, 1)) or (current_state["sumQ"] == 0.0):
            #explore
            print('explore' ,end=' | ')
            action = self.random_action(self.current_state)
        else:
            #exploit
            print('exploit' ,end=' | ')
            for count in range(self.MAX_ACTIONS):
                if self.action_verify(self.current_state, count):
                    if (current_state["q_value"][count] == current_state["maxQ"]):
                        action = count
        return action

    def p_greedy(self):
        action = 0
        current_state = self.stateSpace[self.current_state]
        if (self.EXPLORE_RATE > random.uniform(0, 1)) or (current_state["sumQ"] == 0.0):
            #explore
            print('explore' ,end=' | ')
            action = self.random_action(self.current_state)
        else:
            #exploit
            print('exploit' ,end=' | ')
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
        action = random.randint(0,2)
        while not(self.action_verify(state, action)):
            action = random.randint(0,2)       
        return action

    def action_verify(self, state, action): #complete
        if state % 2 == 0 and action in [0, 2]:
            return True
        elif state % 2 == 1 and action in [0, 1]:
            return True
        return False
    
    def take_action(self, action):
        green_state = [self.current_state] #which state can go?
        phase = [[''],[''],0]

        if action == 0:
            green_state.append(self.current_state + (-2 * (self.current_state % 2)) + 1)
        else:
            green_state.append((self.current_state + 4) % 8)
        
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
        phase[2] = self.greenTime  

        for i in range(len(green_state)):
            self.moveState[i] = self.lane[green_state[i]]
        
        return phase 

    def update(self, nextState, action, data):
        reward = 0
        reward = self.get_reward(data)
        # reward = self.get_reward_2(data)
        self.set_maxQ()
        state = self.stateSpace[self.current_state]
        next_state = self.stateSpace[nextState]

        state["q_value"][action] += round((self.LEARNING_RATE * (reward + (self.DISCOUNT_RATE * next_state["maxQ"])) - state["q_value"][action]), 5)

        self.set_sumQ()
        self.current_state = nextState

    def find_flowrate_expo(self,flowrate):
        # ต้องหา avg_spd,density นำข้อมูลมาจากกราฟของการทดลองแรก
        Saturate_Flowrate = self.AVG_SPD * self.DENSITY
        A3 = Saturate_Flowrate/2
        A2 = 2.944/(0.95-A3)
        flowrateExpo = A2*(flowrate-A3)
        return flowrateExpo

    def find_waitingtime_expo(self,waitingtime):
        A3 = Max_Waiting_Time/2
        A2 = 2.944/(0.95-A3)
        waitingtimeExpo = A2*(waitingtime-A3)
        return waitingtimeExpo

    def get_reward_2(self, data):
        flowrateExpo = self.find_flowrate_expo(data[0])
        waitingtimeExpo = self.find_waitingtime_expo(data[3])
        FlowRateScale = 1/(1+math.exp(flowrateExpo))
        WaitingTimeScale = 1/(1+math.exp(waitingtimeExpo))
        reward = FlowRateScale/(1+WaitingTimeScale)
        return reward

    def get_reward(self, data):
        arrival = sum(data[4]) / len(data[4])
        expo = -0.003930312 * (arrival - 750)
        alpha = 1 / (1 + math.exp(expo))
        tp = sum(data[0]) / len(data[0])
        func = (alpha * st.stdev(data[5])) + ((1 - alpha) * (math.pow(self.TAU, tp)))
        reward = math.log(func, self.DELTA)
        return reward

     


       
    
