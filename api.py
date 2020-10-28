import traci

class API():
    def __init__(self):
        self.wait_time = 0
        self.keep = True
        self.lane = [['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
            ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
        self.result = {
            "w_time" : None,
            "dens" : None,
            "avg_spd" : None,
            "f_rate" : None
        }

    
    def get_obj(self, nextState):
        self.wait_time = [0.0, 0.0, 0.0, 0.0]
        self.keep = True
        self.set_Trafficlight(nextState)
        traci.simulationStep()
        while traci.simulation.getTime() % 132 != 0:
            self.get_waiting_time()
            traci.simulationStep()
        
        #collect all result
        self.result['w_time'] = sum(self.wait_time) / len(self.wait_time)
        return self.result

    def get_waiting_time(self):
        phase = traci.trafficlight.getPhase('gneJ7')
        if phase % 2 == 1 and self.keep:
            temp = (traci.lane.getWaitingTime(
                self.lane[int((phase-1)/2)][0]) + traci.lane.getWaitingTime(self.lane[int((phase-1)/2)][1])) / 2.0           
            self.wait_time[int((phase-1)/2)] = temp
            self.keep = False
        elif phase % 2 == 0:
            self.keep = True
 
    def set_Trafficlight(self, state):
        print(state)
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
        traci.trafficlight.setProgramLogic('gneJ7', logic)

def get_waiting_time(lane,NextState):
    wait_time = [0.0, 0.0, 0.0, 0.0]
    keep = True
    # print("TEST : "," : ",traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
    #set_Trafficlight(NextState)
    traci.simulationStep()
    while traci.simulation.getTime() % 72 != 0 :
        phase = traci.trafficlight.getPhase('gneJ7')
        if phase % 2 == 0 and keep:
            temp = (traci.lane.getWaitingTime(lane[int((phase)/2)][0]) 
             + traci.lane.getWaitingTime(lane[int((phase)/2)][1])) / 2
            wait_time[int((phase)/2)] = temp
            print(wait_time)
            keep = False
        elif phase % 2 == 1:
            keep = True

        # print(traci.trafficlight.getPhaseDuration('gneJ7'))
        # print(traci.trafficlight.getNextSwitch('gneJ7'))
        # print(traci.simulation.getTime())
        # if (traci.simulation.getTime() % 132 == 0 and traci.simulation.getTime() != 0):
        #     print("TESTTTTTTTT")
        #     set_Trafficlight(NextState)
        traci.simulationStep()
    return sum(wait_time) / len(wait_time)

# def get_velocity():
#     while traci.simulation.getMinExpectedNumber() > 0:
#         traci.simulationStep()
#         veh_id = traci.vehicle.getIDList()
#         veh_list = []
#         for x in veh_id:
#             veh_list.append(traci.vehicle.getSpeed(x))
#         print( sum(veh_list)/len(veh_list) )

