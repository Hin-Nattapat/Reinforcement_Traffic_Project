import traci

def get_waiting_time(lane):

    wait_time = [0.0, 0.0, 0.0, 0.0, 0.0]
    keep = True
    count = 0
    # print("TEST : "," : ",traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
    while count < 6:
        phase = traci.trafficlight.getPhase('gneJ7')
        if phase % 2 == 0 and keep:
            temp = (traci.lane.getWaitingTime(
                lane[int(phase/2)][0]) + traci.lane.getWaitingTime(lane[int(phase/2)][1])) / 2
            wait_time[int(phase/2)] = temp
            # print(wait_time)
            
            keep = False
            count += 1    
        elif phase % 2 == 1:
            keep = True 
        print(traci.trafficlight.getPhaseDuration('gneJ7'))
        if (count == 5):
            set_Trafficlight([15,15,15])
        traci.simulationStep()
    wait_time.pop(1)
    return sum(wait_time) / len(wait_time)

def set_Trafficlight(state):
    # print(traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
    TrafficLightPhases = []
    G4 = 120 - state[0] - state[1] - state[2]
    TrafficLightPhases.append(
        traci.trafficlight.Phase(0, "rrrrrrrrrrrrrrrr", 0, 0))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(45, "rrrrrrrrrrrrrrrr", 35, 35))
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
        traci.trafficlight.Phase(3, "rrrrrrrryyyyrrrr", 0, 0))
    logic = traci.trafficlight.Logic("initState", 0, 0, TrafficLightPhases)
    # print("LOGIC : ", logic)
    traci.trafficlight.setProgramLogic('gneJ7', logic)
    # print(traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))