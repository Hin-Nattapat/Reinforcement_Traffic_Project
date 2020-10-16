import os
import sys
import optparse
import random
import traci
import api

EXPLORE_RATE = 0.2
LEARNING_RATE = 0.6
DISCOUNT_RATE = 0.5
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
        self.action = [
            [self.state[0]+15, self.state[1], self.state[2]],
            [self.state[0]-15, self.state[1], self.state[2]],
            [self.state[0], self.state[1]+15, self.state[2]],
            [self.state[0], self.state[1]-15, self.state[2]],
            [self.state[0], self.state[1], self.state[2]+15],
            [self.state[0], self.state[1], self.state[2]-15],
        ]
        self.maxQ = 0.0

    def legalAction(self, action, State):
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
        elif sum(State) > 105:
            return False
        else:
            return True

        # tot style
        # for state_list in self.stateSpace:
        #     if State == state_list[0]:
        #         return True
        # return False

    def randomAction(self):
        while True:
            action = random.randrange(0, MAX_ACTION)
            if self.legalAction(action,self.state):
                break
        return action

    def get_nextState(self, action, State):
        state = self.takeAction(action, State)
        return state

    def get_state(self):
        for i in range(len(self.stateSpace)):
            if self.stateSpace[i]["state"] == self.state:
                state = self.stateSpace[i]
        return state

    def takeAction(self, action, State):
        # State = self.state.copy()
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
        State = self.state.copy()
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
        return print(self.stateSpace)

    def Find_Q_initState(self):
        print("--------------- RUN TIME ---------------")
        for i in range(len(self.stateSpace)):
            tempState = self.stateSpace[i]['state'].copy()
            for j in range(MAX_ACTION):
                if self.legalAction(j, tempState):
                    takeActionState = self.get_nextState(j,tempState)
                    api.set_Trafficlight(takeActionState)
                    Reward = 1/api.get_waiting_time(self.lane)
                    self.stateSpace[i]["Q_value"][j] = Reward

                    if self.stateSpace[34]["Q_value"][5] == 0:
                        traci.load(["-c", "4cross_TLS/1_1Cross.sumocfg"])
                    else:
                        traci.close()
                else:
                    Reward = -1
                    self.stateSpace[i]["Q_value"][j] = Reward
        print(self.stateSpace)
        print("----------------------------------------")

    def Find_Q_Max(self):
        for i in range(len(self.stateSpace)):
            Q_MAX = max(self.stateSpace[i]['Q_value'])
            self.stateSpace[i]["Q_MAX"] = Q_MAX

    def Find_Q_Sum(self):
        for i in range(len(self.stateSpace)):
            tempState = self.stateSpace[i]['state'].copy()
            Q_SUM = 0.0
            for j in range(MAX_ACTION):
                if self.legalAction(j,tempState):
                    # print("state : ", tempState,"Q_value : ", self.stateSpace[i]['Q_value'][j])
                    Q_SUM += self.stateSpace[i]['Q_value'][j]
                    self.stateSpace[i]['Q_SUM'] = Q_SUM

    # def save_reward(self):
    #     count = 0
    #     self.complete = False
    #     for i in range(len(self.stateSpace)):
    #         if self.stateSpace[i][0] == self.state:
    #             if self.stateSpace[i][1] == 0 or self.stateSpace[i][1] < self.reward:
    #                 self.stateSpace[i][1] = self.reward

    #         if self.stateSpace[i][1] != 0:
    #             count += 1
    #         if count == len(self.stateSpace):
    #             self.complete = True

    #     print(self.stateSpace)
    #     print("Remaining state : ", len(self.stateSpace)-count)

    # def Greedy_Al(self):
    #     Q_Max = 0
    #     Action_Max = 0
    #     for i in range(MAX_ACTION):
    #         action = self.legalAction(i)
    #         if action:
    #             tempState = self.takeAction(i)
    #             print(tempState)
    #             for j in range(len(self.stateSpace)):
    #                 if self.stateSpace[j][0] == tempState:
    #                     if self.stateSpace[j][1] > Q_Max:
    #                         Q_Max = self.stateSpace[j][1]
    #                         Action_Max = i
    #     return Action_Max

    def P_Greedy_Al(self):
        randomNumber = random.uniform(0, 1)
        if (EXPLORE_RATE > randomNumber):
            return self.randomAction()
        else:
            action = self.randomAction()
            for i in range(MAX_ACTION):
                if self.legalAction(action,self.state):
                    presentState = self.get_state()
                    prob = presentState["Q_value"][action] / presentState["Q_SUM"]
                    print(prob)

