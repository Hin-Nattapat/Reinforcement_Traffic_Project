import traci

class API():
    def __init__(self):
        self.wait_time = []
        self.avg_spd = []
        self.dens = []
        self.flow = []
        self.keep = True
        self.keep_2 = True
        self.keep_3 = True
        self.lane = [['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
            ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
        self.edge = ['gneE3','gneE13','gneE11','gneE7']
        self.result = {
            "w_time" : None,
            "dens" : None,
            "avg_spd" : None,
            "f_rate" : None
        }

    
    def get_obj(self, nextState):
        self.wait_time = [0.0, 0.0, 0.0, 0.0]
        self.avg_spd = [0.0, 0.0, 0.0, 0.0]
        self.dens = [0.0, 0.0, 0.0, 0.0]
        self.keep = True
        traci.simulationStep()
        self.set_Trafficlight(nextState)
        while traci.simulation.getTime() % 132 != 0:
            phase = traci.trafficlight.getPhase('gneJ7')
            #self.get_waiting_time(phase)
            #self.get_avg_spd(phase)
            self.avg_spd.append(self.get_avg_spd())
            self.dens.append(self.get_dens())
            traci.simulationStep()

        #collect all result
        #self.result['w_time'] = sum(self.wait_time) / len(self.wait_time)
        self.result['avg_spd'] = sum(self.avg_spd) / len(self.avg_spd)
        self.result['dens'] = sum(self.dens) / len(self.dens)
        #self.result['f_rate'] = s
        return self.result

    def get_waiting_time(self, phase):        
        if phase % 2 == 1 and self.keep:
            print('phase : ' ,phase)
            temp = (traci.lane.getWaitingTime(
                self.lane[int((phase-1)/2)][0]) + traci.lane.getWaitingTime(self.lane[int((phase-1)/2)][1])) / 2.0           
            self.wait_time[int((phase-1)/2)] = temp
            print(self.wait_time)
            self.keep = False
        elif phase % 2 == 0:
            self.keep = True
    
    def get_avg_spd(self): #complete
        spd = []
        veh_id = traci.vehicle.getIDList()
        for i in veh_id:
            spd.append(traci.vehicle.getSpeed(i))
        return sum(spd) / len(spd)
    
    def get_dens(self): #complete
        amount = 0
        for i in range(0,4):
            amount += traci.edge.getLastStepVehicleNumber(self.edge[i])

        return 1000 * amount / ( traci.lane.getLength(self.lane[0][0]) * 4 )

    def get_flow(self):
        


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

