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

def runRL(api, tls, agent,side):
    traci.simulationStep()
    print('----------------side =>'+str(side+1)+'--------------------')
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
    print('----------------------------------------')

if __name__ == "__main__":
    state_1 = ['InB_WN_2_0', 'InB_WN_2_1', 'InB_NW_2_0', 'InB_NW_2_1', 'Mid_N_2_0', 'Mid_N_2_1', 'Mid_W_1_0', 'Mid_W_1_1']
    edge_1 = ['InB_WN_2', 'InB_NW_2', 'Mid_N_2', 'Mid_W_1']

    state_2 = ['Mid_N_1_0', 'Mid_N_1_1', 'InB_NE_2_0', 'InB_NE_2_1', 'InB_EN_2_0', 'InB_EN_2_1', 'Mid_E_1_0', 'Mid_E_1_1']
    edge_2 = ['Mid_N_1', 'InB_NE_2', 'InB_EN_2', 'Mid_E_1']

    state_3 = ['Mid_S_1_0', 'Mid_S_1_1', 'Mid_E_2_0', 'Mid_E_2_1', 'InB_ES_2_0', 'InB_ES_2_1', 'InB_SE_2_0', 'InB_SE_2_1']
    edge_3 = ['Mid_S_1', 'Mid_E_2', 'InB_ES_2', 'InB_SE_2']

    state_4 = ['InB_WS_2_0', 'InB_WS_2_1', 'Mid_W_2_0', 'Mid_W_2_1', 'Mid_S_2_0', 'Mid_S_2_1', 'InB_SW_2_0', 'InB_SW_2_1']
    edge_4 = ['InB_WS_2', 'Mid_W_2', 'Mid_S_2', 'InB_SW_2']

    options = get_options()

    state = [state_1,state_2,state_3,state_4]
    edge = [edge_1,edge_2,edge_3,edge_4]
    api = [None,None,None,None]
    agent = [None,None,None,None]
    tls = [None,None,None,None]
    
    #initial
    for i in range (4):
        api[i] = sim_api.Simulation(edge[i], state[i])
        agent[i] = RL.Reinforcement(state[i], 3)
        tls[i] = sim_api.TLScontrol('TFL_'+str((i+1)))

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "Semester_2/map/16-way/16-way.sumocfg"])
    
    #runNormal(api, tls)

    # runRL(api[1], tls[1], agent[1],1)

         
traci.close()
sys.stdout.flush() 
# api.plotData()