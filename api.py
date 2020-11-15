import traci
import pandas
import random

class API():
    def __init__(self):
        self.wait_time = []
        self.avg_spd = []
        self.dens = None
        self.flow = 0
        self.pre_id = [set(), set(), set(), set()]
        self.cur_id= [set(), set(), set(), set()]
        self.keep = True
        self.keep_2 = True
        self.lane = [['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
            ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
        self.edge = ['gneE3','gneE13','gneE11','gneE7']
        self.result = {
            "w_time" : None,
            "dens" : None,
            "avg_spd" : None,
            "f_rate" : None
        }

    def get_obj(self, nextState, epochs):
        self.wait_time = [0.0, 0.0, 0.0, 0.0]
        self.avg_spd = [0.0, 0.0, 0.0, 0.0]
        self.dens = [0.0, 0.0, 0.0, 0.0]
        self.flow = 0
        self.keep = True

        self.set_Trafficlight(nextState)
        ctime = traci.simulation.getTime()
        print(ctime)
        
        while traci.simulation.getTime() - ctime < 132:
            random_Vehicle(epochs)
            traci.simulationStep()
            phase = traci.trafficlight.getPhase('gneJ7')
            self.get_waiting(phase)
            self.get_flow(phase)
            self.avg_spd.append(self.get_avg_spd())
            self.dens.append(self.get_dens())
            #print(traci.trafficlight.getNextSwitch('gneJ7'))
            #print(traci.trafficlight.getPhaseDuration('gneJ7'))
        # print('previous : ' ,self.pre_id , "SUM",len(list(self.pre_id)))
        # print('current : ' ,self.cur_id)
        for i in self.pre_id:
            index = self.pre_id.index(i)
            duplicate = (list(self.pre_id[index].intersection(self.cur_id[index])))
            self.flow += (len(list(self.pre_id[index])) - len(duplicate))

        # print("FLOW RATE",self.flow)

        #collect all result
        self.result['w_time'] = sum(self.wait_time) / len(self.wait_time)
        self.result['avg_spd'] = sum(self.avg_spd) / len(self.avg_spd)
        self.result['dens'] = sum(self.dens) / len(self.dens)
        self.result['f_rate'] = self.flow
    
        return self.result

    def get_waiting(self, phase):        
        if phase % 2 == 1 and self.keep:
            #print('phase : ' ,phase)
            temp = (traci.lane.getWaitingTime(self.lane[int((phase-1)/2)][0]) 
                    + traci.lane.getWaitingTime(self.lane[int((phase-1)/2)][1])) / 2.0           
            self.wait_time[int((phase-1)/2)] = temp
            # print(self.wait_time)
            #print(temp)
            self.keep = False
        elif phase % 2 == 0:
            self.keep = True

    def waiting(self):
        for edge in self.edge:
            print('edge :' ,end=' ')
            print()
    
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

    def get_flow(self, phase): #complete
        if phase % 2 and self.keep_2:
            self.pre_id[int((phase-1)/2)] = set(traci.edge.getLastStepVehicleIDs(self.edge[int((phase-1)/2)]))
            self.keep_2 = False
        elif phase % 2 == 0 and phase > 0 :
            self.cur_id[int((phase-1)/2)] = set(traci.edge.getLastStepVehicleIDs(self.edge[int((phase-1)/2)]))
            self.keep_2 = True

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

def get_waiting_time(lane, NextState):
    wait_time = [0.0, 0.0, 0.0, 0.0]
    keep = True
    count = 0
    # print("TEST : "," : ",traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
    print(NextState)
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
    traci.route.add("rou_W1", ["gneE43", "gneE3", "gneE6", "gneE40"])
    traci.route.add("rou_W2", ["gneE43", "gneE3", "gneE12", "gneE32"])
    traci.route.add("rou_W3", ["gneE43", "gneE3", "gneE10", "gneE34"])

    traci.route.add("rou_E1", ["gneE33", "gneE13", "gneE8", "gneE42"])
    traci.route.add("rou_E2", ["gneE33", "gneE13", "gneE6", "gneE40"])
    traci.route.add("rou_E3", ["gneE33", "gneE13", "gneE10", "gneE34"])

    traci.route.add("rou_N1", ["gneE41", "gneE7", "gneE8", "gneE42"])
    traci.route.add("rou_N2", ["gneE41", "gneE7", "gneE12", "gneE32"])
    traci.route.add("rou_N3", ["gneE41", "gneE7", "gneE10", "gneE34"])

    traci.route.add("rou_S1", ["gneE35", "gneE11", "gneE8", "gneE42"])
    traci.route.add("rou_S2", ["gneE35", "gneE11", "gneE6", "gneE40"])
    traci.route.add("rou_S3", ["gneE35", "gneE11", "gneE12", "gneE32"])

    
    
    # traci.route.add("rou_13", ["gneE43", "gneE3", "gneE6", "gneE7", "gneE12", "gneE32"])
    # traci.route.add("rou_14", ["gneE43", "gneE3", "gneE12", "gneE13", "gneE6", "gneE40"])
    # traci.route.add("rou_15", ["gneE43", "gneE3", "gneE10", "gneE11", "gneE8", "gneE42"])

    # traci.route.add("rou_11", ["gneE43", "gneE3", "gneE6", "gneE7", "gneE10", "gneE34"])
    # traci.route.add("rou_12", ["gneE43", "gneE3", "gneE6", "gneE7", "gneE8", "gneE42"])
    # traci.route.add("rou_14", ["gneE43", "gneE3", "gneE12", "gneE13", "gneE10", "gneE34"])
    # traci.route.add("rou_15", ["gneE43", "gneE3", "gneE12", "gneE13", "gneE8", "gneE42"])
    # traci.route.add("rou_16", ["gneE43", "gneE3", "gneE10", "gneE11", "gneE12", "gneE32"])
    # traci.route.add("rou_17", ["gneE43", "gneE3", "gneE10", "gneE11", "gneE6", "gneE40"])

    # traci.route.add("rou_16", ["gneE41", "gneE7", "gneE8", "gneE3", "gneE12", "gneE32"])
    # traci.route.add("rou_17", ["gneE41", "gneE7", "gneE12", "gneE13", "gneE6", "gneE40"])
    # traci.route.add("rou_18", ["gneE41", "gneE7", "gneE10", "gneE11", "gneE8", "gneE42"])
    # traci.route.add("rou_19", ["gneE41", "gneE7", "gneE8", "gneE3", "gneE12", "gneE32"])
    # traci.route.add("rou_20", ["gneE41", "gneE7", "gneE8", "gneE3", "gneE10", "gneE34"])
    # traci.route.add("rou_21", ["gneE41", "gneE7", "gneE8", "gneE3", "gneE6", "gneE40"])
    # traci.route.add("rou_22", ["gneE41", "gneE7", "gneE12", "gneE13", "gneE6", "gneE40"])
    # traci.route.add("rou_23", ["gneE41", "gneE7", "gneE12", "gneE13", "gneE10", "gneE34"])
    # traci.route.add("rou_24", ["gneE41", "gneE7", "gneE12", "gneE13", "gneE8", "gneE42"])
    # traci.route.add("rou_25", ["gneE41", "gneE7", "gneE10", "gneE11", "gneE12", "gneE32"])
    # traci.route.add("rou_26", ["gneE41", "gneE7", "gneE10", "gneE11", "gneE6", "gneE40"])
    # traci.route.add("rou_27", ["gneE41", "gneE7", "gneE10", "gneE11", "gneE8", "gneE42"])

    # traci.route.add("rou_19", ["gneE33", "gneE13", "gneE8", "gneE3", "gneE12", "gneE32"])
    # traci.route.add("rou_20", ["gneE33", "gneE13", "gneE6", "gneE7", "gneE12", "gneE32"])
    # traci.route.add("rou_21", ["gneE33", "gneE13", "gneE10", "gneE11", "gneE6", "gneE40"])
    # traci.route.add("rou_29", ["gneE33", "gneE13", "gneE8", "gneE3", "gneE10", "gneE34"])
    # traci.route.add("rou_30", ["gneE33", "gneE13", "gneE8", "gneE3", "gneE6", "gneE40"])
    # traci.route.add("rou_32", ["gneE33", "gneE13", "gneE6", "gneE7", "gneE10", "gneE34"])
    # traci.route.add("rou_33", ["gneE33", "gneE13", "gneE6", "gneE7", "gneE8", "gneE42"])
    # traci.route.add("rou_34", ["gneE33", "gneE13", "gneE10", "gneE11", "gneE12", "gneE32"])
    # traci.route.add("rou_36", ["gneE33", "gneE13", "gneE10", "gneE11", "gneE8", "gneE42"])

    # traci.route.add("rou_22", ["gneE35", "gneE11", "gneE8", "gneE3", "gneE10", "gneE34"])
    # traci.route.add("rou_23", ["gneE35", "gneE11", "gneE6", "gneE7", "gneE10", "gneE34"])
    # traci.route.add("rou_24", ["gneE35", "gneE11", "gneE12", "gneE13", "gneE6", "gneE40"])
    # traci.route.add("rou_37", ["gneE35", "gneE11", "gneE8", "gneE3", "gneE12", "gneE32"])
    # traci.route.add("rou_39", ["gneE35", "gneE11", "gneE8", "gneE3", "gneE6", "gneE40"])
    # traci.route.add("rou_40", ["gneE35", "gneE11", "gneE6", "gneE7", "gneE12", "gneE32"])
    # traci.route.add("rou_42", ["gneE35", "gneE11", "gneE6", "gneE7", "gneE8", "gneE42"])
    # traci.route.add("rou_43", ["gneE35", "gneE11", "gneE12", "gneE13", "gneE10", "gneE34"])
    # traci.route.add("rou_45", ["gneE35", "gneE11", "gneE12", "gneE13", "gneE8", "gneE42"])



def setFlow_Rate(i,w,e,n,s):
    RouteID = traci.route.getIDList()
    count = traci.route.getIDCount()
    if i % w == 0 :
        index = random.randint(9, 11)
        traci.vehicle.add("vehicle_"+str(i)+"w",RouteID[index], departSpeed="random")
    if i % e == 0 : 
        index = random.randint(0, 2)
        traci.vehicle.add("vehicle_"+str(i)+"e",RouteID[index], departSpeed="random")
    if i % n == 0 : 
        index = random.randint(3, 5)
        traci.vehicle.add("vehicle_"+str(i)+"n",RouteID[index], departSpeed="random")
    if i % s == 0 :
        index = random.randint(6, 8)
        traci.vehicle.add("vehicle_"+str(i)+"s",RouteID[index], departSpeed="random")


def random_Vehicle(epochs):
    i = traci.simulation.getTime()
    if epochs <= 20:
        setFlow_Rate(i,4,8,4,8)
    elif epochs <= 40:
        setFlow_Rate(i,4,2,8,4)
    elif epochs <= 60:
        setFlow_Rate(i,8,4,4,2)
    elif epochs <= 80:
        setFlow_Rate(i,2,8,2,8)
           

