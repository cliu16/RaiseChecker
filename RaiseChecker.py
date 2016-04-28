import sys
import datetime
import HttpHandler
import time
import MailHandler
import ConfigHandler

priceTotalOrder = 0
cardsTotalOrder = 0

def checkIsGoodDiscount(card):
    num_percent = float(card["percent"])
    num_price = float(card["listPrice"])
    min_percent = float(ConfigHandler.PercentMin)
    min_price = float(ConfigHandler.PriceMin)
    if(num_percent>=min_percent and num_price>=min_price):
        return True

    return False

idSet=set()
def checkIsNewDiscount(card):
    global idSet
    cardId = card["id"]
    if cardId in idSet:
        return False
    idSet.add(cardId)
    return True

def clearSet():
    global idSet
    idSet=set()
    
def sendEmailNotify(card):
    currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    msg = "TIME: " + str(currentTime) + '\tPrice: $' + str(card["listPrice"]) + '\tPercent: ' + str(card["percent"]) + '%\tFinal Price: $' + str(card["finalPrice"])
    print msg
    MailHandler.sendMsg("Purchase Log : " + ConfigHandler.GiftCardName + '\t$'+str(card["listPrice"])+'\t'+str(card["percent"])+'%', msg)

def addCardsToCart(purchaseList):
    for oneCard in purchaseList:
        time.sleep(1)
        sendEmailNotify(oneCard)
        HttpHandler.addToCartById(ConfigHandler.GiftCardName, oneCard["id"])
        
def process():
    global priceTotalOrder
    global cardsTotalOrder
    cartInfo = HttpHandler.getCartInfo()
    cardList = HttpHandler.getCardList(ConfigHandler.GiftCardName)
    countCart = cartInfo["count"]
    priceCart = cartInfo["totalPrice"]
    countSum = 0
    priceSum = 0
    purchaseList = []
    for card in cardList:
        if priceTotalOrder + priceSum + card["finalPrice"] + priceCart > ConfigHandler.MaxPriceTotalOrder:
            continue
        if cardsTotalOrder + countSum + 1 + countCart > ConfigHandler.MaxCardsTotalOrder:
            continue
        if countSum + 1 + countCart > ConfigHandler.MaxCardsPerOrder:
            continue
        if priceSum + card["finalPrice"] + priceCart > ConfigHandler.MaxPricePerOrder:
            continue
        if not checkIsGoodDiscount(card):
            continue
        if not checkIsNewDiscount(card):
            continue
        countSum += 1
        priceSum += card["finalPrice"]
        priceTotalOrder += card["finalPrice"]
        cardsTotalOrder += 1
        purchaseList.append(card)
    if len(purchaseList) == 0:
        return checkIfContinue(priceTotalOrder, cardsTotalOrder)
    addCardsToCart(purchaseList)
    time.sleep(1)
    HttpHandler.checkout()
    clearSet()
    HttpHandler.clearShoppingCart()
    return checkIfContinue(priceTotalOrder, cardsTotalOrder)

def checkIfContinue(priceTotalOrder, cardsTotalOrder):
    print "Ping Info : " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + '\n\tCards Total Purchased : ' + str(cardsTotalOrder) + '/' + str(ConfigHandler.MaxCardsTotalOrder)  + '\n\tPrice Total Purchased : ' + str(priceTotalOrder) + '/' + str(ConfigHandler.MaxPriceTotalOrder)
    if priceTotalOrder >= ConfigHandler.MaxPriceTotalOrder:
        return False
    if cardsTotalOrder >= ConfigHandler.MaxCardsTotalOrder:
        return False
    return True

if __name__ == "__main__":
    configFile = None
    if len(sys.argv) == 2:
        configFile = sys.argv[1]
    ConfigHandler.initConfig(configFile)
    ConfigHandler.displayConfig()
    HttpHandler.login(ConfigHandler.RaiseUser, ConfigHandler.RaisePass, ConfigHandler.VisibleBrowser)
    MailHandler.init(ConfigHandler.GmailUser, ConfigHandler.GmailPass)

    ret = True
    while ret:
        try:
            ret = process()
            time.sleep(5)
        except:
            ret = False

    time.sleep(5)
    HttpHandler.logout()
