import os
import sys
import optparse
from sumolib import checkBinary
import traci
import random
import sim_api
import paperRL as PRL
import smarterRL as SRL
import csv_api as CSV
import constant as const

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

def runNormal(api, tlsList, csvManage, csvRew):
    epoch = 0
    count = 0
    greenTime = 60
    phase = [0]*len(tlsList)
    tlsID = tlsList
    g_phase = ["rrrrrrrrrGGG", "rrrGGGrrrrrr", "rrrrrrGGGrrr", "GGGrrrrrrrrr"]
    y_phase = ["rrrrrrrrryyy", "rrryyyrrrrrr", "rrrrrryyyrrr", "yyyrrrrrrrrr"]
    traci.simulationStep()
    l_phase = [g_phase[phase[0]], y_phase[phase[0]], greenTime]
    for tls in tlsID:
        tls.cycle = greenTime + 3
        tls.setLogic(l_phase)
    while (traci.simulation.getMinExpectedNumber() - traci.vehicle.getIDCount() != 0):
        # try:
        #     result = api.simulate()
        # except:
        #     print('Closed')
        #     return 0
        result = api.simulate()
        if result != None:
            csvManage.saveAvgResult(result[1])
            for tls in tlsID:
                tls.saveResult(result[0][tls.id])
        for tls in tlsID:
            index = tlsID.index(tls)
            if tls.isCycleEnd():
                phase[index] = (phase[index] + 1) % 4
                count += 1
                l_phase = [g_phase[phase[index]], y_phase[phase[index]], greenTime]
                tls.setLogic(l_phase)
                if count == len(phase):
                    count = 0
                    epoch += 1
                    csvRew.saveAvgResult([epoch, greenTime])                    

def runPRL(api, agent, tlsList, csvManage, csvRew):
    traci.simulationStep()
    for tls in tlsList:
        tls.action = agent.getAction('e_greedy', tls.currentState)
        phase, tls.moveState = agent.takeAction(tls.action, tls.currentState)
        tls.setLogic(phase)
    while (traci.simulation.getMinExpectedNumber() - traci.vehicle.getIDCount() != 0):
        try:
            result = api.simulate()
        except:
            print('Closed')
            return 0
        if result != None:
            print(result)
            csvManage.saveAvgResult(result[1])
            for tls in tlsList:
                tls.saveResult(result[0][tls.id])
        for tls in tlsList:
            if tls.isCycleEnd():
                lastQueue = api.getLastLength(tls.id)
                if sum(lastQueue) == 0:
                    nextState = agent.getRandomState(tls.moveState)
                else:
                    nextState = agent.getNextState(lastQueue, tls.moveState)
                data = tls.getAvgResult()
                reward = agent.update(tls.currentState, nextState, tls.action, data)
                if reward != None:
                    csvRew.saveAvgResult(reward)
                tls.currentState = nextState
                tls.action = agent.getAction('e_greedy', tls.currentState)
                printResult(tls.id, data, nextState, tls.action)
                phase, tls.moveState = agent.takeAction(tls.action, tls.currentState)
                tls.setLogic(phase)

def runSRL(api, agent, tlsList, csvManage, csvRew):
    traci.simulationStep()
    for tls in tlsList:
        tls.action = agent.getAction('e_greedy', tls.currentState)
        phase, tls.moveState = agent.takeAction(tls.action, tls.currentState)
        # print(tls.getNextLane())
        phase[2] = agent.getGreenTime(tls.getMoveLane(), tls.getNextLane())
        tls.setLogic(phase)
    while (traci.simulation.getMinExpectedNumber() - traci.vehicle.getIDCount() != 0):
        try:
            result = api.simulate()
        except:
            print('Closed')
            return 0
        if result != None:
            # print(result)
            csvManage.saveAvgResult(result[1])
            for tls in tlsList:
                tls.saveResult(result[0][tls.id])
        for tls in tlsList:
            if tls.isCycleEnd():
                lastQueue = api.getLastLength(tls.id)
                waitingTime = api.getLastWaiting(tls.id)
                print(lastQueue, waitingTime)
                if sum(lastQueue) == 0:
                    nextState = agent.getRandomState(tls.moveState)
                else:
                    nextState = agent.getNextState(lastQueue, tls.moveState, waitingTime)
                # print(tls.cycle)
                data = tls.getAvgResult()
                reward = agent.update(tls.currentState, nextState, tls.action, data)
                if reward != None:
                    csvRew.saveAvgResult(reward)
                tls.currentState = nextState
                tls.action = agent.getAction('e_greedy', tls.currentState)
                printResult(tls.id, data, nextState, tls.action)
                phase, tls.moveState = agent.takeAction(tls.action, tls.currentState)
                phase[2] = agent.getGreenTime(tls.getMoveLane(), tls.getNextLane())
                tls.setLogic(phase)

if __name__ == "__main__":
    solution = 'SRL'
    route = 'p3'
    runningMap = 16

    maxState = 8
    tls = []
    edgeID = {}
    nextLane = {}
    avgSPD = 0
    avgDEN = 0
    maxWait = 0
    if runningMap == 4:
        edgeID = const.edge_4
        nextLane = const.nextEdge_4
        avgSPD = const.avgSPD_4
        avgDEN = const.avgDEN_4
        maxWait = const.maxWT_4
    elif runningMap == 16:
        edgeID = const.edge_16
        nextLane = const.nextEdge_16
        avgSPD = const.avgSPD_16
        avgDEN = const.avgDEN_16
        maxWait = const.maxWT_16
    elif runningMap == 36:
        edgeID = const.edge_36
        nextLane = const.nextEdge_36
        avgSPD = const.avgSPD_36
        avgDEN = const.avgDEN_36
        maxWait = const.maxWT_36

    savePath = "Semester_2/map/%s-way/result/%s_result_%s.csv" % (runningMap, solution, route) #ต้องไปเติมว่าเป็น 16-way กับ Period อะไรมาเพิ่ม ทำเป็นโครงอยู่บรรทัดล่าง
    savePath2 = "Semester_2/map/%s-way/result/%s_reward_%s.csv" % (runningMap, solution, route)
    startPath = ""

    if route == 'p1':
        startPath = "Semester_2/map/%s-way/config/%s-way-1.sumocfg" %(runningMap, runningMap)
    elif route == 'p2':
        startPath = "Semester_2/map/%s-way/config/%s-way-2.sumocfg" %(runningMap, runningMap)
    elif route == 'p3':
        startPath = "Semester_2/map/%s-way/config/%s-way-3.sumocfg" %(runningMap, runningMap)

    api = sim_api.Simulation(edgeID)
    agent = 0
    csvResult = 0
    csvRew = 0
    if solution == 'fix':
        csvResult = CSV.Csv_api(savePath, ['time','avgFlowRate','avgSpeed','avgDensity','avgWaiting','avgQLength'])
        csvRew = CSV.Csv_api(savePath2, ['epoch','greenTime'])
    elif solution == 'PRL':
        agent = PRL.Reinforcement(8, len(edgeID))
        csvResult = CSV.Csv_api(savePath, ['time','avgFlowRate','avgSpeed','avgDensity','avgWaiting','avgQLength'])
        csvRew = CSV.Csv_api(savePath2, ['epoch','greenTime','reward'])
    elif solution == 'SRL':
        agent = SRL.Reinforcement(8, len(edgeID), avgSPD, avgDEN, maxWait)
        csvResult = CSV.Csv_api(savePath, ['time','avgFlowRate','avgSpeed','avgDensity','avgWaiting','avgQLength'])
        csvRew = CSV.Csv_api(savePath2, ['epoch','greenTime','reward'])

    for junc, edge in edgeID.items():
        tls.append(sim_api.TLScontrol(junc, edge, nextLane[junc]))

    options = get_options()
    
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    
    traci.start([sumoBinary, "-c", startPath])

    if solution == 'fix':
        runNormal(api, tls, csvResult, csvRew)
        print('Complete')
    elif solution == 'PRL':
        runPRL(api, agent, tls, csvResult, csvRew)
        print('Complete')
    elif solution == 'SRL':
        runSRL(api, agent, tls, csvResult, csvRew)
        print('Complete')

traci.close()
sys.stdout.flush()
# api.plotData()

