import matplotlib.pyplot as plt
import pandas as pd


class LoginRecordDTO:

    def __init__(self, log):
        self.__log = log
    #
    # def getDataAsGraph(self):
    #     plt.title("info of user in the workshop")
    #     names = ['guests', 'regular\n members', 'only\n managers', 'only\n owners', 'system\n managers']
    #     for i in range(0, 5):
    #         values = self.__getInPos(i)
    #         plt.bar(names[i], values, width=0.25)
    #     plt.legend(self.__log.keys())
    #     plt.show()

    def getDataAsGraph(self):
        names = ['guests', 'regular\n members', 'only\n managers', 'only\n owners', 'system\n managers']
        statsInDate = self.__getInPos()
        plotdata = pd.DataFrame(statsInDate, index=names)
        plotdata.plot(kind="bar", rot=0)
        plt.show()

    def __getInPos(self):
        statsInDate = {}
        for date in self.__log.keys():
            dateStat = []
            for i in range(0, 5):
                dateStat.append(len(self.__log.get(date).get(i)))
            statsInDate[date] = dateStat
        return statsInDate

    # def __str__(self):
    #     toReturn = "Guests:" + str(self.__loginDateRecordGuest)
    #     toReturn += "\nOnly members:" + str(self.__loginDateRecordRegularMembers)
    #     toReturn += "\nOnly managers:" + str(self.__loginDateRecordJustManagers)
    #     toReturn += "\nOnly owners:" + str(self.__loginDateRecordJustOwners)
    #     toReturn += "\nsystem managers:" + str(self.__loginDateRecordSystemManager)
    #     return toReturn
