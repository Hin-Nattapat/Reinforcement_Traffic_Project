import pandas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#CSV structure
#Time,Flow Rate,Speed,Density,Waiting Time,Arrival Rate

#Warning!!! The Current Data that using in this module was mocked up.

def plot_line(ax,data_x,data_y,label_x,label_y,line_label,color):
    ax.set_xlabel(label_x, fontsize=10)
    ax.set_ylabel(label_y, fontsize=10)
    ax.plot(data_x,data_y,label =line_label,color = color)
    # ax.legend()

def plot_bar_3(ax,data1,data2,data3,label1,label2,label3,label_y):
    ax.set_ylabel(label_y)
    label = [label1, label2, label3]
    data = [data1,data2,data3]
    ax.bar(label,data,color=['Red', 'Yellow', 'Green'])

def plot_bar_2(ax,data1,data2,label1,label2,label_y):
    ax.set_ylabel(label_y)
    label = [label1, label2]
    data = [data1,data2]
    ax.bar(label,data,color=['Red', 'Green'])

fig = plt.figure()

# dataframe = pandas.read_csv("Semester_2/map/4-way/result/result.csv")
dataframe_fix = pandas.read_csv("Semester_2/map/4-way/result/fix_result_p1.csv")
dataframe_paper = pandas.read_csv("Semester_2/map/4-way/result/PRL_result_p1.csv")
dataframe = pandas.read_csv("SemeSter_2/map/4-way/result/SRL_result_p1.csv")
dataframe_reward_fix = pandas.read_csv("SemeSter_2/map/4-way/result/fix_reward_p1.csv")
dataframe_reward = pandas.read_csv("SemeSter_2/map/4-way/result/SRL_reward_p1.csv")
dataframe_reward_paper = pandas.read_csv("SemeSter_2/map/4-way/result/PRL_reward_p1.csv")

#SRL
x = dataframe['time']
x_epoch = dataframe_reward['epoch']
y1 = dataframe['avgFlowRate']
y2 = dataframe['avgSpeed']
y3 = dataframe['avgDensity']
y4 = dataframe['avgWaiting']
y5 = dataframe_reward['greenTime']
y6 = dataframe_reward['reward']
y7 = dataframe['avgQLength']

#FIX
x_fix = dataframe_fix['time']
x_fix_epoch = dataframe_reward_fix['epoch']
y1_fix = dataframe_fix['avgFlowRate']
y2_fix = dataframe_fix['avgSpeed']
y3_fix = dataframe_fix['avgDensity']
y4_fix = dataframe_fix['avgWaiting']
y5_fix = dataframe_reward_fix['greenTime']
y7_fix = dataframe_fix['avgQLength']

#PRL
x_paper = dataframe_paper['time']
x_paper_epoch = dataframe_reward_paper['epoch']
y1_paper = dataframe_paper['avgFlowRate']
y2_paper = dataframe_paper['avgSpeed']
y3_paper = dataframe_paper['avgDensity']
y4_paper = dataframe_paper['avgWaiting']
y5_paper = dataframe_reward_paper['greenTime']
y6_paper = dataframe_reward_paper['reward']
y7_paper = dataframe_paper['avgQLength']

ax1 = plt.subplot2grid((12,18),(0,0),colspan = 8,rowspan=3)
ax2 = plt.subplot2grid((12,18),(4,0),colspan = 8,rowspan=3)
ax3 = plt.subplot2grid((12,18),(0,10),colspan = 8,rowspan=3)
ax11 = plt.subplot2grid((12,18),(4,10),colspan = 8,rowspan=3)
ax4 = plt.subplot2grid((12,18),(9,0),colspan = 2,rowspan=2)
ax5 = plt.subplot2grid((12,18),(9,3),colspan = 2,rowspan=2)
ax6 = plt.subplot2grid((12,18),(9,6),colspan = 2,rowspan=2)
ax7 = plt.subplot2grid((12,18),(9,9),colspan = 2,rowspan=2)
ax8 = plt.subplot2grid((12,18),(9,12),colspan = 2,rowspan=2)
ax9 = plt.subplot2grid((12,18),(9,15),colspan = 2,rowspan=2)

plot_line(ax1,x,y4,'Time','Waiting Time','Proposed','Red')
plot_line(ax1,x_fix,y4_fix,'Time','Waiting Time','FixedTime','Yellow')
plot_line(ax1,x_paper,y4_paper,'Time','Waiting Time','TSCRL','Green')

plot_line(ax2,x,y7,'Time','Queue Length','Proposed','Red')
plot_line(ax2,x_fix,y7_fix,'Time','Queue Length','FixedTime','Yellow')
plot_line(ax2,x_paper,y7_paper,'Time','Queue Length','TSCRL','Green')

plot_line(ax3,x_epoch,y5,'Epoch','Green Time','Proposed','Red')
plot_line(ax3,x_fix_epoch,y5_fix,'Epoch','Green Time','FixedTime','Yellow')
plot_line(ax3,x_paper_epoch,y5_paper,'Epoch','Green Time','TSCRL','Green')

plot_line(ax11,x_epoch,y6,'Epoch','Reward','Proposed','Red')
plot_line(ax11,x_paper_epoch,y6_paper,'Epoch','Reward','TSCRL','Green')

plot_bar_3(ax4,sum(y4_fix)/len(y4_fix),sum(y4_paper)/len(y4_paper),sum(y4)/len(y4),'FixedTime','TSCRL','Proposed','Avg Waiting Time')
plot_bar_3(ax5,sum(y5_fix)/len(y5_fix),sum(y5_paper)/len(y5_paper),sum(y5)/len(y5),'FixedTime','TSCRL','Proposed','Avg Green Time')
plot_bar_3(ax6,sum(y3_fix)/len(y3_fix),sum(y3_paper)/len(y3_paper),sum(y3)/len(y3),'FixedTime','TSCRL','Proposed','Avg Density')
plot_bar_3(ax7,sum(y7_fix)/len(y7_fix),sum(y7_paper)/len(y7_paper),sum(y7)/len(y7),'FixedTime','TSCRL','Proposed','Avg Queue Length')
plot_bar_3(ax8,sum(y1_fix)/len(y1_fix),sum(y1_paper)/len(y1_paper),sum(y1)/len(y1),'FixedTime','TSCRL','Proposed','Avg Flow Rate')
plot_bar_3(ax9,sum(y2_fix)/len(y2_fix),sum(y2_paper)/len(y2_paper),sum(y2)/len(y2),'FixedTime','TSCRL','Proposed','Avg Speed')

# plt.tight_layout()
plt.xticks(rotation=45)
plt.show()