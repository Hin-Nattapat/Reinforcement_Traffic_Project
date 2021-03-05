import traci
import pandas
import matplotlib.pyplot as plt

class Simulation():
    def __init__(self, edge, laneId):
        self.edge = edge
        self.laneId = laneId
        self.passId = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
        self.arrId = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
        self.carOut = 0
        self.carIn = 0
        self.length = 489.6
        self.tls_id = ''
        self.dur = 3
        self.epoch = 0
        self.result_data = [['Time', 'Flow Rate', 'Speed', 'Density', 'Waiting Time', 'Arrival Rate']]

    def simulate(self, duration):
        result = [[],[],[],[],[],[]] #flowrate,speed,density,waiting,arrivalRate,queueLength
        time = 0
        while time < duration:
            traci.simulationStep()
            
            self.carOut += self.getCarOut()
            self.carIn += self.getCarIn()
            if (time+1) % self.dur == 0:
                update_result = [] #for update to csv
                systemTime = (self.epoch * duration) + (time + 1) #Time in System
                update_result.append(systemTime)
                flowRate = round((self.carOut * 3600 / traci.simulation.getTime()), 2)
                arrRate = round((self.carIn * 3600 / traci.simulation.getTime()), 2)
                result[0].append(flowRate)
                update_result.append(flowRate)
                result[1].append(self.get_avg_speed())
                update_result.append(self.get_avg_speed())
                result[2].append(self.get_density())
                update_result.append(self.get_density())
                result[3].append(self.getWaitingTime())
                update_result.append(self.getWaitingTime())
                result[4].append(arrRate)
                update_result.append(arrRate)
                self.result_data.append(update_result)
            result[5] = self.get_length(self.laneId)    
            time += 1

        self.epoch += 1
        self.csvResultData(self.result_data)
        return result

    def csvResultData(self,data):
        self.dataframe = pandas.DataFrame(data)
        self.dataframe.to_csv('result.csv', index=False,header=False, encoding='utf-8')

    def plotData(self):
        fig , ax = plt.subplots(2,3)
        ax[0,0].set_title("Flow Rate")
        ax[0,0].set_xlabel("Time")
        ax[0,0].set_ylabel("Flow Rate")
        ax[0,1].set_title("Speed")
        ax[0,1].set_xlabel("Time")
        ax[0,1].set_ylabel("Speed")
        ax[0,2].set_title("Density")
        ax[0,2].set_xlabel("Time")
        ax[0,2].set_ylabel("Density")
        ax[1,0].set_title("Waiting Time")
        ax[1,0].set_xlabel("Time")
        ax[1,0].set_ylabel("Waiting Time")
        ax[1,1].set_title("Arrival Rate")
        ax[1,1].set_xlabel("Time")
        ax[1,1].set_ylabel("Arrival Rate")
        #ax[1,2].set_title("Flow-Density model")
        #ax[1,2].set_xlabel("Density")
        #ax[1,2].set_ylabel("Flow Rate")
        dataframe = pandas.read_csv("result.csv")
        dataframe.plot(ax=ax[0,0],x="Time", y="Flow Rate")
        dataframe.plot(ax=ax[0,1],x="Time", y="Speed")
        dataframe.plot(ax=ax[0,2],x="Time", y="Density")
        dataframe.plot(ax=ax[1,0],x="Time", y="Waiting Time")
        dataframe.plot(ax=ax[1,1],x="Time", y="Arrival Rate")
        plt.show()

    def get_avg_speed(self): #complete
        avg_spd = 0
        for e_id in self.edge:
            if traci.edge.getLastStepVehicleNumber(e_id) > 0:
                avg_spd += traci.edge.getLastStepMeanSpeed(e_id)
        return round(((avg_spd / 4) * 3.6), 2)

    def getCarOut(self):
        numCar = 0
        for eId in self.edge:
            eIndex = self.edge.index(eId)
            for lane in range(0, 2):
                num = traci.inductionloop.getLastStepVehicleNumber('e1_' + eId + '_' + str(lane))
                curId = traci.inductionloop.getLastStepVehicleIDs('e1_' + eId + '_' + str(lane))
                if num > 0 and curId[0] != self.passId[eIndex][lane]:
                    self.passId[eIndex][lane] = curId[0]
                    numCar += 1
        
        return numCar

    def getCarIn(self):
        numCar = 0
        for eId in self.edge:
            eIndex = self.edge.index(eId)
            for lane in range(0, 2):
                num = traci.inductionloop.getLastStepVehicleNumber('a1_' + eId + '_' + str(lane))
                curId = traci.inductionloop.getLastStepVehicleIDs('a1_' + eId + '_' + str(lane))
                if num > 0 and curId[0] != self.arrId[eIndex][lane]:
                    self.arrId[eIndex][lane] = curId[0]
                    numCar += 1
        return numCar            

    def get_density(self): #complete
        density = 0
        for e_id in self.edge:
            density += traci.edge.getLastStepVehicleNumber(e_id)
        return round(((density / 4) * 1000 / self.length), 2)

    def getWaitingTime(self): #complete
        wTime = []
        for eId in self.edge:
            vehs = traci.edge.getLastStepVehicleIDs(eId)
            if len(vehs) > 0:
                for vId in vehs:
                    wait = traci.vehicle.getAccumulatedWaitingTime(vId)
                    if wait > 0:
                        wTime.append(wait)
        if len(wTime) > 0:
            return round((sum(wTime) / len(wTime)), 2)
        return 0
    
    def get_length(self, laneId): #queue length in m
        length = []
        for lane in laneId:
            length.append(traci.lane.getLastStepHaltingNumber(lane) * 6.0)
        return length

    def get_lastLength(self, laneID):
        length = {}
        for lane in laneID:
            length[lane] = traci.lane.getLastStepHaltingNumber(lane) * 6.0
        return length


class TLScontrol():
    def __init__(self, tls_id):
        self.id = tls_id

    def set_logic(self, phase):
        tlPhase = []
        tlPhase.append(traci.trafficlight.Phase(3, phase[1], 3, 3))
        tlPhase.append(traci.trafficlight.Phase(phase[2], phase[0], phase[2], phase[2]))
        
        logic = traci.trafficlight.Logic("0", 0, 0, tlPhase)
        traci.trafficlight.setProgramLogic(self.id, logic)

