import os
import sys
import optparse
from sumolib import checkBinary
import traci
import api
import reinforcement as RL
import random
import randomTrips

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


if __name__ == "__main__":
    lane = [['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
            ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
    initState = [15, 15, 15]
    MAX_EPOCHS = 1000
    CYCLE = 132
    TIME = MAX_EPOCHS*CYCLE
    rl = RL.TrafficLight(initState, lane)
    
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "4cross_TLS/1_1Cross.sumocfg"])
    rl.InitStateSpace()
    
    traci.route.add("rou_1",["gneE43", "gneE3", "gneE12","gneE32"])
    traci.route.add("rou_2",["gneE33", "gneE13","gneE10","gneE34"])
    traci.route.add("rou_3",["gneE35", "gneE11","gneE6","gneE40"])
    traci.route.add("rou_4",["gneE41", "gneE7", "gneE10", "gneE11", "gneE6", "gneE40"])
    traci.route.add("rou_5",["gneE43", "gneE3", "gneE12", "gneE13", "gneE8", "gneE42"])
    traci.route.add("rou_6",["gneE33" ,"gneE13", "gneE8", "gneE42"])
    traci.route.add("rou_7",["gneE33" ,"gneE13", "gneE8", "gneE3", "gneE12", "gneE32"])
    traci.route.add("rou_8",["gneE35", "gneE11", "gneE6", "gneE7","gneE10", "gneE34"])
    traci.route.add("rou_9",["gneE41","gneE7","gneE12","gneE32"])
    traci.route.add("rou_10",["gneE41", "gneE7", "gneE10","gneE34"])
    traci.route.add("rou_11",["gneE33","gneE13","gneE6","gneE40"])
    traci.route.add("rou_12",["gneE43", "gneE3", "gneE10", "gneE34"])
    
    RouteID = traci.route.getIDList()
    print("Test :",RouteID[1])
    for i in range(10000):
        index = random.randint(0,11)
        traci.vehicle.add("vehicle_"+str(i),RouteID[index],departSpeed="desired",)
        traci.vehicle.setMaxSpeed("vehicle_"+str(i),25.0)
        traci.simulationStep()

    # os.chdir("./4cross_TLS")
    # os.system('python randomTrips.py --net-file=1_1Cross.net.xml --route-file=1_1Cross.rou.xml --weights-prefix=1_1Cross --end='+str(TIME)+' --fringe-factor=10 --period=2.5 --trip-attributes="departLane=\'best\' departSpeed=\'max\' departPos=\'random\'"  -l --validate --fringe-factor 10  --max-distance 2000')

    # for i in range(MAX_EPOCHS):
    #     print("----------------------------- EPOCHS: ",i, "-----------------------------")
    #     # api.random_vehicle(i)
    #     rl.P_Greedy_Al()
    #     rl.updateFuction()
    #     rl.updateState()
    #     print("----------------------------------------------------------------------")
sys.stdout.flush()
