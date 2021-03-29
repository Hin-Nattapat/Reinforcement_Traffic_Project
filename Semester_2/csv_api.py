import pandas
import matplotlib.pyplot as plt

class Csv_api():
    def __init__(self, path, query):
        self.path = path
        self.queryList = [query]
        self.saveToCsv(self.queryList)

    def saveToCsv(self, data, mode='w'):
        saveData = pandas.DataFrame(data)
        saveData.to_csv(self.path, index=False, header=False, encoding='utf-8', mode=mode)

    # def findAverage(self,path):
    #     queryList = ['Flow_Rate','Speed','Density','Waiting_Time','Arrival_Rate']
    #     result = []
    #     avg_result = [0,0,0,0,0]
    #     dataframe = pandas.read_csv(path)

    #     for query in (queryList):
    #         index = queryList.index(query)
    #         query_data = dataframe[query]
    #         avg_value = sum(query_data)/len(query_data)
    #         avg_result[index] = round(avg_value,2)

    #     result.append(avg_result)
    #     print(result)
    #     self.csvResultData(result,'./Semester_2/map/4-way/avg_result.csv','a')

    # def saveStateSpace(self,data,path):
    #     queryList = ['State','Q_Value','SumQ','MaxQ']
    #     result = []
    #     result.append(queryList)
    #     for x in data:
    #         temp = []
    #         temp.append(x)
    #         temp.append(data[x]['q_value'])
    #         temp.append(data[x]['sumQ'])
    #         temp.append(data[x]['maxQ'])
    #         result.append(temp)
            
    #     self.csvResultData(result,path,'w')

    # def createAvg_Q(self,path):
    #     queryList = ['Epoch','Avg_Q']
    #     result = []
    #     result.append(queryList)

    #     self.csvResultData(result,path,'w')

    # def createReward(self,path):
    #     queryList = ['Epoch','Reward']
    #     result = []
    #     result.append(queryList)

    #     self.csvResultData(result,path,'w')

    # def createAvgResult(self,path):
    #     queryList = ['Time','Avg_FlowRate','Avg_Speed','Avg_Density','Avg_WaitingTime','Avg_ArrivalRate','Avg_qLength','Avg_qSTD','Avg_QValue']
    #     result = []
    #     result.append(queryList)

    #     self.csvResultData(result,path,'w')

    def saveAvgResult(self,data):
        dataframe = pandas.read_csv(self.path)
        result = [dataframe.columns.values.tolist()] + dataframe.values.tolist()
        result.append(data)
            
        self.saveToCsv(result)


