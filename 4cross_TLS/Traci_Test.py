import os
import sys
import optparse
import random
# DOCUMENT https://sumo.dlr.de/docs/TraCI.html


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary
import traci
import traci.constants as tc

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def Get_Vehicel_Fuction():
    while traci.simulation.getMinExpectedNumber() > 0: 
        # แสดงรถทั้งหมดในระบบ ณ เวลานั้นๆ
        vehicle_id_list = traci.vehicle.getIDList()
        # แสดงเวลารอของรถแต่ละคัน (ทั้งหมด ณ ขณะนั้น)
        print([traci.vehicle.getWaitingTime(vehicle_id) for vehicle_id in vehicle_id_list]) 
        # แสดงเวลารอสะสมของรถแต่ละคัน (ทั้งหมด ณ ขณะนั้น)
        # print([traci.vehicle.getAccumulatedWaitingTime(vehicle_id) for vehicle_id in vehicle_id_list]) 
        traci.simulationStep()
    traci.close()
    sys.stdout.flush()

def Get_Lane_Fuction():
    while traci.simulation.getMinExpectedNumber() > 0: 
        # แสดงเลนทั้งหมด
        # print(traci.lane.getIDList()) 
        # จำนวนรถที่หยุด
        # print(traci.lane.getLastStepHaltingNumber('gneE10_0')) 
        # เวลารอของรถทุกคันในเลนนั้นๆ
        # print(traci.lane.getWaitingTime('gneE10_0')) 
        traci.simulationStep()
    traci.close()
    sys.stdout.flush()

def Get_TLS_Fuction():
    while traci.simulation.getMinExpectedNumber() > 0: 
        # แสดงไฟจราจรทั้งหมด
        # print(traci.trafficlight.getIDList()) 
        # แสดง State TLS ขณะนั้น
        # print(traci.trafficlight.getRedYellowGreenState('gneJ8'))
        # เวลาที่จะเปลี่ยนเป็น Next State
        # print(traci.trafficlight.getNextSwitch('gneJ8')) 
        # เวลาของ State นั้่นๆ 
        # print(traci.trafficlight.getPhaseDuration('gneJ8')) 
        # ข้อมูลของ State ทั้งหมด
        # print(traci.trafficlight.getCompleteRedYellowGreenDefinition('gneJ8')) 
        # Index ของ State ไฟจราจรใน file .net.xml 	
        # print(traci.trafficlight.getPhase('gneJ8')) 
        # id ของชุด TLS
        # print(traci.trafficlight.getProgram('gneJ8'))
        traci.simulationStep()
    traci.close()
    sys.stdout.flush()

def Get_Simulation_Fuction():
    while traci.simulation.getMinExpectedNumber() > 0: 
        # หมายเลขรถที่กำลังเข้ามาใน Network
        # print(traci.simulation.getDepartedIDList()) 
        # จำนวนรถที่อยู่ใน Network และที่รอเข้ามาใน Network
        # print(traci.simulation.getMinExpectedNumber()) 
        traci.simulationStep()
    traci.close()
    sys.stdout.flush()

def Set_TLS_Fuction():
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep() 
        # set ค่าเวลาของ Index ณ ขณะนั้น(เปลี่ยนแปลงแค่ช่วงเวลานั้นๆ)
        # traci.trafficlight.setPhaseDuration('gneJ8',20.00)
        # set State ของ Index ณ ขณะนั้น(เปลี่ยนแปลงแค่ช่วงเวลานั้นๆ)
        # traci.trafficlight.setRedYellowGreenState('gneJ8','yyyrrryyyrrr')
        
        # หากต้องการตั้งค่าของการเปลี่ยน TLS จะใช้ [คำสั่งเดียวกัน]
        # traci.trafficlight.setProgramLogic('gneJ8',)
        # traci.trafficlight.setCompleteRedYellowGreenDefinition('gneJ8',)
    traci.close()
    sys.stdout.flush()
   

if __name__ == "__main__":
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    traci.start([sumoBinary, "-c", "4cross_TLS/1_1Cross.sumocfg"])
    # Get_Vehicel_Fuction()
    # Get_Lane_Fuction()
    # Get_TLS_Fuction()
    # Get_Simulation_Fuction()
    # Set_TLS_Fuction()