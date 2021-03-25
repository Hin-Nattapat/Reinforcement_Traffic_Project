import traci
import pandas
import statistics as st

class Simulation():
    def __init__(self, edgeList):
        self.edge = edgeList
        self.numJunc = len(edgeList)
        self.passId = [[-1] *8] *self.numJunc
        self.arrId = [[-1] *8] *self.numJunc
        self.carOut = [0] *self.numJunc
        self.carIn = [0] *self.numJunc
        self.getDuration = 4
        
    def simulate(self):
        #flowrate,speed,density,waiting,arrivalRate,queuelength,sdLength
        self.addCarOut()
        self.addCarIn()
        result = {}
        if traci.simulation.getTime() % self.getDuration == 0:
            juncIndex = 0
            for junc, edge in self.edge.items():
                result[junc] = {}
                flowRate = round((self.carOut[juncIndex] * 3600 / traci.simulation.getTime()), 2)
                arrRate = round((self.carIn[juncIndex] * 3600 / traci.simulation.getTime()), 2)
                length = self.getAvgLength(edge)
                result[junc]["flowRate"] = flowRate
                result[junc]["speed"] = self.get_avg_speed(edge)
                result[junc]["density"] = self.get_density(edge)
                result[junc]["waitingTime"] = self.getWaitingTime(edge)
                result[junc]["arrivalRate"] = arrRate
                result[junc]["qLength"] = length[0]
                result[junc]["qStd"] = length[1]
                juncIndex += 1
                
        traci.simulationStep()
        if len(result) > 0:
            return result
        return None

    def addCarOut(self):
        juncIndex = 0
        for junc in self.edge.keys():
            for state in range(8):
                num = traci.inductionloop.getLastStepVehicleNumber('e1_' + junc + '_' + str(state))
                curId = traci.inductionloop.getLastStepVehicleIDs('e1_' + junc + '_' + str(state))
                if num > 0 and curId[0] != self.passId[juncIndex][state]:
                    self.passId[juncIndex][state] = curId[0]
                    self.carOut[juncIndex] += 1
            juncIndex += 1

    def addCarIn(self):
        juncIndex = 0
        for junc in self.edge.keys():
            for state in range(8):
                num = traci.inductionloop.getLastStepVehicleNumber('a1_' + junc + '_' + str(state))
                curId = traci.inductionloop.getLastStepVehicleIDs('a1_' + junc + '_' + str(state))
                if num > 0 and curId[0] != self.arrId[juncIndex][state]:
                    self.arrId[juncIndex][state] = curId[0]
                    self.carIn[juncIndex] += 1
            juncIndex += 1

    def get_avg_speed(self, edgeId): #complete
        avg_spd = 0
        for e_id in edgeId:
            if traci.edge.getLastStepVehicleNumber(e_id) > 0:
                avg_spd += traci.edge.getLastStepMeanSpeed(e_id)
        return round(((avg_spd / 4) * 3.6), 2)

    def get_density(self, edgeID): #complete
        density = 0
        for e_id in edgeID:
            density += traci.edge.getLastStepVehicleNumber(e_id) * 1000 / traci.lane.getLength(e_id + '_0')
        return round((density / 4), 2)

    def getWaitingTime(self, edgeID): #complete
        wTime = []
        for eId in edgeID:
            vehs = traci.edge.getLastStepVehicleIDs(eId)
            if len(vehs) > 0:
                for vId in vehs:
                    wait = traci.vehicle.getAccumulatedWaitingTime(vId)
                    if wait > 0:
                        wTime.append(wait)
        if len(wTime) > 0:
            return round((sum(wTime) / len(wTime)), 2)
        return 0

    def getAvgLength(self, edgeId): #queue length in m
        lengthList = []
        for edge in edgeId:
            lengthList.append(traci.lane.getLastStepHaltingNumber(edge+'_0') * 6.0)
            lengthList.append(traci.lane.getLastStepHaltingNumber(edge+'_1') * 6.0)
        avg_length = sum(lengthList) / len(lengthList)
        std_length = st.stdev(lengthList)
        return avg_length, std_length

    def getLastLength(self, juncID):
        edgeID = self.edge[juncID]
        length = []
        for edge in edgeID:
            length.append(traci.lane.getLastStepHaltingNumber(edge+'_0') * 6.0)
            length.append(traci.lane.getLastStepHaltingNumber(edge+'_1') * 6.0)
        
        return length

class TLScontrol():
    def __init__(self, tlsID, edgeID):
        self.id = tlsID
        self.cycle = 0
        self.time = 0
        self.lane = []
        self.currentState = 0
        self.moveState = []
        self.action = 0
        self.greenTime = 0
        self.result = {
            'flowRate' : [],
            'speed' : [],
            'density' : [],
            'waitingTime' : [],
            'arrivalRate' : [],
            'qLength' : [],
            'qStd' : []
        }
        
        for edge in edgeID:
            self.lane.append(edge + '_1')
            self.lane.append(edge + '_0')

    def __str__(self):
        return self.id

    def setLogic(self, phase):
        tlPhase = []
        tlPhase.append(traci.trafficlight.Phase(3, phase[1], 3, 3))
        tlPhase.append(traci.trafficlight.Phase(phase[2], phase[0], phase[2], phase[2]))
        logic = traci.trafficlight.Logic("0", 0, 0, tlPhase)
        traci.trafficlight.setProgramLogic(self.id, logic)
        self.cycle = phase[2] + 3

    def isCycleEnd(self):
        self.time += 1
        if self.cycle == self.time:
            self.time = 0
            return True
        return False

    def saveResult(self, data):
        self.result['flowRate'].append(data['flowRate'])
        self.result['speed'].append(data['speed'])
        self.result['density'].append(data['density'])
        self.result['waitingTime'].append(data['waitingTime'])
        self.result['arrivalRate'].append(data['arrivalRate'])
        self.result['qLength'].append(data['qLength'])
        self.result['qStd'].append(data['qStd'])
        #and write data to CSV

    def getAvgResult(self):
        avgResult = {
            'flowRate' : round(sum(self.result['flowRate']) / len(self.result['flowRate']), 2),
            'speed' : round(sum(self.result['speed']) / len(self.result['speed']), 2),
            'density' : round(sum(self.result['density']) / len(self.result['density']), 2),
            'waitingTime' : round(sum(self.result['waitingTime']) / len(self.result['waitingTime']), 2),
            'arrivalRate' : round(sum(self.result['arrivalRate']) / len(self.result['arrivalRate']), 2),
            'qLength' : round(sum(self.result['qLength']) / len(self.result['qLength']), 2),
            'qStd' : round(sum(self.result['qStd']) / len(self.result['qStd']), 2)
        }
        self.result = {
            'flowRate' : [],
            'speed' : [],
            'density' : [],
            'waitingTime' : [],
            'arrivalRate' : [],
            'qLength' : [],
            'qStd' : []
        }
        return avgResult

