import matplotlib.pyplot as plt
import pandas as pd


class LoginRecordDTO:

    def __init__(self, log):
        self.__statsInDate = {}
        for date in log.keys():
            dateStat = []
            for i in range(0, 5):
                dateStat.append(len(log.get(date).get(i)))
            self.__statsInDate[date.strftime('%Y-%m-%d')] = dateStat

    def getDataAsGraph(self):
        names = ['guests', 'regular\n members', 'only\n managers', 'only\n owners', 'system\n managers']
        plotdata = pd.DataFrame(self.__statsInDate, index=names)
        plotdata.plot(kind="bar", rot=0, title="Info of users")
        plt.show()
