import pandas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#CSV structure
#Time,Flow Rate,Speed,Density,Waiting Time,Arrival Rate

fig , ax = plt.subplots(3,3)
ax[0,0].set_title("Flow Rate")
ax[0,0].set_xlabel("Time")
ax[0,0].set_ylabel("Flow Rate")
ax[0,1].set_title("Speed")
ax[0,1].set_xlabel("Time")
ax[0,1].set_ylabel("Speed")
ax[0,2].set_title("Density")
ax[0,2].set_xlabel("Time")
ax[0,2].set_ylabel("Density")
ax[1,0].set_title("Waiting Time")
ax[1,0].set_xlabel("Time")
ax[1,0].set_ylabel("Waiting Time")
ax[1,1].set_title("Arrival Rate")
ax[1,1].set_xlabel("Time")
ax[1,1].set_ylabel("Arrival Rate")
ax[1,2].set_title("Greenshields Linear model")
ax[1,2].set_xlabel("Density")
ax[1,2].set_ylabel("Average Speed")
ax[2,0].set_title("Speed-Flow model")
ax[2,0].set_xlabel("Flow Rate")
ax[2,0].set_ylabel("Speed")
ax[2,1].set_title("Flow-Density model")
ax[2,1].set_xlabel("Density")
ax[2,1].set_ylabel("Flow Rate")

def plotData(i):
    dataframe = pandas.read_csv("Semester_2/map/4-way/Rou_File/Period_1/result.csv")
    x = dataframe['Time']
    y1 = dataframe['Flow_Rate']
    y2 = dataframe['Speed']
    y3 = dataframe['Density']
    y4 = dataframe['Waiting_Time']
    y5 = dataframe['Arrival_Rate']
    plt.cla()
    
    ax[0,0].plot(x,y1,color = 'blue')
    ax[0,1].plot(x,y2,color = 'green')
    ax[0,2].plot(x,y3,color = 'red')
    ax[1,0].plot(x,y4,color = 'magenta')
    ax[1,1].plot(x,y5,color = 'grey')
    ax[1,2].scatter(y3,y2,color = 'deeppink')
    ax[2,0].scatter(y1,y2,color = 'mediumorchid')
    ax[2,1].scatter(y3,y1,color = 'skyblue')
    plt.tight_layout()


ani = FuncAnimation(fig, plotData, interval = 200)

plt.tight_layout()
plt.show()