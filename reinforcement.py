import os
import sys
import optparse
import random
import traci
import api

EXPLORE_RATE = 0.2
LEARNING_RATE = 0.5
DISCOUNT_RATE = 0.9
MAX_ACTION = 6
num_episodes = 5

# State จะอยู่ในรูปแบบของ [G1,G2,G3] เวลาไฟเขียวแต่ละแยก
# 1 Cycle = 120 วินาที ดังนั้น G4 = 120-G1-G2-G3

# class SumoEnv:
#     def __init__(self, net_file="test", rou_file="test", use_gui=False,):
#         self.net_file = net_file
#         self.rou_file = rou_file
#         self.use_gui = use_gui
#         if self.use_gui:
#             self.sumo_binary = checkBinary('sumo-gui')
#         else:
#             self.sumo_binary = checkBinary('sumo')
#         traci.start([self.sumo_binary, "-c", "4cross_TLS/1_1Cross.sumocfg"])

class StateAction:
    def __init__(self, state):
        self.state_value = state
        self.q_value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def __str__(self):
        return "state" + str(self.state_value)

    def get_QMax(self):
        self.q_Max = max(self.q_value)
        return self.q_Max

    def get_QSum(self):
        self.q_Sum = sum(self.q_value)
        return self.q_Sum


class TrafficLight:
    def __init__(self, state, lane):
        # self.phases = phases
        self.reward = 0.0
        self.state = state
        self.stateSpace = []
        self.lane = lane
        self.complete = False
        self.action = 0

    def legalAction(self, action, inputState):
        State = inputState.copy()
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

        if (State[0] == 0 or State[1] == 0 or State[2] == 0):
            return False
        elif sum(State) > 105:
            return False
        else:
            return True

    def randomAction(self):
        while True:
            action = random.randrange(0, MAX_ACTION)
            if self.legalAction(action, self.state):
                break
        return action

    # def get_nextState(self, action, State):
    #     state = self.takeAction(action, State)
    #     return state

    def get_state(self, inputState):
        tempState = []
        for i in range(len(self.stateSpace)):
            if self.stateSpace[i]["state"] == inputState:
                tempState = self.stateSpace[i]
                break
        return tempState

    def takeAction(self, action, inputState):
        State = inputState.copy()
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
        return State

    def InitStateSpace(self):
        State = [15,15,15]
        self.stateSpace.append({"state": [State[0], State[1], State[2]], "Q_value": [
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "Q_MAX": 0.0, "Q_SUM": 0.0})
        while State != [75, 75, 75]:
            State[2] += 15
            if State[2] == 90:
                State[2] = 15
                State[1] += 15
                if State[1] == 90:
                    State[1] = 15
                    State[0] += 15
            if sum(State) <= 105:
                self.stateSpace.append({"state": [State[0], State[1], State[2]], "Q_value": [
                                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "Q_MAX": 0.0, "Q_SUM": 0.0})
        print(self.stateSpace)
        # return print(self.stateSpace)

    def Find_Q_Max(self):
        for i in range(len(self.stateSpace)):
            Q_MAX = max(self.stateSpace[i]['Q_value'])
            self.stateSpace[i]["Q_MAX"] = Q_MAX

    def Find_Q_Sum(self):
        for i in range(len(self.stateSpace)):
            tempState = self.stateSpace[i]['state'].copy()
            Q_SUM = 0.0
            for j in range(MAX_ACTION):
                if self.legalAction(j, tempState):
                    # print("state : ", tempState,"Q_value : ", self.stateSpace[i]['Q_value'][j])
                    Q_SUM += self.stateSpace[i]['Q_value'][j]
                    self.stateSpace[i]['Q_SUM'] = Q_SUM
        # return print(self.stateSpace)

    def Find_avg_Q(self):
        count_Q = 0
        Q_sum_all = 0
        for item in self.stateSpace:
            if item['Q_SUM'] != 0:
                Q_sum_all += item['Q_SUM']
            count_Q += 1
        avg_Q = Q_sum_all / count_Q
        if count_Q == 0:
            return 0
        return avg_Q         


    def Greedy_Al(self):
        self.Find_Q_Max()
        State = self.get_state(self.state)
        for i in range(MAX_ACTION):
            if State["Q_value"][i] == State["Q_MAX"]:
                self.action = i
        return self.action

    def E_Greedy_Al(self):
        randomNumber = random.uniform(0, 1)
        State = self.get_state(self.state)
        if ((EXPLORE_RATE > randomNumber) or (State["Q_SUM"] == 0.0)):
            self.action = self.randomAction()
            return self.action
        else:
            for i in range(MAX_ACTION):
                if State["Q_value"][i] == State["Q_MAX"]:
                    self.action = i
            return self.action

    def P_Greedy_Al(self):
        randomNumber = random.uniform(0, 1)
        randomProb = random.uniform(0, 1)
        presentState = self.get_state(self.state)
        if ((EXPLORE_RATE > randomNumber) or (presentState["Q_SUM"] == 0.0)):
            # print("EXPLORE", EXPLORE_RATE, randomNumber)
            self.action = self.randomAction()
            return self.action
        else:
            action = self.randomAction()
            for i in range(MAX_ACTION):
                if self.legalAction(action, self.state):
                    
                    prob = (presentState["Q_value"]
                            [action] / presentState["Q_SUM"])
                    if prob > randomProb:
                        self.action = action
                        return self.action
                action = action + 1
                if action == MAX_ACTION:
                    action = 0
            if (i == MAX_ACTION-1):
                self.action = self.randomAction()
                return self.action
               
    def updateFuction_fixed(self):
        state = [30,30,30]
        api.get_waiting_time(self.lane,state)

    def updateFuction(self, waiting_time):
        newState = self.takeAction(self.action, self.state)
        presentState = self.get_state(self.state)
        nextState = self.get_state(newState)
        #continue simulate
        # api.set_Trafficlight(newState)
        rewardResult = waiting_time
        if rewardResult != 0:
            self.reward = (1/rewardResult) * 100
        else: self.reward = 0
        
        self.Find_Q_Max()
        presentState["Q_value"][self.action] += (LEARNING_RATE * (
            self.reward+(DISCOUNT_RATE*nextState["Q_MAX"])-presentState["Q_value"][self.action]))
        for i in range(len(self.stateSpace)):
            if self.stateSpace[i]["state"] == presentState['state']:
                self.stateSpace[i]["Q_value"][self.action] = presentState["Q_value"][self.action]
        self.Find_Q_Sum()
        api.csv_data_stateSpace(self.stateSpace)

    def updateState(self):
        oldState = self.state.copy()
        self.state = self.takeAction(self.action, self.state)
        print("Present_STATE :",oldState,"Next_STATE :",self.state,"ACTION :",self.action,"Reward :",self.reward)
        return self.state
        
    # def showQMax(self):
    #     qValueMax = 0
    #     StateMax = 0
    #     for i in range(len(self.stateSpace)):
    #         if self.stateSpace[i]["Q_MAX"] > qValueMax:
    #             qValueMax = self.stateSpace[i]["Q_MAX"]
    #             StateMax = i
    #     return print(self.stateSpace[StateMax])
