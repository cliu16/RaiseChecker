import datetime
import HttpHandler
import time
import MailHandler
import ConfigHandler

def checkIsGoodDiscount(card):
    percent = card["percent"]
    price = card["listPrice"]
    if percent == "" or price == "":
        return False
    num_percent = float(percent[:-1].replace(',', ''))
    num_price = float(price[1:].replace(',', ''))
    min_percent = float(ConfigHandler.PercentMin)
    min_price = float(ConfigHandler.PriceMin)
    if(num_percent>=min_percent and num_price>=min_price):
        return True

    return False

idSet=set()
def checkIsNewDiscount(card):
    global idSet
    cardId = card["id"]
    print "CardId:"+cardId
    if cardId in idSet:
        return False
    idSet.add(cardId)
    return True
    
def sendEmailNotify(card):
    currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    msg = "TIME: " + currentTime + '\tPrice: ' + card["listPrice"] + '\tPercent: ' + card["percent"] + '\tFinal Price: ' + card["finalPrice"]
    print msg
    MailHandler.sendMsg(gcName+'\t'+card["listPrice"]+'\t'+card["percent"], msg)
    
def process():
    cardList = HttpHandler.getCardList(ConfigHandler.GiftCardName)
    for card in cardList:
        if checkIsGoodDiscount(card) and checkIsNewDiscount(card):
#            sendEmailNotify(card)
            HttpHandler.addToCartById(ConfigHandler.GiftCardName, card["id"])
    HttpHandler.checkout()

ConfigHandler.initConfig()
ConfigHandler.displayConfig()
HttpHandler.login(ConfigHandler.RaiseUser, ConfigHandler.RaisePass)
MailHandler.init(ConfigHandler.GmailUser, ConfigHandler.GmailUser)

while True:
    process()
    time.sleep(5)

HttpHandler.logout()
