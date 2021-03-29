import random
import math
import statistics as st
import csv_api as CSV
import traci

class Reinforcement():
    def __init__(self, maxState, numJunc, avg_speed, avg_density, max_waiting_time):
        self.EXPLORE_RATE = 0.5
        self.LEARNING_RATE = 0.1
        self.DISCOUNT_RATE = 0.9
        self.MAX_ACTIONS = 3
        self.TAU = 0.8
        self.DELTA = 0.5
        self.EPOCH = 1
        self.TYPE = 'SRL'
        self.stateSpace = {}
        self.count = 0
        self.numJunc = numJunc
        self.reward = []
        self.greenTime = []
        #####################################
        self.AVG_SPD = avg_speed
        self.DENSITY = avg_density
        self.MAX_WAITING_TIME = max_waiting_time
        #####################################
        for i in range(maxState):
            temp = {
                "qValue" : [0.0]*self.MAX_ACTIONS,
                "sumQ" : 0.0,
                "maxQ" : 0.0
            }
            self.stateSpace[i] = temp

    def printStateSpace(self):
        print(self.stateSpace)

    def getStateSpace(self):
        return self.stateSpace

    def getEpoch(self):
        return self.EPOCH

    def setMaxQ(self):
        for i in range(len(self.stateSpace)):
            maxQ = max(self.stateSpace[i]["qValue"])
            self.stateSpace[i]["maxQ"] = maxQ
    
    def setSumQ(self):
        for i in range(len(self.stateSpace)):
            sumQ = sum(self.stateSpace[i]["qValue"])
            self.stateSpace[i]["sumQ"] = sumQ

    def getAvgQ(self):
        total_sumQ = 0
        for i in range(len(self.stateSpace)):
            total_sumQ += sum(self.stateSpace[i]["qValue"])
        avg_sumQ = total_sumQ / (len(self.stateSpace) * (self.MAX_ACTIONS - 1))
        return avg_sumQ

    def getAction(self, policy, currentState):
        action = None
        if policy == "p_greedy":
            action = self.pGreedy(currentState)
        if policy == "e_greedy":
            action = self.eGreedy(currentState)
        return action

    def eGreedy(self, currentState):
        action = 0
        stateData = self.stateSpace[currentState]
        if (self.EXPLORE_RATE > random.uniform(0, 1)) or (stateData["sumQ"] == 0.0):
            #explore
            print('explore' ,end=' | ')
            action = self.randomAction(currentState)
        else:
            #exploit
            print('exploit' ,end=' | ')
            for count in range(self.MAX_ACTIONS):
                if self.actionVerify(currentState, count):
                    if (stateData["qValue"][count] == stateData["maxQ"]):
                        action = count
        return action

    def pGreedy(self, currentState):
        action = 0
        stateData = self.stateSpace[currentState]
        if (self.EXPLORE_RATE > random.uniform(0, 1)) or (stateData["sumQ"] == 0.0):
            #explore
            print('explore' ,end=' | ')
            action = self.randomAction(currentState)
        else:
            #exploit
            print('exploit' ,end=' | ')
            action = self.randomAction(currentState)
            for count in range(self.MAX_ACTIONS):
                if self.actionVerify(currentState, action):
                    prob = (stateData["qValue"][action]) / stateData["sumQ"]
                    if prob > random.uniform(0, 1):
                        return action
                action += 1
                if action == self.MAX_ACTIONS:
                    action = 0
            if count == self.MAX_ACTIONS:
                action = self.randomAction(currentState)
        return action
    
    def randomAction(self, state): #complete
        action = random.randint(0,2)
        while not(self.actionVerify(state, action)):
            action = random.randint(0,2)       
        return action

    def actionVerify(self, state, action): #complete
        if state % 2 == 0 and action in [0, 2]:
            return True
        elif state % 2 == 1 and action in [0, 1]:
            return True
        return False
    
    def takeAction(self, action, currentState):
        green_state = [currentState] #which state can go?
        phase = [[''],[''],0]
        
        if action == 0:
            green_state.append(currentState + (-2 * (currentState % 2)) + 1)
        else:
            green_state.append((currentState + 4) % 8)
        
        g_phase = ''
        y_phase = ''
        for i in [7,6,5,4,3,2,1,0]:
            if i in green_state:
                g_phase += 'G' * (1 + (i % 2))
                y_phase += 'y' * (1 + (i % 2))
            else:
                g_phase += 'r' * (1 + (i % 2))
                y_phase += 'r' * (1 + (i % 2))

        phase[0] = g_phase
        phase[1] = y_phase  
        
        return phase, green_state
    
    def getGreenTime(self, moveLane, nextLane):
        moveDens = []
        nextDens = []
        for i in range(len(moveDens)):
            moveDens.append(traci.lane.getLastStepVehicleNumber(moveLane[i])*0.4)
            nextDens.append(traci.lane.getLastStepVehicleNumber(nextLane[i])*0.4)
        
        if sum(moveDens)==0 or sum(nextDens)==0:
            self.greenTime.append(60)
            return 60
        greenTime = (sum(moveDens)/len(moveDens)) / (sum(nextDens)/len(nextDens)) * 60
        self.greenTime.append(greenTime)
        return greenTime

    def getNextState(self, qLength, moveState, waitingTime):
        maxWT = max(waitingTime)
        index = waitingTime.index(maxWT)
        val = maxWT / (qLength[index] / 6)
        print(val)
        if val > 300:
            return index

        length = qLength
        maxLength = max(length)
        nextState = length.index(maxLength)
        while nextState in moveState:
            length[nextState] = -1
            maxLength = max(length)
            nextState = length.index(maxLength)
        print(nextState)
        return nextState
    
    def getRandomState(self, moveState):
        nextState = random.randint(0, 7)
        while nextState in moveState:
            nextState = random.randint(0, 7)
        return nextState

    def update(self, currentState, nextState, action, data):
        reward = self.getSrlReward(data)
        self.reward.append(reward)
        self.setMaxQ()
        currentData = self.stateSpace[currentState]
        nextData = self.stateSpace[nextState]

        currentData["qValue"][action] += round((self.LEARNING_RATE * (reward + (self.DISCOUNT_RATE * nextData["maxQ"])) - currentData["qValue"][action]), 5)
        self.stateSpace[currentState] = currentData
        self.setSumQ()
        self.count += 1
        if self.count == self.numJunc:
            self.EPOCH += 1
            avgGreen = round(sum(self.greenTime) / len(self.greenTime), 2)
            avgRew = round(sum(self.reward) / len(self.reward), 2)
            self.reward = []
            self.greenTime = []
            self.count = 0
            return [self.EPOCH - 1, avgGreen, avgRew]
        return None

    def find_flowrate_expo(self,flowrate):
        # ต้องหา avg_spd,density นำข้อมูลมาจากกราฟของการทดลองแรก
        Saturate_Flowrate = self.AVG_SPD * self.DENSITY
        A3 = Saturate_Flowrate/2
        A2 = 2.944/(0.95-A3)
        flowrateExpo = A2*(flowrate-A3)
        return flowrateExpo

    def find_waitingtime_expo(self,waitingtime):
        A3 = self.MAX_WAITING_TIME/2
        A2 = 2.944/(0.95-A3)
        waitingtimeExpo = A2*(waitingtime-A3)
        return waitingtimeExpo

    def getSrlReward(self, data):
        FR = data['flowRate']
        WT = data['waitingTime']
        flowrateExpo = self.find_flowrate_expo(FR)
        waitingtimeExpo = self.find_waitingtime_expo(WT)
        FlowRateScale = 1/(1+math.exp(flowrateExpo))
        WaitingTimeScale = 1/(1+math.exp(waitingtimeExpo))
        reward = FlowRateScale/(1+WaitingTimeScale)
        return reward


     


       
    
