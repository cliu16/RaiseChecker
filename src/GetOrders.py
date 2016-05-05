import sys
import datetime
import HttpHandler
import time
import MailHandler
import ConfigHandler

def process(raw):
    orderInfoList = getOrderInfo(raw)
    fName = ConfigHandler.GiftCardName + "-" + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ".csv"
    saveListToFile(fName , orderInfoList)
    
def getOrderInfo(raw):
    orderList = HttpHandler.getOrderList(raw)
    orderInfoList = []
    for orderNumber in orderList:
        orderInfoList.append(HttpHandler.getOrder(orderNumber))
    return orderInfoList

def saveListToFile(fName, orderInfoList):
    with open(fName, 'w') as f:
        f.write("Face Value, Price, SN, PIN\n")
        for orderInfo in orderInfoList:
            line = str(orderInfo["faceValue"]) + "," + str(orderInfo["price"]) + "," + str(orderInfo["SN"]) + "," + str(orderInfo["PIN"])
            f.write(line+"\n")
            
if __name__ == "__main__":
    configFile = None
    if len(sys.argv) == 2:
        configFile = sys.argv[1]
    ConfigHandler.initConfig(configFile)
    ConfigHandler.displayConfig()
    raw = raw_input("Input the start date of your order (mm/dd/yy) or how many orders you want to look up (1 , 2 etc).")
    HttpHandler.login(ConfigHandler.RaiseUser, ConfigHandler.RaisePass, ConfigHandler.VisibleBrowser)
    process(raw)
    time.sleep(5)
    HttpHandler.logout()

