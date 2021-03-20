import pandas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#CSV structure
#Time,Flow Rate,Speed,Density,Waiting Time,Arrival Rate

#Warning!!! The Current Data that using in this module was mocked up.

def plot_line(ax,data_x,data_y,label_x,label_y,line_label,color):

    ax.set_xlabel(label_x, fontsize=12)
    ax.set_ylabel(label_y, fontsize=12)
    ax.plot(data_x,data_y,label =line_label,color = color)
    ax.legend()

def plot_bar(ax,data1,data2,data3,label1,label2,label3,label_y):
    
    ax.set_ylabel(label_y)
    label = [label1, label2, label3]
    data = [data1,data2,data3]
    ax.bar(label,data,color=['Red', 'Yellow', 'Green'])


fig = plt.figure()

dataframe = pandas.read_csv("Semester_2/map/4-way/Rou_File/Period_1/result.csv")
dataframe_fix = pandas.read_csv("Semester_2/map/4-way/Rou_File/Period_1/result_fix.csv")
dataframe_paper = pandas.read_csv("Semester_2/map/4-way/Rou_File/Period_1/result_paper.csv")

x = dataframe['Time']
y1 = dataframe['Flow_Rate']
y2 = dataframe['Speed']
y3 = dataframe['Density']
y4 = dataframe['Waiting_Time']
y5 = dataframe['Arrival_Rate']

x_fix = dataframe_fix['Time']
y1_fix = dataframe_fix['Flow_Rate']
y2_fix = dataframe_fix['Speed']
y3_fix = dataframe_fix['Density']
y4_fix = dataframe_fix['Waiting_Time']
y5_fix = dataframe_fix['Arrival_Rate']

x_paper = dataframe_paper['Time']
y1_paper = dataframe_paper['Flow_Rate']
y2_paper = dataframe_paper['Speed']
y3_paper = dataframe_paper['Density']
y4_paper = dataframe_paper['Waiting_Time']
y5_paper = dataframe_paper['Arrival_Rate']

ax1 = plt.subplot2grid((9,13),(0,0),colspan = 7,rowspan=2)
ax2 = plt.subplot2grid((9,13),(3,0),colspan = 7,rowspan=2)
ax3 = plt.subplot2grid((9,13),(6,0),colspan = 7,rowspan=2)
ax4 = plt.subplot2grid((9,13),(0,8),colspan = 2,rowspan=2)
ax5 = plt.subplot2grid((9,13),(3,8),colspan = 2,rowspan=2)
ax6 = plt.subplot2grid((9,13),(6,8),colspan = 2,rowspan=2)
ax7 = plt.subplot2grid((9,13),(0,11),colspan = 2,rowspan=2)
ax8 = plt.subplot2grid((9,13),(3,11),colspan = 2,rowspan=2)
ax9 = plt.subplot2grid((9,13),(6,11),colspan = 2,rowspan=2)

plot_line(ax1,x,y3,'Time','Waiting Time','SmarterRL','Red')
plot_line(ax1,x_fix,y3_fix,'Time','Waiting Time','Fixed','Yellow')
plot_line(ax1,x_paper,y3_paper,'Time','Waiting Time','Paper','Green')
plot_line(ax2,x,y4,'Time','Queue Length','SmarterRL','Red')
plot_line(ax2,x_fix,y4_fix,'Time','Queue Length','Fixed','Yellow')
plot_line(ax2,x_paper,y4_paper,'Time','Queue Length','Paper','Green')
plot_line(ax3,x,y5,'Time','Green Time','SmarterRL','Red')
plot_line(ax3,x_fix,y5_fix,'Time','Green Time','Fixed','Yellow')
plot_line(ax3,x_paper,y5_paper,'Time','Green Time','Paper','Green')
plot_bar(ax4,max(y4),max(y4_fix),max(y4_paper),'SmarterRL','Fixed','Paper','Avg Waiting Time')
plot_bar(ax5,max(y5),max(y5_fix),max(y5_paper),'SmarterRL','Fixed','Paper','Avg Green Time')
plot_bar(ax6,max(y3),max(y3_fix),max(y3_paper),'SmarterRL','Fixed','Paper','Avg Density')
plot_bar(ax7,max(y5),max(y5_fix),max(y5_paper),'SmarterRL','Fixed','Paper','Avg Queue Length')
plot_bar(ax8,max(y1),max(y1_fix),max(y1_paper),'SmarterRL','Fixed','Paper','Avg Flow Rate')
plot_bar(ax9,max(y2),max(y2_fix),max(y2_paper),'SmarterRL','Fixed','Paper','Avg Speed')

plt.tight_layout()
plt.show()