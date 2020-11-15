import os
import sys
import optparse
from sumolib import checkBinary
import traci
import api
import plotter
import reinforcement as RL
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import threading

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


def main_program_fixed(epochs,plot_data):
    while True:
        print("----------------------------- EPOCHS: ",epochs, "-----------------------------")
        result = call_api.get_obj(initState,epochs)
        plot_data.update_plot(epochs,result['w_time'],result['dens'],result['avg_spd'],result['f_rate'])
        epochs = epochs+1
        print("----------------------------------------------------------------------")

def main_program(epochs,rl_data,plot_data,traci_data):
    while True:
        print("----------------------------- EPOCHS: ",epochs, "-----------------------------")
        current_state = rl_data.state
        action = rl_data.P_Greedy_Al()
        new_state = rl_data.takeAction(action, current_state)
        result = call_api.get_obj(new_state)
        rl_data.updateFuction(result['w_time'])
        rl_data.updateState()
        plot_data.update_plot(epochs,result['w_time'],result['dens'],result['avg_spd'],result['f_rate'])
        epochs = epochs+1
        #กูใส่ traci_data เข้ามาละ 
        print("----------------------------------------------------------------------")

if __name__ == "__main__":
    fix_traffic = True
    global initState
    lane = [['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
            ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
    if fix_traffic is True:
        initState = [30, 30, 30]
    else:
        initState = [30, 30, 30]
    MAX_EPOCHS = 1000
    EPOCHS = 0
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
    api.add_Route()

    # # os.chdir("./4cross_TLS")
    # # os.system('python randomTrips.py --net-file=1_1Cross.net.xml --route-file=1_1Cross.rou.xml --weights-prefix=1_1Cross --end='+str(TIME)+' --fringe-factor=10 --period=2.5 --trip-attributes="departLane=\'best\' departSpeed=\'max\' departPos=\'random\'"  -l --validate --fringe-factor 10  --max-distance 2000')

    # # for i in range(MAX_EPOCHS):
    call_api = api.API()
    data = plotter.Plotter()
    traci_data = api.API()
    global thread_main_data
    if fix_traffic is True:
        thread_main_data = threading.Thread(target=main_program_fixed,args=(EPOCHS,data,))
    else:
        thread_main_data = threading.Thread(target=main_program,args=(EPOCHS,rl,data,traci_data,))
    thread_main_data.start()
    ani = FuncAnimation(data.fig,data.animation)
    plt.tight_layout()
    plt.show()
sys.stdout.flush()
