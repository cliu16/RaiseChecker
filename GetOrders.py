import sys
import datetime
import HttpHandler
import time
import MailHandler
import ConfigHandler

def process(raw):
    orderList = HttpHandler.getOrderList(raw)
    for orderNumber in orderList:
        HttpHandler.getOrder(orderNumber)

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

