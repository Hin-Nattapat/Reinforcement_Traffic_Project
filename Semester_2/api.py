import traci
import pandas
import random

class API():
    def __init__(self):
        self.edge = ['gneE8', 'gneE10', 'gneE12', 'gneE14']
        self.lane = [['gneE8_0', 'gneE8_1'], ['gneE10_0', 'gneE10_1'], 
                    ['gneE12_0', 'gneE12_1'], ['gneE14_0', 'gneE14_1']]
        #self.acc_waiting_time = []
        self.oldId = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
        self.carPass = [0, 0, 0, 0]
        self.length = 489.6

    def get_avg_speed(self):
        avg_spd = []
        for edge in self.edge:
            if traci.edge.getLastStepVehicleNumber(edge) > 0:
                avg_spd.append(traci.edge.getLastStepMeanSpeed(edge))
            else:
                avg_spd.append(0)
        
        return avg_spd

    def get_flow_rate(self):
        flow_rate = []
        for edge in range(0, 4):
            for lane in range(0, 2):
                num = traci.inductionloop.getLastStepVehicleNumber('e1_'+self.lane[edge][lane])
                curID = traci.inductionloop.getLastStepVehicleIDs('e1_'+self.lane[edge][lane])
                if num > 0 and curID != self.oldId[edge][lane]:
                    self.oldId[edge][lane] = curID
                    self.carPass[edge] += 1
            flow_rate.append(self.carPass[edge] / traci.simulation.getCurrentTime() * 1000 * 3600)        
        
        return flow_rate

    def get_density(self):
        dens = []
        for edge in self.edge:
            num = traci.edge.getLastStepVehicleNumber(edge)
            dens.append(num*1000 / self.length)

        return dens

    def get_waiting_time(self):
        w_time = []
        for edge in self.edge:
            total_time = 0
            vehs = traci.edge.getLastStepVehicleIDs(edge)
            if len(vehs > 0):
                for vid in vehs:
                    total_time += traci.vehicle.getAccumulatedWaitingTime(vid)
                w_time.append(total_time / len(vehs))
            else:
                w_time.append(0)
        return w_time

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
  
def set_Trafficlight(state,duration):
    TrafficLightPhases = []
    TrafficLightPhases.append(
        traci.trafficlight.Phase(0, "rrrrrrrrrrrrrrrr", 0, 0))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(duration, state[0], duration, duration))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(3, state[1], 3, 3))
    Trafficlogic = traci.trafficlight.Logic("0", 0, 0, TrafficLightPhases)
    traci.trafficlight.setProgramLogic('TFL_C', Trafficlogic)

def checkNextLane(lane):
    # test = traci.lane.getLastStepVehicleNumber("InB_S_2_1")
    laneObject = [0,0,0,0,0,0]
    for i in range(len(lane)):
        laneObject[i] = traci.lane.getLastStepVehicleNumber(lane[i])
    MaxValue = max(laneObject)
    Index = laneObject.index(MaxValue) 
    print("---------------- Checker ----------------")
    print("Candidate : ",lane)
    print("CountVahicle : ",laneObject)
    print("NextLane : ",lane[Index])
    print("-----------------------------------------")
    return lane[Index]

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
        setFlow_Rate(i,8,8,8,8)
    elif epochs <= 40:
        setFlow_Rate(i,8,4,8,8)
    elif epochs <= 60:
        setFlow_Rate(i,4,16,8,8)
    elif epochs <= 80:
        setFlow_Rate(i,16,8,8,4)
    elif epochs <= 100:
        setFlow_Rate(i,8,8,4,16)    
    