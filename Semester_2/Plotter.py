import pandas
import matplotlib.pyplot as plt

class Plotter():
    def csvResultData(self,data,path,mode):
        self.dataframe = pandas.DataFrame(data)
        self.dataframe.to_csv(path,index=False,header=False, encoding='utf-8',mode=mode)

    def findAverage(self,path):
        queryList = ['Flow_Rate','Speed','Density','Waiting_Time','Arrival_Rate']
        result = []
        avg_result = [0,0,0,0,0]
        dataframe = pandas.read_csv(path)

        for query in (queryList):
            index = queryList.index(query)
            query_data = dataframe[query]
            avg_value = sum(query_data)/len(query_data)
            avg_result[index] = round(avg_value,2)

        result.append(avg_result)
        print(result)
        self.csvResultData(result,'./Semester_2/map/4-way/avg_result.csv','a')

    def plotData(self,path):
        fig , ax = plt.subplots(2,3)
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
        #ax[1,2].set_title("Flow-Density model")
        #ax[1,2].set_xlabel("Density")
        #ax[1,2].set_ylabel("Flow Rate")
        dataframe = pandas.read_csv(path)
        dataframe.plot(ax=ax[0,0],x="Time", y="Flow_Rate")
        dataframe.plot(ax=ax[0,1],x="Time", y="Speed")
        dataframe.plot(ax=ax[0,2],x="Time", y="Density")
        dataframe.plot(ax=ax[1,0],x="Time", y="Waiting_Time")
        dataframe.plot(ax=ax[1,1],x="Time", y="Arrival_Rate")
        plt.show()