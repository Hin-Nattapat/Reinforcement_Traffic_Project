import matplotlib.pyplot as plt
import pandas
import numpy as np

route = 'p3'
runningMap = 4

resultFix = pandas.read_csv(
    "Semester_2/map/%s-way/result/fix_result_%s.csv" % (runningMap, route))
resultPRL = pandas.read_csv(
    "Semester_2/map/%s-way/result/PRL_result_%s.csv" % (runningMap, route))
resultSRL = pandas.read_csv(
    "Semester_2/map/%s-way/result/SRL_result_%s.csv" % (runningMap, route))

rewardFix = pandas.read_csv(
    "Semester_2/map/%s-way/result/fix_reward_%s.csv" % (runningMap, route))
rewardPRL = pandas.read_csv(
    "Semester_2/map/%s-way/result/PRL_reward_%s.csv" % (runningMap, route))
rewardSRL = pandas.read_csv(
    "Semester_2/map/%s-way/result/SRL_reward_%s.csv" % (runningMap, route))

# x-axis
x_time = resultFix['time']
x_epoch = rewardFix['epoch']
xp_time = resultPRL['time']
xs_time = resultSRL['time']
xp_epoch = rewardPRL['epoch']
xs_epoch = rewardSRL['epoch']
# y-axis fixedTime
yf_flow = resultFix['avgFlowRate']
yf_spd = resultFix['avgSpeed']
yf_dens = resultFix['avgDensity']
yf_wait = resultFix['avgWaiting']
yf_qLength = resultFix['avgQLength']
yf_green = rewardFix['greenTime']
# y-axis TSCRL
yp_flow = resultPRL['avgFlowRate']
yp_spd = resultPRL['avgSpeed']
yp_dens = resultPRL['avgDensity']
yp_wait = resultPRL['avgWaiting']
yp_qLength = resultPRL['avgQLength']
yp_green = rewardPRL['greenTime']
yp_rew = rewardPRL['reward']
# y-axis Proposed
ys_flow = resultSRL['avgFlowRate']
ys_spd = resultSRL['avgSpeed']
ys_dens = resultSRL['avgDensity']
ys_wait = resultSRL['avgWaiting']
ys_qLength = resultSRL['avgQLength']
ys_green = rewardSRL['greenTime']
ys_rew = rewardSRL['reward']


def plotBar(ax, y1, y2, y3, label_y):
    pos = [1, 2, 3, 4, 5, ]
    
    y_val = [ 0, y1, y2, y3, 0, ]
    label_x = [ None, 'Proposed', 'TSCRL', 'Fix', None]
    width = 0.6
    
    # ax.set_ylim(0, 50)
    rects1 = ax.bar(pos, y_val, width=width,edgecolor='w', color=[
                     'w', 'navy', 'darkred', 'green', 'w',])
    # ax.locator_params(nbins=3)
    ax.set_ylabel(label_y, fontsize=12)
    ax.set_xticks(pos)
    ax.set_xticklabels(label_x, rotation=30)
    ax.bar_label(rects1,padding=3, labels=['','%.1f'%y1,'%.2f'%y2,'%.2f'%y3,''])
    ax.margins(0.15)


plt.close('all')
fig = plt.figure()

bar1 = plt.subplot2grid((2, 3), (0, 0))
bar2 = plt.subplot2grid((2, 3), (0, 1))
bar3 = plt.subplot2grid((2, 3), (0, 2))
bar4 = plt.subplot2grid((2, 3), (1, 0))
bar5 = plt.subplot2grid((2, 3), (1, 1))
bar6 = plt.subplot2grid((2, 3), (1, 2))

wait_f = sum(yf_wait) / len(yf_wait)
wait_p = sum(yp_wait) / len(yp_wait)
wait_s = sum(ys_wait) / len(ys_wait)
plotBar(bar1, wait_s, wait_p, wait_f, 'avg Waiting time')

green_f = sum(yf_green) / len(yf_green)
green_p = sum(yp_green) / len(yp_green)
green_s = sum(ys_green) / len(ys_green)
plotBar(bar2, green_s, green_p, green_f, 'avg Green time')

q_f = sum(yf_qLength) / len(yf_qLength)
q_p = sum(yp_qLength) / len(yp_qLength)
q_s = sum(ys_qLength) / len(ys_qLength)
plotBar(bar3, q_s, q_p, q_f, 'avg Queue length')

den_f = sum(yf_dens) / len(yf_dens)
den_p = sum(yp_dens) / len(yp_dens)
den_s = sum(ys_dens) / len(ys_dens)
plotBar(bar4, den_s, den_p, den_f, 'avg Density')

flow_f = sum(yf_flow) / len(yf_flow)
flow_p = sum(yp_flow) / len(yp_flow)
flow_s = sum(ys_flow) / len(ys_flow)
plotBar(bar5, flow_s, flow_p, flow_f, 'avg Flow rate')

spd_f = sum(yf_spd) / len(yf_spd)
spd_p = sum(yp_spd) / len(yp_spd)
spd_s = sum(ys_spd) / len(ys_spd)
plotBar(bar6, spd_s, spd_p, spd_f, 'avg Speed')

# plt.tight_layout()
plt.show()
