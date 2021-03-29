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
        self.getDuration = 10
        
    def simulate(self):
        #flowrate,speed,density,waiting,arrivalRate,queuelength,sdLength
        self.addCarOut()
        self.addCarIn()
        result = {}
        avgData = [[],[],[],[],[],[]]
        if traci.simulation.getTime() % self.getDuration == 0:
            juncIndex = 0
            for junc, edge in self.edge.items():
                result[junc] = {}
                flowRate = round((self.carOut[juncIndex] * 3600 / traci.simulation.getTime()), 2)
                arrRate = round((self.carIn[juncIndex] * 3600 / traci.simulation.getTime()), 2)
                length = self.getAvgLength(edge)
                speed = self.get_avg_speed(edge)
                density = self.get_density(edge)
                waiting = self.getWaitingTime(edge)
                result[junc]["flowRate"] = flowRate
                result[junc]["speed"] = speed
                result[junc]["density"] = density
                result[junc]["waitingTime"] = waiting
                result[junc]["arrivalRate"] = arrRate
                result[junc]["qLength"] = length[0]
                result[junc]["qStd"] = length[1]
                avgData[1].append(flowRate)
                avgData[2].append(speed)
                avgData[3].append(density)
                avgData[4].append(waiting)
                avgData[5].append(length[0])
                juncIndex += 1
                
        traci.simulationStep()
        if len(result) > 0:
            avgData[0] = traci.simulation.getTime()
            avgData[1] = round(sum(avgData[1]) / len(avgData[1]), 2)
            avgData[2] = round(sum(avgData[2]) / len(avgData[2]), 2)
            avgData[3] = round(sum(avgData[3]) / len(avgData[3]), 2)
            avgData[4] = round(sum(avgData[4]) / len(avgData[4]), 2)
            avgData[5] = round(sum(avgData[5]) / len(avgData[5]), 2)
            return result, avgData
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
            lengthList.append(traci.lane.getLastStepHaltingNumber(edge+'_1') * 6.0)
            lengthList.append(traci.lane.getLastStepHaltingNumber(edge+'_0') * 6.0)
        avg_length = sum(lengthList) / len(lengthList)
        std_length = st.stdev(lengthList)
        return avg_length, round(std_length, 2)

    def getLastLength(self, juncID):
        edgeID = self.edge[juncID]
        length = []
        for edge in edgeID:
            length.append(traci.lane.getLastStepHaltingNumber(edge+'_1') * 6.0)
            length.append(traci.lane.getLastStepHaltingNumber(edge+'_0') * 6.0)
        return length
    
    def getLastWaiting(self, juncID):
        edgeID = self.edge[juncID]
        wait = []
        for edge in edgeID:
            wait.append(traci.lane.getWaitingTime(edge+'_1'))
            wait.append(traci.lane.getWaitingTime(edge+'_0'))
        return wait

class TLScontrol():
    def __init__(self, tlsID, edgeID, nextLane):
        self.id = tlsID
        self.cycle = 0
        self.time = 0
        self.lane = []
        self.nextLane = nextLane
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
        return 'hi'

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
    
    def getMoveLane(self):
        lane = []
        for i in self.moveState:
            lane.append(self.lane[i])
        return lane
    
    def getNextLane(self):
        lane = []
        for i in self.moveState:
            lane.append(self.nextLane[i])
        return lane

