import os
import sys
import optparse
from sumolib import checkBinary
import traci
import random
import sim_api
import reinforcement as RL

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def printResult(result, nextState):
    print('\nflowRate    :' ,result[0])
    print('speed       :' ,result[1])
    print('density     :' ,result[2])
    print('waitingTime :' ,result[3])
    print('arrivalRate :' ,result[4])
    print('\nnextstate :' ,nextState)
    print('-------------------------------------------------------------')

def runNormal(api, tls):
    i = 0
    g_phase = ["rrrrrrrrrGGG", "rrrGGGrrrrrr", "rrrrrrGGGrrr", "GGGrrrrrrrrr"]
    y_phase = ["rrrrrrrrryyy", "rrryyyrrrrrr", "rrrrrryyyrrr", "yyyrrrrrrrrr"]
    traci.simulationStep()
    while traci.simulation.getMinExpectedNumber() > 0:
        phase = [g_phase[i], y_phase[i], 45]
        tls.set_logic(phase)
        result = api.simulate(48)
        printResult(result ,0)
        i = (i + 1) % 4

def runRL(api, tls, agent):
    traci.simulationStep()
    while traci.simulation.getMinExpectedNumber() > 0:
        action = agent.get_action('p_greedy')
        phase = agent.take_action(action)
        print('action :' ,action ,end=' | ')
        print('duration :',phase[2]+3)
        tls.set_logic(phase)
        try:    
            result = api.simulate(phase[2] + 3)
        except:
            print('closed')
            return 0
        
        lastQueue = api.get_lastLength(state)
        nextState = agent.get_nextState(lastQueue)
        printResult(result, nextState)
        if nextState != None:
            agent.update(nextState, action, result)
    agent.printStateSpace()

if __name__ == "__main__":
    state = ['gneE8_1', 'gneE8_0', 'gneE10_1', 'gneE10_0', 'gneE12_1', 'gneE12_0', 'gneE14_1', 'gneE14_0']
    edge = ['gneE8', 'gneE10', 'gneE12', 'gneE14']
    options = get_options()

    #initial
    api = sim_api.Simulation(edge, state)
    agent = RL.Reinforcement(state, 3)
    tls = sim_api.TLScontrol('gneJ10')

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "Semester_2/map/4-way/4-way.sumocfg"])
    
    #runNormal(api, tls)
    runRL(api, tls, agent)
         
traci.close()
sys.stdout.flush() 