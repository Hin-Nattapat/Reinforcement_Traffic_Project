import os
import sys
import optparse
import random

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary
import traci
import traci.constants as tc
from random import randrange

EXPLORE_RATE = 0.2
LEARNING_RATE = 0.6
DISCOUNT_RATE = 0.5
MAX_ACTION = 6
num_episodes = 5

# State จะอยู่ในรูปแบบของ [G1,G2,G3] เวลาไฟเขียวแต่ละแยก
# 1 Cycle = 120 วินาที ดังนั้น G4 = 120-G1-G2-G3


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


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
    def __init__(self, state):
        # self.phases = phases
        self.reward = 0.0
        self.state = state
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

    def get_waiting_time(self):
        wait_time = [0.0, 0.0, 0.0, 0.0, 0.0]
        keep = True
        count = 0
        lane = [['gneE3_0', 'gneE3_1'], ['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
                ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
        while count < 5:
            phase = traci.trafficlight.getPhase('gneJ7')
            if phase % 2 == 0 and keep:
                temp = (traci.lane.getWaitingTime(
                    lane[int(phase/2)][0]) + traci.lane.getWaitingTime(lane[int(phase/2)][1]))/2
                wait_time[int(phase/2)] = temp
                print(wait_time, phase)
                keep = False
                count += 1
            elif phase % 2 == 1:
                keep = True
            print("STATE : ", self.state, "PHASE : ", phase, "TIME : ",
                  traci.trafficlight.getPhaseDuration('gneJ7'))
            traci.simulationStep()
        wait_time.pop(0)
        # print("STATE : ", State, "ARRAY REWARD : ", wait_time, "REWARD : ", sum(wait_time) / len(wait_time))
        # print(wait_time)
        self.reward = len(wait_time)/sum(wait_time)
        return self.reward

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
        else:
            return True

    def randomAction(self):
        while True:
            action = randrange(0, MAX_ACTION)
            if self.legalAction(action):
                break
        return action

    def takeAction(self, action):
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

    def InitStateSpace(self):
        State = self.state.copy()
        self.stateSpace.append([[State[0], State[1], State[2]], 0])
        while State != [75, 75, 75]:
            State[2] += 15
            if State[2] == 90:
                State[2] = 15
                State[1] += 15
                if State[1] == 90:
                    State[1] = 15
                    State[0] += 15
            if sum(State) <= 105:
                self.stateSpace.append([[State[0], State[1], State[2]], 0])

    def Find_Q_Statespace(self):
        action = self.randomAction()
        State = self.takeAction(action)
        self.set_Trafficlight()
        self.get_waiting_time()
        # print("STATE : ",State,"REWARD : ",self.reward)
        for i in range(len(self.stateSpace)):
            if self.stateSpace[i][0] == State:
                self.stateSpace[i][1] = self.reward
        print(self.stateSpace)

        traci.load(["-c", "4cross_TLS/1_1Cross.sumocfg"])
        # index = self.stateSpace.index([15, 15, 15, 0])
        # print(index)
        # self.stateSpace[index][1] = self.reward
        # print("test", self.stateSpace)

    def Get_TLS_Fuction(self):
        # print(self.stateSpace)
        while traci.simulation.getMinExpectedNumber() > 0:
            self.Find_Q_Statespace()
            # if (traci.simulation.getCurrentTime()) == 132000:
            #     action = TLS.randomAction()
            #     TLS.takeAction(action)
            #     print(self.state)
            #     TLS.set_Trafficlight()

            # if (traci.simulation.getCurrentTime()) == 264000:
            #     action = TLS.randomAction()
            #     TLS.takeAction(action)
            #     print(self.state)
            #     TLS.set_Trafficlight()

            # แสดงไฟจราจรทั้งหมด
            # print(traci.trafficlight.getIDList())
            # แสดง State TLS ขณะนั้น
            # print(traci.trafficlight.getRedYellowGreenState('gneJ7'))
            # เวลาที่จะเปลี่ยนเป็น Next State
            # print(traci.trafficlight.getNextSwitch('gneJ7'))
            # เวลาของ State นั้่นๆ
            # ######print(traci.trafficlight.getPhaseDuration('gneJ7'))
            # ข้อมูลของ State ทั้งหมด
            # print(traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
            # Index ของ State ไฟจราจรใน file .net.xml
            # print(traci.trafficlight.getPhase('gneJ7'))
            # id ของชุด TLS
            # print(traci.trafficlight.getProgram('gneJ7'))
            traci.simulationStep()
        traci.close()
        sys.stdout.flush()


if __name__ == "__main__":
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    traci.start([sumoBinary, "-c", "4cross_TLS/1_1Cross.sumocfg"])

    State = [15, 15, 15]
    TLS = TrafficLight(State)
    TLS.InitStateSpace()
    TLS.Get_TLS_Fuction()


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
