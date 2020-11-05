import traci
import pandas
import random

def get_waiting_time(lane, NextState):
    wait_time = [0.0, 0.0, 0.0, 0.0]
    keep = True
    count = 0
    # print("TEST : "," : ",traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
    set_Trafficlight(NextState)
    traci.simulationStep()
    while traci.simulation.getTime() % 132 != 0:
        phase = traci.trafficlight.getPhase('gneJ7')
        if phase % 2 == 1 and keep:
            temp = (traci.lane.getWaitingTime(
                lane[int((phase-1)/2)][0]) + traci.lane.getWaitingTime(lane[int((phase-1)/2)][1])) / 2
            wait_time[int((phase-1)/2)] = temp
            keep = False
            count += 1
        elif phase % 2 == 0:
            keep = True
        random_Vehicle()
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
    list_data = [['State', 'Q_Value', 'Q_Max', 'Q_Sum']]
    for item in data:
        temp = []
        temp.extend([item['state'], item['Q_value'],
                     item['Q_MAX'], item['Q_SUM']])
        list_data.append(temp)
    dataframe = pandas.DataFrame(list_data)
    dataframe.to_csv('stateSpace.csv', index=False,header=False, encoding='utf-8')
    print(dataframe)

def add_Route():
    traci.route.add("rou_1", ["gneE43", "gneE3", "gneE6", "gneE40"])
    traci.route.add("rou_2", ["gneE43", "gneE3", "gneE12", "gneE32"])
    traci.route.add("rou_3", ["gneE43", "gneE3", "gneE10", "gneE34"])
    traci.route.add("rou_4", ["gneE41", "gneE7", "gneE8", "gneE42"])
    traci.route.add("rou_5", ["gneE41", "gneE7", "gneE12", "gneE32"])
    traci.route.add("rou_6", ["gneE41", "gneE7", "gneE10", "gneE34"])
    traci.route.add("rou_7", ["gneE35", "gneE11", "gneE8", "gneE42"])
    traci.route.add("rou_8", ["gneE35", "gneE11", "gneE6", "gneE40"])
    traci.route.add("rou_9", ["gneE35", "gneE11", "gneE12", "gneE32"])
    traci.route.add("rou_10", ["gneE33", "gneE13", "gneE8", "gneE42"])
    traci.route.add("rou_11", ["gneE33", "gneE13", "gneE6", "gneE40"])
    traci.route.add("rou_12", ["gneE33", "gneE13", "gneE10", "gneE34"])
    # traci.route.add("rou_10", ["gneE43", "gneE3", "gneE6", "gneE7", "gneE12", "gneE32"])
    # traci.route.add("rou_11", ["gneE43", "gneE3", "gneE6", "gneE7", "gneE10", "gneE34"])
    # traci.route.add("rou_12", ["gneE43", "gneE3", "gneE6", "gneE7", "gneE8", "gneE42"])
    # traci.route.add("rou_13", ["gneE43", "gneE3", "gneE12", "gneE13", "gneE6", "gneE40"])
    # traci.route.add("rou_14", ["gneE43", "gneE3", "gneE12", "gneE13", "gneE10", "gneE34"])
    # traci.route.add("rou_15", ["gneE43", "gneE3", "gneE12", "gneE13", "gneE8", "gneE42"])
    # traci.route.add("rou_16", ["gneE43", "gneE3", "gneE10", "gneE11", "gneE12", "gneE32"])
    # traci.route.add("rou_17", ["gneE43", "gneE3", "gneE10", "gneE11", "gneE6", "gneE40"])
    # traci.route.add("rou_18", ["gneE43", "gneE3", "gneE10", "gneE11", "gneE8", "gneE42"])
    # traci.route.add("rou_19", ["gneE41", "gneE7", "gneE8", "gneE3", "gneE12", "gneE32"])
    # traci.route.add("rou_20", ["gneE41", "gneE7", "gneE8", "gneE3", "gneE10", "gneE34"])
    # traci.route.add("rou_21", ["gneE41", "gneE7", "gneE8", "gneE3", "gneE6", "gneE40"])
    # traci.route.add("rou_22", ["gneE41", "gneE7", "gneE12", "gneE13", "gneE6", "gneE40"])
    # traci.route.add("rou_23", ["gneE41", "gneE7", "gneE12", "gneE13", "gneE10", "gneE34"])
    # traci.route.add("rou_24", ["gneE41", "gneE7", "gneE12", "gneE13", "gneE8", "gneE42"])
    # traci.route.add("rou_25", ["gneE41", "gneE7", "gneE10", "gneE11", "gneE12", "gneE32"])
    # traci.route.add("rou_26", ["gneE41", "gneE7", "gneE10", "gneE11", "gneE6", "gneE40"])
    # traci.route.add("rou_27", ["gneE41", "gneE7", "gneE10", "gneE11", "gneE8", "gneE42"])
    # traci.route.add("rou_28", ["gneE33", "gneE13", "gneE8", "gneE3", "gneE12", "gneE32"])
    # traci.route.add("rou_29", ["gneE33", "gneE13", "gneE8", "gneE3", "gneE10", "gneE34"])
    # traci.route.add("rou_30", ["gneE33", "gneE13", "gneE8", "gneE3", "gneE6", "gneE40"])
    # traci.route.add("rou_31", ["gneE33", "gneE13", "gneE6", "gneE7", "gneE12", "gneE32"])
    # traci.route.add("rou_32", ["gneE33", "gneE13", "gneE6", "gneE7", "gneE10", "gneE34"])
    # traci.route.add("rou_33", ["gneE33", "gneE13", "gneE6", "gneE7", "gneE8", "gneE42"])
    # traci.route.add("rou_34", ["gneE33", "gneE13", "gneE10", "gneE11", "gneE12", "gneE32"])
    # traci.route.add("rou_35", ["gneE33", "gneE13", "gneE10", "gneE11", "gneE6", "gneE40"])
    # traci.route.add("rou_36", ["gneE33", "gneE13", "gneE10", "gneE11", "gneE8", "gneE42"])
    # traci.route.add("rou_37", ["gneE35", "gneE11", "gneE8", "gneE3", "gneE12", "gneE32"])
    # traci.route.add("rou_38", ["gneE35", "gneE11", "gneE8", "gneE3", "gneE10", "gneE34"])
    # traci.route.add("rou_39", ["gneE35", "gneE11", "gneE8", "gneE3", "gneE6", "gneE40"])
    # traci.route.add("rou_40", ["gneE35", "gneE11", "gneE6", "gneE7", "gneE12", "gneE32"])
    # traci.route.add("rou_41", ["gneE35", "gneE11", "gneE6", "gneE7", "gneE10", "gneE34"])
    # traci.route.add("rou_42", ["gneE35", "gneE11", "gneE6", "gneE7", "gneE8", "gneE42"])
    # traci.route.add("rou_43", ["gneE35", "gneE11", "gneE12", "gneE13", "gneE10", "gneE34"])
    # traci.route.add("rou_44", ["gneE35", "gneE11", "gneE12", "gneE13", "gneE6", "gneE40"])
    # traci.route.add("rou_45", ["gneE35", "gneE11", "gneE12", "gneE13", "gneE8", "gneE42"])


def random_Vehicle():
    i = traci.simulation.getTime()
    if i % 2 == 0 :
        RouteID = traci.route.getIDList()
        count = traci.route.getIDCount()
        index = random.randint(0, count-1)
        traci.vehicle.add("vehicle_"+str(i),RouteID[index], departSpeed="desired",)
        traci.vehicle.setMaxSpeed("vehicle_"+str(i), 25.0)
    
