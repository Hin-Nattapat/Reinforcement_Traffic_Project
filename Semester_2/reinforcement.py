import os
import sys
import optparse
import random
import traci
import api

EXPLORE_RATE = 0.2
LEARNING_RATE = 0.5
DISCOUNT_RATE = 0.9
MAX_ACTION = 6
num_episodes = 5


class TrafficLight:
    def __init__(self, state, lane):
        self.state = state
        self.lane = lane
        self.totalState = ["S1","S2","S3","S4","S5","S6","S7","S8"]
        self.Nextlane = []
        self.stateTransition = {
            "S1":{
                "Index": 0, 
                "State": "S1",
                "Lane": "InB_S_2_0",
                # "ActionNumber": {"A1" : [3,4,5,6,7,8],"A2" : [2,3,4,6,7,8]},
                "Action": {"A1" : ["S3","S4","S5","S6","S7","S8"],"A2" : ["S2","S3","S4","S6","S7","S8"]}     
            },
            "S2":{
                "Index": 1, 
                "State": "S2",
                "Lane": "InB_S_2_1",
                "ActionNumber": {"A1" : [3,4,5,6,7,8],"A2" : [1,3,4,5,7,8]},
                "Action": {"A1" : ["S3","S4","S5","S6","S7","S8"],"A3" : ["S1","S3","S4","S5","S7","S8"]}
            },
            "S3":{
                "Index": 2, 
                "State": "S3",
                "Lane": "InB_E_2_0",
                "ActionNumber": {"A1" : [1,2,5,6,7,8],"A2" : [1,2,4,5,6,8]},
                "Action": {"A1" : ["S1","S2","S5","S6","S7","S8"],"A2" : ["S1","S2","S4","S5","S6","S8"]}
            },
            "S4":{
                "Index": 3, 
                "State": "S4",
                "Lane": "InB_E_2_1",
                "ActionNumber": {"A1" : [1,2,5,6,7,8],"A2" : [1,2,3,5,6,7]},
                "Action": {"A1" : ["S1","S2","S5","S6","S7","S8"],"A3" : ["S1","S2","S3","S5","S6","S7"]}
            },
            "S5":{
                "Index": 4, 
                "State": "S5",
                "Lane": "InB_N_2_0",
                "ActionNumber": {"A1" : [1,2,3,4,7,8],"A2" : [2,3,4,6,7,8]},
                "Action": {"A1" : ["S1","S2","S3","S4","S7","S8"],"A2" : ["S2","S3","S4","S6","S7","S8"]}
            },
            "S6":{
                "Index": 5, 
                "State": "S6",
                "Lane": "InB_N_2_1",
                "ActionNumber": {"A1" : [1,2,3,4,7,8],"A2" :[1,3,4,5,7,8]},
                "Action": {"A1" : ["S1","S2","S3","S4","S7","S8"],"A3" : ["S1","S3","S4","S5","S7","S8"]}
            },
            "S7":{
                "Index": 6, 
                "State": "S7",
                "Lane": "InB_W_2_0",
                "ActionNumber": {"A1" : [1,2,3,4,5,6],"A2" :[1,2,4,5,6,8]},
                "Action": {"A1" : ["S1","S2","S3","S4","S5","S6"],"A2" : ["S1","S2","S4","S5","S6","S8"]}
            },
            "S8":{
                "Index": 7, 
                "State": "S8",
                "Lane": "InB_W_2_0",
                "ActionNumber": {"A1" : [1,2,3,4,5,6],"A2" :[1,2,3,5,6,7]},
                "Action": {"A1" : ["S1","S2","S3","S4","S5","S6"],"A3" : ["S1","S2","S3","S5","S6","S7"]}
            }
        }
        self.action = {
            "S1":{
                "LegalAction":["A1","A2"],
                "Action":{"A1":["GGrrrrrr","yyrrrrrr"],"A2":["GrrrGrrr","yrrryrrr"]}
            },
            "S2":{
                "LegalAction":["A1","A3"],
                "Action":{"A1":["GGrrrrrr","yyrrrrrr"],"A3":["rGrrrGrr","ryrrryrr"]}
            },
            "S3":{
                "LegalAction":["A1","A2"],
                "Action":{"A1":["rrGGrrrr","rryyrrrr"],"A2":["rrGrrrGr","rryrrryr"]}
            },
            "S4":{
                "LegalAction":["A1","A3"],
                "Action":{"A1":["rrGGrrrr","rryyrrrr"],"A3":["rrrGrrrG","rrryrrry"]}
            },
            "S5":{
                "LegalAction":["A1","A2"],
                "Action":{"A1":["rrrrGGrr","rrrryyrr"],"A2":["GrrrGrrr","yrrryrrr"]}
            },
            "S6":{
                "LegalAction":["A1","A3"],
                "Action":{"A1":["rrrrGGrr","rrrryyrr"],"A3":["rGrrrGrr","ryrrryrr"]}
            },
            "S7":{
                "LegalAction":["A1","A2"],
                "Action":{"A1":["rrrrrrGG","rrrrrryy"],"A2":["rrGrrrGr","rryrrryr"]}
            },
            "S8":{
                "LegalAction":["A1","A3"],
                "Action":{"A1":["rrrrrrGG","rrrrrryy"],"A3":["rrrGrrrG","rrryrrry"]}
            },
        }

        self.stateSpace = []

        # self.reward = 0.0
        # self.stateSpace = []
        # self.complete = False
        # self.action = 0


    def StateTransition(self):
        #วิธ๊ใช้ self.stateTransition ตามด้วย Array[] ของ State เรียกหา Dict ของ State นั้นๆ
        #Search หาข้อมูลต่อด้วย key State Action 
        #ตัวอย่างหา nextState ของ state8 action2 ==>> self.stateTransition[7]["Action"]["A2"]
        print("state ->",self.stateTransition)

    def takeAction(self,action):
        #วิธ๊ใช้ self.action ตามด้วย Array[] ของ State - 1 เรียกหา Dict ของ action ณ State นั้นๆ
        #Search หาข้อมูลต่อด้วย key Action 
        #ตัวอย่างหา action A3 ของ state8 ==>> self.action[7]["Action"]["A3"]
        # print("action ->",self.action[7]["Action"]["A3"])
        # return self.action[self.state]["Action"][action]

    def InitStateSpace(self,countState):
        #สร้าง Table เก็บค่าของ Q-value เอาไว้
        for i in range(0,countState):
            self.stateSpace.append({"Q-Value":[0.0,0.0],"Q-Max":0.0,"Q-Sum":i})
        print(self.stateSpace[5]["Q-Sum"])

    def getTrafficState(self,currentState,action):
        return self.stateTransition[currentState]["Action"][action]
        
    def randomAction(self):
        index = random.randrange(0, 2)
        print(self.action[self.state]["LegalAction"][index])
        return self.action[self.state]["LegalAction"][index]

    def changeState(self,NextLane):
        for i in self.totalState:
            if NextLane == self.stateTransition[i]["Lane"]:
                self.state = self.stateTransition[i]["State"]
        print("CurrentState => ",self.state)

    def fineCandidateLane(self,action):
        nextState = self.stateTransition["S1"]["Action"][action]
        for i in nextState:
            self.Nextlane.append(self.stateTransition[i]["Lane"])
        print(nextState)
        print(self.Nextlane)
        return self.Nextlane





















    def LegalAction(self, action, inputState):
        State = inputState.copy()
        
        if action == 0:
            State = [State[0]+15, State[1], State[2]]
        elif action == 1:
            State = [State[0]-15, State[1], State[2]]
        elif action == 2:
            State = [State[0], State[1]+15, State[2]]
        elif action == 3:
            State = [State[0], State[1]-15, State[2]]
        elif action == 4:
            State = [State[0], State[1], State[2]+15]
        else:
            State = [State[0], State[1], State[2]-15]

        if (State[0] == 0 or State[1] == 0 or State[2] == 0):
            return False
        elif sum(State) > 105:
            return False
        else:
            return True

    
    # def get_nextState(self, action, State):
    #     state = self.takeAction(action, State)
    #     return state

    def get_state(self, inputState):
        tempState = []
        for i in range(len(self.stateSpace)):
            if self.stateSpace[i]["state"] == inputState:
                tempState = self.stateSpace[i]
                break
        return tempState

    

    # def InitStateSpace(self):
    #     State = [15,15,15]
    #     self.stateSpace.append({"state": [State[0], State[1], State[2]], "Q_value": [
    #                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "Q_MAX": 0.0, "Q_SUM": 0.0})
    #     while State != [75, 75, 75]:
    #         State[2] += 15
    #         if State[2] == 90:
    #             State[2] = 15
    #             State[1] += 15
    #             if State[1] == 90:
    #                 State[1] = 15
    #                 State[0] += 15
    #         if sum(State) <= 105:
    #             self.stateSpace.append({"state": [State[0], State[1], State[2]], "Q_value": [
    #                                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "Q_MAX": 0.0, "Q_SUM": 0.0})
    #     print(self.stateSpace)
    #     # return print(self.stateSpace)

    def Find_Q_Max(self):
        for i in range(len(self.stateSpace)):
            Q_MAX = max(self.stateSpace[i]['Q_value'])
            self.stateSpace[i]["Q_MAX"] = Q_MAX

    def Find_Q_Sum(self):
        for i in range(len(self.stateSpace)):
            tempState = self.stateSpace[i]['state'].copy()
            Q_SUM = 0.0
            for j in range(MAX_ACTION):
                if self.LegalAction(j, tempState):
                    # print("state : ", tempState,"Q_value : ", self.stateSpace[i]['Q_value'][j])
                    Q_SUM += self.stateSpace[i]['Q_value'][j]
                    self.stateSpace[i]['Q_SUM'] = Q_SUM
        # return print(self.stateSpace)

    def Find_avg_Q(self):
        count_Q = 0
        Q_sum_all = 0
        for item in self.stateSpace:
            if item['Q_SUM'] != 0:
                Q_sum_all += item['Q_SUM']
            count_Q += 1
        avg_Q = Q_sum_all / count_Q
        if count_Q == 0:
            return 0
        return avg_Q         


    def Greedy_Al(self):
        self.Find_Q_Max()
        State = self.get_state(self.state)
        for i in range(MAX_ACTION):
            if State["Q_value"][i] == State["Q_MAX"]:
                self.action = i
        return self.action

    def E_Greedy_Al(self):
        randomNumber = random.uniform(0, 1)
        State = self.get_state(self.state)
        if ((EXPLORE_RATE > randomNumber) or (State["Q_SUM"] == 0.0)):
            self.action = self.randomAction()
            return self.action
        else:
            for i in range(MAX_ACTION):
                if State["Q_value"][i] == State["Q_MAX"]:
                    self.action = i
            return self.action

    def P_Greedy_Al(self):
        randomNumber = random.uniform(0, 1)
        randomProb = random.uniform(0, 1)
        presentState = self.get_state(self.state)
        if ((EXPLORE_RATE > randomNumber) or (presentState["Q_SUM"] == 0.0)):
            # print("EXPLORE", EXPLORE_RATE, randomNumber)
            self.action = self.randomAction()
            return self.action
        else:
            action = self.randomAction()
            for i in range(MAX_ACTION):
                if self.LegalAction(action, self.state):
                    
                    prob = (presentState["Q_value"]
                            [action] / presentState["Q_SUM"])
                    if prob > randomProb:
                        self.action = action
                        return self.action
                action = action + 1
                if action == MAX_ACTION:
                    action = 0
            if (i == MAX_ACTION-1):
                self.action = self.randomAction()
                return self.action
               
    def updateFuction_fixed(self):
        state = [30,30,30]
        api.get_waiting_time(self.lane,state)

    def updateFuction(self, waiting_time):
        newState = self.takeAction(self.action, self.state)
        presentState = self.get_state(self.state)
        nextState = self.get_state(newState)
        #continue simulate
        # api.set_Trafficlight(newState)
        rewardResult = waiting_time
        if rewardResult != 0:
            self.reward = (1/rewardResult) * 100
        else: self.reward = 0
        
        self.Find_Q_Max()
        presentState["Q_value"][self.action] += (LEARNING_RATE * (
            self.reward+(DISCOUNT_RATE*nextState["Q_MAX"])-presentState["Q_value"][self.action]))
        for i in range(len(self.stateSpace)):
            if self.stateSpace[i]["state"] == presentState['state']:
                self.stateSpace[i]["Q_value"][self.action] = presentState["Q_value"][self.action]
        self.Find_Q_Sum()
        api.csv_data_stateSpace(self.stateSpace)

    def updateState(self):
        oldState = self.state.copy()
        self.state = self.takeAction(self.action, self.state)
        print("Present_STATE :",oldState,"Next_STATE :",self.state,"ACTION :",self.action,"Reward :",self.reward)
        return self.state
        