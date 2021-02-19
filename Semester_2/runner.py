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

def runRL(api, agent, tls):
    traci.simulationStep()
    while traci.simulation.getMinExpectedNumber() > 0:
        action = agent.get_action('p_greedy')
        phase = agent.take_action(action)
        tls.set_logic(phase)
        result = api.simulate(phase[2] + 3)
        lastQueue = api.get_lastLength(state)
        next_state = agent.get_nextState(lastQueue)
        print(next_state)
        agent.update(next_state, action, result)

def run_normal(api, tls):
    i = 0
    g_phase = ["rrrrrrrrrGGG", "rrrGGGrrrrrr", "rrrrrrGGGrrr", "GGGrrrrrrrrr"]
    y_phase = ["rrrrrrrrryyy", "rrryyyrrrrrr", "rrrrrryyyrrr", "yyyrrrrrrrrr"]
    traci.simulationStep()
    while traci.simulation.getMinExpectedNumber() > 0:
        phase = [g_phase[i], y_phase[i], 45]
        tls.set_logic(phase)
        result = api.simulate(48)
        print(result)
        i = (i + 1) % 4

if __name__ == "__main__":
    state = ['InB_W_2_0', 'InB_W_2_1', 'InB_N_2_0', 'InB_N_2_1', 'InB_E_2_0', 'InB_E_2_1', 'InB_S_2_0', 'InB_S_2_1']
    edge = ['InB_W_2', 'InB_N_2', 'InB_E_2', 'InB_S_2']
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    path_4Cross = os.path.abspath('Semester_2\\map\\4-way\\4-way.sumocfg')
    # path_16Cross = os.path.abspath('Semester_2\\map\\16-way\\16-way.sumocfg')
    traci.start([sumoBinary, "-c", path_4Cross])

    #initial
    api = sim_api.Simulation(edge)
    agent = RL.Reinforcement(state, 3)
    tls = sim_api.TLScontrol('Center_TFL')

    #runRL(api, agent, tls)
    run_normal(api, tls)
    #run_dynTime(api, agent, tls)
            
    traci.close()
    sys.stdout.flush()
