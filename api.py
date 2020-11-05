import traci
import pandas


def get_waiting_time(lane,NextState):
    wait_time = [0.0, 0.0, 0.0, 0.0]
    keep = True
    count = 0
    # print("TEST : "," : ",traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
    set_Trafficlight(NextState)
    traci.simulationStep()
    while traci.simulation.getTime() % 132 != 0 :
        phase = traci.trafficlight.getPhase('gneJ7')
        if phase % 2 == 1 and keep:
            temp = (traci.lane.getWaitingTime(
                lane[int((phase-1)/2)][0]) + traci.lane.getWaitingTime(lane[int((phase-1)/2)][1])) / 2
            wait_time[int((phase-1)/2)] = temp
            keep = False
            count += 1
        elif phase % 2 == 0:
            keep = True
        #print(traci.trafficlight.getPhaseDuration('gneJ7'))
        # print(traci.trafficlight.getNextSwitch('gneJ7'))
        # print(traci.simulation.getTime())
        # if (traci.simulation.getTime() % 132 == 0 and traci.simulation.getTime() != 0):
        #     print("TESTTTTTTTT")
        #     set_Trafficlight(NextState)
        traci.simulationStep()
    return sum(wait_time) / len(wait_time)


def set_Trafficlight(state):
    # print(traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
    # print(state)
    TrafficLightPhases = []
    G4 = 120 - state[0] - state[1] - state[2]
    TrafficLightPhases.append(
        traci.trafficlight.Phase(0, "rrrrrrrrrrrrrrrr", 0, 0))
    TrafficLightPhases.append(traci.trafficlight.Phase(
        state[0], "rrrrrrrrrrrrGGGG", state[0], state[0]))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(3, "rrrrrrrrrrrryyyy", 3, 3))
    TrafficLightPhases.append(traci.trafficlight.Phase(
        state[1], "rrrrGGGGrrrrrrrr", state[1], state[1]))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(3, "rrrryyyyrrrrrrrr", 3, 3))
    TrafficLightPhases.append(traci.trafficlight.Phase(
        state[2], "GGGGrrrrrrrrrrrr", state[2], state[2]))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(3, "yyyyrrrrrrrrrrrr", 3, 3))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(G4,  "rrrrrrrrGGGGrrrr", G4, G4))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(3, "rrrrrrrryyyyrrrr", 3, 3))
    logic = traci.trafficlight.Logic("0", 0, 0, TrafficLightPhases)
    # print("LOGIC : ", logic)
    traci.trafficlight.setProgramLogic('gneJ7', logic)
    # print(traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))

def csv_data_stateSpace(data):
    list_data = [['State','Q_Value','Q_Max','Q_Sum']]
    for item in data:
        temp = []
        temp.extend([item['state'],item['Q_value'],item['Q_MAX'],item['Q_SUM']])
        list_data.append(temp)
    dataframe = pandas.DataFrame(list_data)
    dataframe.to_csv('stateSpace.csv', index=False, header=False, encoding = 'utf-8')
    print(dataframe)
