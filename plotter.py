import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Plotter:
    def __init__(self):
        self.fig , self.ax = plt.subplots(3,2)
        self.ax[0,0].set_title("Waiting Time")
        self.ax[0,1].set_title("Density")
        self.ax[1,0].set_title("Average Speed")
        self.ax[1,1].set_title("Flow Rate")
        self.ax[2,0].set_title("Greenshields Linear model")
        self.ax[2,0].set_xlabel("Density")
        self.ax[2,0].set_ylabel("Average Speed")
        self.line1, = self.ax[0,0].plot([], [], lw=2)
        self.line2, = self.ax[0,1].plot([], [], lw=2, color='r')
        self.line3, = self.ax[1,0].plot([], [], lw=2, color='g')
        self.line4, = self.ax[1,1].plot([], [], lw=2, color='y')
        for ax in [self.ax[0,0], self.ax[0,1], self.ax[1,0], self.ax[1,1], self.ax[2,0]]:
            ax.set_ylim(0, 1)
            ax.set_xlim(0, 1)
            ax.grid()
        self.line = [self.line1, self.line2, self.line3, self.line4]
        self.epochs_value = []
        self.avg_Q_value = []
        self.w_time_value = []
        self.dens_value = []
        self.avg_spd_value = []
        self.f_rate_value = []

    def update_plot(self,epochs,w_time,dens,avg_spd,f_rate):
        self.epochs_value.append(epochs)
        self.w_time_value.append(w_time)
        self.dens_value.append(dens)
        self.avg_spd_value.append(avg_spd)
        self.f_rate_value.append(f_rate)
        self.scatter_plot()

    def scatter_plot(self):
        self.ax[2,0].scatter(self.avg_spd_value,self.dens_value,color = 'cyan')

    def animation(self,frame):
        self.line[0].set_data(self.epochs_value, self.w_time_value)
        self.line[1].set_data(self.epochs_value, self.dens_value)
        self.line[2].set_data(self.epochs_value, self.avg_spd_value)
        self.line[3].set_data(self.epochs_value, self.f_rate_value)
        for ax in [self.ax[0,0], self.ax[0,1], self.ax[1,0], self.ax[1,1]]:
            xmin, xmax = ax.get_xlim()
            if self.epochs_value != []:
                if self.epochs_value[-1] >= xmax:
                    ax.set_xlim(xmin, 2*xmax)
                    ax.figure.canvas.draw()

        xmin, xmax = self.ax[2,0].get_xlim()
        if self.avg_spd_value != []:
            if self.avg_spd_value[-1] >= xmax:
                self.ax[2,0].set_xlim(xmin, self.avg_spd_value[-1] + (self.avg_spd_value[-1]*0.2))
                self.ax[2,0].figure.canvas.draw()

        ymin, ymax = self.ax[0,0].get_ylim()
        if self.w_time_value != []:
            if self.w_time_value[-1] >= ymax:
                self.ax[0,0].set_ylim(ymin, self.w_time_value[-1]+ (self.w_time_value[-1]*0.2))
                self.ax[0,0].figure.canvas.draw()
            elif self.w_time_value[-1] <= ymin:
                self.ax[0,0].set_ylim(self.w_time_value[-1]+ (self.w_time_value[-1]*0.2), ymax)
                self.ax[0,0].figure.canvas.draw()

        ymin, ymax = self.ax[0,1].get_ylim()
        if self.dens_value != []:
            if self.dens_value[-1] >= ymax:
                self.ax[0,1].set_ylim(ymin, self.dens_value[-1]+ (self.dens_value[-1]*0.2))
                self.ax[0,1].figure.canvas.draw()
            elif self.dens_value[-1] <= ymin:
                self.ax[0,1].set_ylim(self.dens_value[-1]+ (self.dens_value[-1]*0.2), ymax)
                self.ax[0,1].figure.canvas.draw()

        ymin, ymax = self.ax[1,0].get_ylim()
        if self.avg_spd_value != []:
            if self.avg_spd_value[-1] >= ymax:
                self.ax[1,0].set_ylim(ymin, self.avg_spd_value[-1]+ (self.avg_spd_value[-1]*0.2))
                self.ax[1,0].figure.canvas.draw()
            elif self.avg_spd_value[-1] <= ymin:
                self.ax[1,0].set_ylim(self.avg_spd_value[-1]+ (self.avg_spd_value[-1]*0.2), ymax)
                self.ax[1,0].figure.canvas.draw()

        ymin, ymax = self.ax[1,1].get_ylim()
        if self.f_rate_value != []:
            if self.f_rate_value[-1] >= ymax:
                self.ax[1,1].set_ylim(ymin, self.f_rate_value[-1]+ (self.f_rate_value[-1]*0.2))
                self.ax[1,1].figure.canvas.draw()
            elif self.f_rate_value[-1] <= ymin:
                self.ax[1,1].set_ylim(self.f_rate_value[-1]+ (self.f_rate_value[-1]*0.2), ymax)
                self.ax[1,1].figure.canvas.draw()
        
        ymin, ymax = self.ax[2,0].get_ylim()
        if self.dens_value != []:
            if self.dens_value[-1] >= ymax:
                self.ax[2,0].set_ylim(ymin, self.dens_value[-1]+ (self.dens_value[-1]*0.2))
                self.ax[2,0].figure.canvas.draw()

        return self.line
