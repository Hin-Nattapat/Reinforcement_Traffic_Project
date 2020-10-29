import os
import sys
import optparse
from sumolib import checkBinary
import traci
import api
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

def plot_data(a):
    ani = FuncAnimation(plt.gcf(), a.animation_trafficload)
    plt.tight_layout()
    plt.show()
    thread_plot_data.join()

if __name__ == "__main__":
    lane = [['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
            ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
    initState = [15, 15, 15]  
    MAX_EPOCHS = 1000
    rl = RL.TrafficLight(initState,lane)

    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "4cross_TLS/1_1Cross.sumocfg"])

    rl.InitStateSpace()
    data = RL.Plotter()
    data.init_trafficload()
    global thread_plot_data
    thread_plot_data = threading.Thread(target=plot_data,args=(data,))
    for i in range(MAX_EPOCHS):
        print("----------------------------- EPOCHS: ",i,"-----------------------------")
        rl.P_Greedy_Al()
        rl.updateFuction()
        rl.updateState()
<<<<<<< Updated upstream
=======
        data.update_plot_trafficload(i,1,2,3,4)
        if i == 0:
            thread_plot_data.start()
        # rl.showQMax()
>>>>>>> Stashed changes
        print("----------------------------------------------------------------------")
    sys.stdout.flush()

    
    