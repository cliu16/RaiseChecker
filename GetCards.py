import sys
import datetime
import HttpHandler
import time
import MailHandler
import ConfigHandler

def process():
    orderList = HttpHandler.getOrderList()
    for order in orderList:
        print order

if __name__ == "__main__":
    configFile = None
    if len(sys.argv) == 2:
        configFile = sys.argv[1]
    ConfigHandler.initConfig(configFile)
    ConfigHandler.displayConfig()
    HttpHandler.login(ConfigHandler.RaiseUser, ConfigHandler.RaisePass, ConfigHandler.VisibleBrowser)
    process()
    time.sleep(5)
    HttpHandler.logout()

