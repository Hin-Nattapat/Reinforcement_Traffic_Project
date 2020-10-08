import traci

def get_waiting_time(lane):
    wait_time = [0.0, 0.0, 0.0, 0.0]
    keep = True
    count = 0
    while count < 4:
        phase = traci.trafficlight.getPhase('gneJ7')
        if phase % 2 == 0 and keep:
            temp = (traci.lane.getWaitingTime(
                lane[int(phase/2)][0]) + traci.lane.getWaitingTime(lane[int(phase/2)][1])) / 2
            wait_time[int(phase/2)] = temp
            print(wait_time)
            keep = False
            count += 1    
        elif phase % 2 == 1:
            keep = True 
        traci.simulationStep()

    return sum(wait_time) / len(wait_time)

def setTLS(self):
    TrafficLightPhases = []
    G4 = 120-self.state[0]-self.state[1]-self.state[2]
    TrafficLightPhases.append(traci.trafficlight.Phase(
        self.state[0], "rrrrrrrrrrrrGGGG", 0, 0, [], "setViaComplete"))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(3, "rrrrrrrrrrrryyyy", 0, 0))
    TrafficLightPhases.append(traci.trafficlight.Phase(
        self.state[1], "rrrrGGGGrrrrrrrr", 0, 0))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(3, "rrrryyyyrrrrrrrr", 0, 0))
    TrafficLightPhases.append(traci.trafficlight.Phase(
        self.state[2], "GGGGrrrrrrrrrrrr", 0, 0))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(3, "yyyyrrrrrrrrrrrr", 0, 0))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(G4,  "rrrrrrrrGGGGrrrr", 0, 0))
    TrafficLightPhases.append(
        traci.trafficlight.Phase(3, "rrrrrrrryyyyrrrr", 0, 0))
    logic = traci.trafficlight.Logic("InitState", 0, 0, TrafficLightPhases)
    traci.trafficlight.setProgramLogic('gneJ7', logic)

def Get_TLS_Fuction(self):
    while traci.simulation.getMinExpectedNumber() > 0:
        if (traci.simulation.getCurrentTime()) == 132000:
            action = TLS.randomAction()
            TLS.takeAction(action)
            print(self.state)
            TLS.setTLS()

        if (traci.simulation.getCurrentTime()) == 264000:
            action = TLS.randomAction()
            TLS.takeAction(action)
            print(self.state)
            TLS.setTLS()


        # แสดงไฟจราจรทั้งหมด
        # print(traci.trafficlight.getIDList())
        # แสดง State TLS ขณะนั้น
        # print(traci.trafficlight.getRedYellowGreenState('gneJ7'))
        # เวลาที่จะเปลี่ยนเป็น Next State
        # print(traci.trafficlight.getNextSwitch('gneJ7'))
        # เวลาของ State นั้่นๆ
        print(traci.trafficlight.getPhaseDuration('gneJ7'))
        # ข้อมูลของ State ทั้งหมด
        # print(traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ7'))
        # Index ของ State ไฟจราจรใน file .net.xml
        # print(traci.trafficlight.getPhase('gneJ7'))
        # id ของชุด TLS
        # print(traci.trafficlight.getProgram('gneJ7'))
        traci.simulationStep()
    traci.close()
    sys.stdout.flush()