# import os
# import sys
# import optparse
# import random
# from sumolib import checkBinary
import traci
import traci.constants as tc


EXPLORE_RATE = 0.2
LEARNING_RATE = 0.6
DISCOUNT_RATE = 0.5
MAX_ACTION = 6
num_episodes = 5

# State จะอยู่ในรูปแบบของ [G1,G2,G3] เวลาไฟเขียวแต่ละแยก 
# 1 Cycle = 120 วินาที ดังนั้น G4 = 120-G1-G2-G3
State = [15, 15, 15]
ACTION = [
    [State[0]+15, State[1], State[2]],
    [State[0]-15, State[1], State[2]],
    [State[0], State[1]+15, State[2]],
    [State[0], State[1]-15, State[2]],
    [State[0], State[1], State[2]+15],
    [State[0], State[1], State[2]-15],
]
Q_value = 0
StateSpace = []
# print(ACTION)

class StateAction:
    def __init__(self, action, q_value):
        self.action = action
        self.q_value = q_value
    def getData(self):
        return [self.action,self.q_value]

def setTLS():
    TrafficLightPhases = []
    G4 = 120-State[0]-State[1]-State[2]
    TrafficLightPhases.append(traci.trafficlight.Phase(State[0], "rrrrrrrrrrrrGGGG", 0, 0, [], "setViaComplete"))
    TrafficLightPhases.append(traci.trafficlight.Phase(3, "rrrrrrrrrrrryyyy", 0, 0))
    TrafficLightPhases.append(traci.trafficlight.Phase(State[1], "rrrrGGGGrrrrrrrr", 0, 0))
    TrafficLightPhases.append(traci.trafficlight.Phase(3, "rrrryyyyrrrrrrrr", 0, 0))
    TrafficLightPhases.append(traci.trafficlight.Phase(State[2], "GGGGrrrrrrrrrrrr", 0, 0))
    TrafficLightPhases.append(traci.trafficlight.Phase(3, "yyyyrrrrrrrrrrrr", 0, 0))
    TrafficLightPhases.append(traci.trafficlight.Phase(G4,  "rrrrrrrrGGGGrrrr", 0, 0))
    TrafficLightPhases.append(traci.trafficlight.Phase(3, "rrrrrrrryyyyrrrr", 0, 0))
    logic = traci.trafficlight.Logic("InitState", 0, 0, TrafficLightPhases)
    # traci.trafficlight.setProgramLogic('gneJ7', logic)

print(StateSpace)
data = StateAction(ACTION[0],2)
print(data.q_value)


# setTLS()
# for episode in range(num_episodes):

    

#############################################    Sumo    #############################################

# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("please declare environment variable 'SUMO_HOME'")

# def get_options():
#     optParser = optparse.OptionParser()
#     optParser.add_option("--nogui", action="store_true",
#                          default=False, help="run the commandline version of sumo")
#     options, args = optParser.parse_args()
#     return options

# if __name__ == "__main__":
#     options = get_options()
#     if options.nogui:
#         sumoBinary = checkBinary('sumo')
#     else:
#         sumoBinary = checkBinary('sumo-gui')
#     traci.start([sumoBinary, "-c", "4cross_TLS/1_1Cross.sumocfg"])

######################################################################################################
