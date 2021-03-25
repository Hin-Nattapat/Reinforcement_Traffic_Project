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

def printResult(tlsID, result, nextState, nextAction):
    print('\n $$ junction --> ',tlsID)
    print('flowRate    :' ,result['flowRate'])
    print('speed       :' ,result['speed'])
    print('density     :' ,result['density'])
    print('waitingTime :' ,result['waitingTime'])
    print('arrivalRate :' ,result['arrivalRate'])
    print('\nnextstate :', nextState, '| nextAction :', nextAction)
    print('-------------------------------------------------------------')

def runNormal(api, tlsList):
    phase = [0]*len(tlsList)
    tlsID = tlsList
    g_phase = ["rrrrrrrrrGGG", "rrrGGGrrrrrr", "rrrrrrGGGrrr", "GGGrrrrrrrrr"]
    y_phase = ["rrrrrrrrryyy", "rrryyyrrrrrr", "rrrrrryyyrrr", "yyyrrrrrrrrr"]
    traci.simulationStep()
    l_phase = [g_phase[phase[0]], y_phase[phase[0]], 45]
    for tls in tlsID:
        tls.cycle = 48
        tls.setLogic(l_phase)

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        for tls in tlsID:
            index = tlsID.index(tls)
            if tls.isCycleEnd():
                phase[index] = (phase[index] + 1) % 4
                l_phase = [g_phase[phase[index]], y_phase[phase[index]], 45]
                tls.setLogic(l_phase)

def runRL(api, agent, tlsList):
    traci.simulationStep()
    for tls in tlsList:
        tls.action = agent.getAction('e_greedy', tls.currentState)
        phase, tls.moveState = agent.takeAction(tls.action, tls.currentState)
        tls.setLogic(phase)
    while traci.simulation.getMinExpectedNumber() > 0:
        try:
            result = api.simulate()
        except:
            print('Closed')
            return 0
        if result != None:
            for tls in tlsList:
                tls.saveResult(result[tls.id])
        for tls in tlsList:
            if tls.isCycleEnd():
                lastQueue = api.getLastLength(tls.id)
                if sum(lastQueue) == 0:
                    nextState = agent.getRandomState(tls.moveState)
                else:
                    nextState = agent.getNextState(lastQueue, tls.moveState)
                data = tls.getAvgResult()
                agent.update(tls.currentState, nextState, tls.action, data)
                tls.currentState = nextState
                tls.action = agent.getAction('e_greedy', tls.currentState)
                printResult(tls.id, data, nextState, tls.action)
                phase, tls.moveState = agent.takeAction(tls.action, tls.currentState)
                tls.setLogic(phase)                

if __name__ == "__main__":
    numJunc = 4
    agent = []
    tls = []
    state = ['gneE8_1', 'gneE8_0', 'gneE10_1', 'gneE10_0', 'gneE12_1', 'gneE12_0', 'gneE14_1', 'gneE14_0']
    # edgeID = {
    #     'TFL_1' : ['InB_WN_2', 'InB_NW_2', 'Mid_N_2', 'Mid_W_1'],
    #     'TFL_2' : ['Mid_N_1', 'InB_NE_2', 'InB_EN_2', 'Mid_E_1'],
    #     'TFL_3' : ['Mid_S_1', 'Mid_E_2', 'InB_ES_2', 'InB_SE_2'],
    #     'TFL_4' : ['InB_WS_2', 'Mid_W_2', 'Mid_S_2', 'InB_SW_2']
    # }
    edgeID = {
        'TFL_1' : ['InB_WN_2', 'InB_NW_2', 'Mid_NW_2', 'Mid_WN_1'],
        'TFL_2' : ['Mid_NW_1', 'InB_NM_2', 'Mid_NE_2', 'Mid_N_1'],
        'TFL_3' : ['Mid_NE_1', 'InB_NE_2', 'InB_EN_2', 'Mid_EN_1'],
        'TFL_4' : ['InB_WM_2', 'Mid_WN_2', 'Mid_W_2', 'Mid_WS_1'],
        'TFL_5' : ['Mid_W_1', 'Mid_N_2', 'Mid_E_2', 'Mid_S_1'],
        'TFL_6' : ['Mid_E_1', 'Mid_EN_2', 'InB_EM_2', 'Mid_ES_1'],
        'TFL_7' : ['InB_WS_2', 'Mid_WS_2', 'Mid_SW_2', 'InB_SW_2'],
        'TFL_8' : ['Mid_SW_1', 'Mid_S_2', 'Mid_SE_2', 'InB_SM_2'],
        'TFL_9' : ['Mid_SE_1', 'Mid_ES_2', 'InB_ES_2', 'InB_SE_2']
    }
    api = sim_api.Simulation(edgeID)
    agent = RL.Reinforcement(8)
    for junc, edge in edgeID.items():
        tls.append(sim_api.TLScontrol(junc, edge))

    options = get_options()
    
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    
    traci.start([sumoBinary, "-c", "Semester_2/map/36-way/36-way.sumocfg"])
    
    runNormal(api, tls)
    #runRL(api, agent, tls)

traci.close()
sys.stdout.flush() 
# api.plotData()