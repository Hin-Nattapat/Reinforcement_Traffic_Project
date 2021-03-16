import pandas
import matplotlib.pyplot as plt

class Csv_api():
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
