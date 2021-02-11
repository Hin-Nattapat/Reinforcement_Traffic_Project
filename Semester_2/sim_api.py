import traci

class Simulation():
    def __init__(self, edge):
        self.edge = edge
        self.oldId = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
        self.carPass = [0, 0, 0, 0]
        self.length = 900
        self.tls_id = ''

    def simulate(self, duration):
        result = {
            "speed" : [0.0, 0.0, 0.0, 0.0],
            "f_rate" : [0.0, 0.0, 0.0, 0.0],
            "dens" : [0.0, 0.0, 0.0, 0.0],
            "w_time" : [0.0, 0.0, 0.0, 0.0],
            "q_length" : [0.0, 0.0, 0.0, 0.0],
            "arrival" : 0.0
        }
        time = 0

        while time < duration:
            traci.simulationStep()
            for i in range(len(self.edge)):
                result["speed"][i] += self.get_avg_speed(self.edge[i])
                result["f_rate"][i] += self.get_flow_rate(self.edge[i])
                result["dens"][i] += self.get_density(self.edge[i])
                result["w_time"][i] += self.get_waiting_time(self.edge[i])
                result["q_length"][i] += self.get_length(self.edge[i])
            result["arrival"] += self.get_arrival()
            time += 1
        
        for i in range(len(self.edge)):
            result["speed"][i] = round((result["speed"][i] / duration * 3.6), 2)
            result["f_rate"][i] = round((result["f_rate"][i] * 3600 / duration), 2)
            result["dens"][i] = round((result["dens"][i] * 1000 / self.length / duration), 2)
            result["w_time"][i] = round((result["w_time"][i] / duration), 2)
            result["q_length"][i] = round((result["q_length"][i] * 6 / duration), 2) 
        result["arrival"] = round((result["arrival"] * 3600 / duration), 2)

        print("Result",result)
        return result

    def get_avg_speed(self, e_id):
        #return average speed of edge in m/s
        avg_spd = 0
        if traci.edge.getLastStepVehicleNumber(e_id) > 0:
            avg_spd = traci.edge.getLastStepMeanSpeed(e_id)
        return avg_spd

    def get_flow_rate(self, e_id):
        e_index = self.edge.index(e_id)
        for lane in range(0, 2):
            num = traci.inductionloop.getLastStepVehicleNumber('e1_' + e_id + '_' + str(lane))
            curID = traci.inductionloop.getLastStepVehicleIDs('e1_' + e_id + '_' + str(lane))
            if num > 0 and curID != self.oldId[e_index][lane]:
                self.oldId[e_index][lane] = curID
                self.carPass[e_index] += 1
        flow_rate = self.carPass[e_index] / traci.simulation.getTime()        
        
        return flow_rate

    def get_density(self, e_id):
        return traci.edge.getLastStepVehicleNumber(e_id)

    def get_waiting_time(self, e_id):
        total_time = 0
        vehs = traci.edge.getLastStepVehicleIDs(e_id)
        num_wait = 0
        if len(vehs) > 0:
            for vid in vehs:
                wait = traci.vehicle.getAccumulatedWaitingTime(vid)
                if wait > 0:
                    total_time += wait
                    num_wait += 1
            if num_wait > 0:
                return total_time/num_wait
                
        return 0
    
    def get_length(self, e_id): #queue length in m
        lane_0 = traci.lane.getLastStepHaltingNumber(e_id + '_0')
        lane_1 = traci.lane.getLastStepHaltingNumber(e_id + '_1')
        length = ((lane_0 + lane_1) / 2)
        return length

    def get_arrival(self):
        return traci.simulation.getDepartedNumber()    
    
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

