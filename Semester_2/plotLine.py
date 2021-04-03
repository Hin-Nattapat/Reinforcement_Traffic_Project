import matplotlib.pyplot as plt
import pandas

route = 'p1'
runningMap = 16

resultFix = pandas.read_csv("Semester_2/map/%s-way/result/fix_result_%s.csv" %(runningMap, route))
resultPRL = pandas.read_csv("Semester_2/map/%s-way/result/PRL_result_%s.csv" %(runningMap, route))
resultSRL = pandas.read_csv("Semester_2/map/%s-way/result/SRL_result_%s.csv" %(runningMap, route))

rewardFix = pandas.read_csv("Semester_2/map/%s-way/result/fix_reward_%s.csv" %(runningMap, route))
rewardPRL = pandas.read_csv("Semester_2/map/%s-way/result/PRL_reward_%s.csv" %(runningMap, route))
rewardSRL = pandas.read_csv("Semester_2/map/%s-way/result/SRL_reward_%s.csv" %(runningMap, route))

#x-axis
x_time = resultFix['time']
x_epoch = rewardFix['epoch']
xp_time = resultPRL['time']
xs_time = resultSRL['time']
xp_epoch = rewardPRL['epoch']
xs_epoch = rewardSRL['epoch']

#y-axis fixedTime
yf_flow = resultFix['avgFlowRate']
yf_spd = resultFix['avgSpeed']
yf_dens = resultFix['avgDensity']
yf_wait = resultFix['avgWaiting']
yf_qLength = resultFix['avgQLength']
yf_green = rewardFix['greenTime']
#y-axis TSCRL
yp_flow = resultPRL['avgFlowRate']
yp_spd = resultPRL['avgSpeed']
yp_dens = resultPRL['avgDensity']
yp_wait = resultPRL['avgWaiting']
yp_qLength = resultPRL['avgQLength']
yp_green = rewardPRL['greenTime']
yp_rew = rewardPRL['reward']
#y-axis Proposed
ys_flow = resultSRL['avgFlowRate']
ys_spd = resultSRL['avgSpeed']
ys_dens = resultSRL['avgDensity']
ys_wait = resultSRL['avgWaiting']
ys_qLength = resultSRL['avgQLength']
ys_green = rewardSRL['greenTime']
ys_rew = rewardSRL['reward']

def plotLine(ax, x, y, label_x, label_y, line, color, ylim):
    ax.set_ylim(ylim[0], ylim[1])
    ax.plot(x, y, label=line, color=color)
    ax.set_xlabel(label_x, fontsize=9)
    ax.set_ylabel(label_y, fontsize=9)
    ax.legend()
    # ax.set_title(title, fontsize=10)

plt.close('all')
fig = plt.figure()

 # waiting time, queue length, green time, reward
line1 = plt.subplot2grid((2, 8), (0, 0), colspan=4)
line2 = plt.subplot2grid((2, 8), (0, 4), colspan=4)
line3 = plt.subplot2grid((2, 8), (1, 0), colspan=4)
line4 = plt.subplot2grid((2, 8), (1, 4), colspan=4)

plotLine(line1, x_time, yf_wait, 'time', 'avg Waiting time', 'FixedTime', 'navajowhite', [0,120])
plotLine(line1, xp_time, yp_wait, 'time', 'avg Waiting time', 'TSCRL', 'lightpink', [0,120])
plotLine(line1, xs_time, ys_wait, 'time', 'avg Waiting time', 'Proposed', 'cornflowerblue', [0,120])

plotLine(line2, x_time, yf_qLength, 'time', 'avg Queue length', 'FixedTime', 'navajowhite', [0,1500])
plotLine(line2, xp_time, yp_qLength, 'time', 'avg Queue length', 'TSCRL', 'lightpink', [0,1500])
plotLine(line2, xs_time, ys_qLength, 'time', 'avg Queue length', 'Proposed', 'cornflowerblue', [0,1500])

plotLine(line3, x_epoch, yf_green, 'time', 'avg Green time', 'FixedTime', 'navajowhite', [25,80])
plotLine(line3, xp_epoch, yp_green, 'time', 'avg Green time', 'TSCRL', 'lightpink', [25,80])
plotLine(line3, xs_epoch, ys_green, 'time', 'avg Green time', 'Proposed', 'cornflowerblue', [25,80])

plotLine(line4, xp_epoch, yp_rew, 'time', 'Reward', 'TSCRL', 'lightpink', [-10, 10])
plotLine(line4, xs_epoch, ys_rew, 'time', 'Reward', 'Proposed', 'cornflowerblue', [-10,10])

plt.tight_layout()
plt.show()