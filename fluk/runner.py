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

if __name__ == "__main__":
    state = ['gneE8_1', 'gneE8_0', 'gneE10_1', 'gneE10_0', 'gneE12_1', 'gneE12_0', 'gneE14_1', 'gneE14_0']
    edge = ['gneE8', 'gneE10', 'gneE12', 'gneE14']
    options = get_options()

    #initial
    api = sim_api.Simulation(edge)
    agent = RL.Reinforcement(1, state, 3)
    tls = sim_api.TLScontrol('gneJ10')

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "map/4-way/4-way.sumocfg"])
    
    traci.simulationStep()
    while traci.simulation.getMinExpectedNumber() > 0:
        action = agent.get_action('p_greedy')
        phase = agent.take_action(action)
        print('action : ' ,end='')
        print(action ,end=' -- ')
        print('duration : ', end='')
        print(phase[2] + 3)
        tls.set_logic(phase)
        result = api.simulate(phase[2] + 3)
        lastQueue = api.get_lastLength(state)
        next_state = agent.get_nextState(lastQueue)
        agent.update(next_state, action, result)
        # result = api.simulate(20)
        # length = api.get_lastLength(state)
        
    traci.close()
    sys.stdout.flush()