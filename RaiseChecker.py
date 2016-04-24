import datetime
import HttpHandler
import time
import MailHandler
import ConfigHandler

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
    print "len set : " + str(len(idSet))
    if cardId in idSet:
        print "contains " + cardId
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
    cartInfo = HttpHandler.getCartInfo()
    cardList = HttpHandler.getCardList(ConfigHandler.GiftCardName)
    countCart = cartInfo["count"]
    priceCart = cartInfo["totalPrice"]
    print "Ping Info : " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + '\tCards in Cart : ' + str(countCart) + '\tTotal Price in Cart : ' + str(priceCart)
    countSum = 0
    priceSum = 0
    purchaseList = []
    for card in cardList:
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
        purchaseList.append(card)
    if len(purchaseList) == 0:
        return 
    addCardsToCart(purchaseList)
    time.sleep(1)
    HttpHandler.checkout()
    clearSet()
    HttpHandler.clearShoppingCart()

ConfigHandler.initConfig()
ConfigHandler.displayConfig()
HttpHandler.login(ConfigHandler.RaiseUser, ConfigHandler.RaisePass)
MailHandler.init(ConfigHandler.GmailUser, ConfigHandler.GmailPass)

while True:
    process()
    time.sleep(5)

time.sleep(5)
HttpHandler.logout()
