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
        # self.reward = reward
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
        print(self.state)

    def setTLS(self):
        TrafficLightPhases = []
        G4 = 120-self.state[0]-self.state[1]-self.state[2]
        TrafficLightPhases.append(traci.trafficlight.Phase(
            self.state[0], "rrrrrrrrrrrrGGGG", 0, 0, [], "setViaComplete"))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(3, "rrrrrrrrrrrryyyy", 0, 0))
        TrafficLightPhases.append(traci.trafficlight.Phase(
            self.state[1], "rrrrGGGGrrrrrrrr", 0, 0))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(3, "rrrryyyyrrrrrrrr", 0, 0))
        TrafficLightPhases.append(traci.trafficlight.Phase(
            self.state[2], "GGGGrrrrrrrrrrrr", 0, 0))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(3, "yyyyrrrrrrrrrrrr", 0, 0))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(G4,  "rrrrrrrrGGGGrrrr", 0, 0))
        TrafficLightPhases.append(
            traci.trafficlight.Phase(3, "rrrrrrrryyyyrrrr", 0, 0))
        logic = traci.trafficlight.Logic("InitState", 0, 0, TrafficLightPhases)
        traci.trafficlight.setProgramLogic('gneJ7', logic)

    def get_waiting_time(self):
        wait_time = [0.0, 0.0, 0.0, 0.0]
        keep = True
        lane = [['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
                ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
        while traci.simulation.getMinExpectedNumber() > 0:
            phase = traci.trafficlight.getPhase('gneJ7')
            if phase % 2 == 0 and keep:
                temp = (traci.lane.getWaitingTime(
                    lane[int(phase/2)][0]) + traci.lane.getWaitingTime(lane[int(phase/2)][1])) / 2
                wait_time[int(phase/2)] = temp
                print(temp)
                keep = False
            elif phase == 7:
                print('Avg = ', end='')
                print(sum(wait_time) / len(wait_time))
            elif phase % 2 == 1:
                keep = True

            traci.simulationStep()
        traci.close()
        sys.stdout.flush()

    def randomAction(self):
        print("test_1", self.state)
        action = randrange(0, 6)
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
            self.state = [self.state[0], self.state[1], self.state[2]-15],
        print("test_2", self.state , action)
        return self.state

    def InitStateSpace(self):
        self.stateSpace.append(
            [self.state[0], self.state[1], self.state[2], 0])
        while self.state != [75, 75, 75]:
            self.state[2] += 15
            if self.state[2] == 90:
                self.state[2] = 15
                self.state[1] += 15
                if self.state[1] == 90:
                    self.state[1] = 15
                    self.state[0] += 15
            self.stateSpace.append(
                [self.state[0], self.state[1], self.state[2], 0])
        return self.stateSpace

    def Get_TLS_Fuction(self):
        while traci.simulation.getMinExpectedNumber() > 0:
            if (traci.simulation.getCurrentTime()) == 50000:
                self.state = x.randomAction()
                print(self.state)
                x.setTLS()

            if (traci.simulation.getCurrentTime()) == 100000:
                self.state = x.randomAction()
                print(self.state)
                x.setTLS()
            if (traci.simulation.getCurrentTime()) == 150000:
                self.state = x.randomAction()
                print(self.state)
                x.setTLS()
            # แสดงไฟจราจรทั้งหมด
            # print(traci.trafficlight.getIDList())
            # แสดง State TLS ขณะนั้น
            # print(traci.trafficlight.getRedYellowGreenState('gneJ7'))
            # เวลาที่จะเปลี่ยนเป็น Next State
            # print(traci.trafficlight.getNextSwitch('gneJ7'))
            # เวลาของ State นั้่นๆ
            print(traci.trafficlight.getPhaseDuration('gneJ7'))
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
    x = TrafficLight(State)
    x.setTLS()
    x.Get_TLS_Fuction()

# x = TrafficLight(State)
# # State = x.randomAction()
# test = x.InitStateSpace()
# print(test[0][3])