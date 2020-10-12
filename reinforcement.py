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
        # print(self.state)

    def set_Trafficlight(self):
        print(traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
        TrafficLightPhases = []
        G4 = 120-self.state[0]-self.state[1]-self.state[2]
        TrafficLightPhases.append(
            traci.trafficlight.Phase(0, "rrrrrrrrrrrrrrrr", 0, 0))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(45, "rrrrrrrrrrrrrrrr", 35, 35))
        TrafficLightPhases.append(traci.trafficlight.Phase(
            self.state[0], "rrrrrrrrrrrrGGGG", self.state[0], self.state[0]))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(3, "rrrrrrrrrrrryyyy", 3, 3))
        TrafficLightPhases.append(traci.trafficlight.Phase(
            self.state[1], "rrrrGGGGrrrrrrrr", self.state[1], self.state[1]))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(3, "rrrryyyyrrrrrrrr", 3, 3))
        TrafficLightPhases.append(traci.trafficlight.Phase(
            self.state[2], "GGGGrrrrrrrrrrrr", self.state[2], self.state[2]))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(3, "yyyyrrrrrrrrrrrr", 3, 3))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(G4,  "rrrrrrrrGGGGrrrr", G4, G4))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(3, "rrrrrrrryyyyrrrr", 0, 0))
        logic = traci.trafficlight.Logic("InitState", 0, 0, TrafficLightPhases)
        print("LOGIC : ", logic)
        traci.trafficlight.setProgramLogic('gneJ7', logic)


    def legalAction(self, action):
        State = self.state.copy()
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

    def randomAction(self):
        while True:
            action = random.randrange(0, MAX_ACTION)
            if self.legalAction(action):
                break
        return action

    def takeAction(self, action):
        State = self.state.copy()
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
        self.stateSpace.append([[State[0], State[1], State[2]], 0, 0])
        while State != [75, 75, 75]:
            State[2] += 15
            if State[2] == 90:
                State[2] = 15
                State[1] += 15
                if State[1] == 90:
                    State[1] = 15
                    State[0] += 15
            if sum(State) <= 105:
                self.stateSpace.append([[State[0], State[1], State[2]], 0, 0])

    def Find_Q_initState(self):
        print("--------------- RUN TIME ---------------")
        action = self.randomAction()
        self.state = self.get_state(action)
        api.set_Trafficlight(self.state)
        Reward = api.get_waiting_time(self.lane)

        if Reward > 0:
            self.reward = 1 / Reward
        else:
            self.reward = -1

        self.save_reward()
        print("----------------------------------------")

        if self.complete == False:
            traci.load(["-c", "4cross_TLS/1_1Cross.sumocfg"])
    
    def get_state(self, action):
        state = self.takeAction(action)
        return state

    def save_reward(self):
        count = 0
        self.complete = False
        for i in range(len(self.stateSpace)):
            if self.stateSpace[i][0] == self.state:
                if self.stateSpace[i][1] == 0 or self.stateSpace[i][1] < self.reward:
                    self.stateSpace[i][1] = self.reward  

            if self.stateSpace[i][1] != 0:
                count += 1
            if count == len(self.stateSpace):
                self.complete = True

        print(self.stateSpace)
        print("Remaining state : ", len(self.stateSpace)-count)
        

    def Greedy_Al(self):
        Q_Max = 0
        Action_Max = 0
        for i in range(MAX_ACTION):
            action = self.legalAction(i)
            if action:
                tempState = self.takeAction(i)
                print(tempState)
                for j in range(len(self.stateSpace)):
                    if self.stateSpace[j][0] == tempState:
                        if self.stateSpace[j][1] > Q_Max:
                            Q_Max = self.stateSpace[j][1]
                            Action_Max = i
        return Action_Max
    

    # def P_Greedy_Al(self):
    #     randomNumber = random.uniform(0, 1)
    #     if (EXPLORE_RATE > randomNumber):
    #         return self.randomAction()
    #     else:
    #         action = self.randomAction()
    #         for i in range(MAX_ACTION):
    #             if legalAction(action):
    #                 prob = 
             




    # def Get_TLS_Fuction(self):
    #     # print(self.stateSpace)
    #     while traci.simulation.getMinExpectedNumber() > 0:
    #         self.Find_Q_Statespace()
    #         traci.simulationStep()
    #     traci.close()
    #     sys.stdout.flush()


# if __name__ == "__main__":
#     options = get_options()
#     if options.nogui:
#         sumoBinary = checkBinary('sumo')
#     else:
#         sumoBinary = checkBinary('sumo-gui')
#     traci.start([sumoBinary, "-c", "4cross_TLS/1_1Cross.sumocfg"])

#     State = [15, 15, 15]
#     TLS = TrafficLight(State)
#     TLS.InitStateSpace()
#     TLS.Get_TLS_Fuction()


# State = [15, 15, 15]
# TLS = TrafficLight(State)
# test = TLS.randomAction()
# print(test)
# TLS.findMaxQ()
# State = TLS.randomAction()


# TLS.InitStateSpace()
# print(test)
# index = test.index([[15,15,30],0])
# print(index)
