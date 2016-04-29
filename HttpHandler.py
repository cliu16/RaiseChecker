from selenium import webdriver
import time
from dateutil.parser import parse

driver=None

def login(user, password, visible):
    global driver
    if visible == True:
        driver = webdriver.Firefox()
    else:
        driver = webdriver.PhantomJS()
    login_url = "https://www.raise.com/user/sign_in"
    gotoPage(login_url)
    email_field = driver.find_element_by_xpath('//input[@id="user_email"]')
    email_field.clear()
    email_field.send_keys(user)
    showHide_btn = driver.find_element_by_xpath('//a[@id="toggle_password_btn"]')
    showHide_btn.click()
    password_field = driver.find_element_by_xpath('//input[@id="user_password"]')
    password_field.clear()
    password_field.send_keys(password)
    login_btn = driver.find_element_by_xpath('//input[@name="commit"]')
    time.sleep(1)
    login_btn.click()
    time.sleep(1)

def gotoPage(url):
    global driver
    if(driver.current_url == url):
        return
    driver.get(url)
    time.sleep(1)
    
def addToCartById(giftCardName, id):
    global driver
    #Add to cart
    url='https://www.raise.com/buy-'+giftCardName+'-gift-cards'
    gotoPage(url)
    
    card_field = driver.find_element_by_xpath('//tr[@id="'+id+'"]')
    parsedCard = parseCardField(card_field)

    addToCart_btn = card_field.find_element_by_class_name("span2")
    addToCart_btn.find_element_by_name("commit").submit()

def getCartInfo():
    global driver
    url = "https://www.raise.com/cart"
    gotoPage(url)
    totalPrice_field = None
    try:
        totalPrice_field = driver.find_element_by_xpath('//tr[@class="summary"]')
    except:
        return {"count":0,"totalPrice":0}
    
    t = totalPrice_field.find_element_by_class_name("right").text.replace(',','')
    countCards_field = driver.find_element_by_xpath('//div[@class="span8 content left"]').find_element_by_tag_name('h2')
    c = countCards_field.text.split(' ')[0]
    return {"count":int(c),"totalPrice":float(t[1:])}
    
def checkout():
    global driver
    #Checkout
    url = "https://www.raise.com/cart"
    gotoPage(url)
    checkout_btn = driver.find_element_by_xpath('//a[@class="btn btn-primary btn-block btn-xlarge"]')
    checkout_btn.click()
    time.sleep(2)
    try:
        checkout_btn = driver.find_element_by_xpath('//a[@class="btn btn-primary btn-block btn-xlarge"]')
    except:
        return False
    raw_input("Press Enter to Pay!!!")
    checkout_btn.click()
    time.sleep(2)
    return True

def verifyDevice():
    global driver
    email_btn = driver.find_element_by_xpath('//a[@class="btn btn-action phone-verification-option device-verification-delivery"]')
    email_btn.click()
    code = raw_input("Type the verification code:\n")
    print 'Code entered is : ' + code
    code_field = driver.find_element_by_xpath('//input[@id="device_verification_code"]')
    code_field.clear()
    code_field.send_keys(code)
    verify_btn = driver.find_element_by_xpath('//input[@name="commit"]')
    verify_btn.submit()

def clearShoppingCart():
    global driver
    url = "https://www.raise.com/cart"
    gotoPage(url)
    remove_btn_list = driver.find_elements_by_xpath('//input[@name="commit"]')
    for x in range(0, len(remove_btn_list)):
        remove_btn = driver.find_element_by_xpath('//input[@name="commit"]')
        remove_btn.submit()
        
def parseCardField(card_field):
    id = card_field.get_attribute("id")
    contentList = card_field.find_elements_by_class_name("right")

    if(len(contentList)!=3):
        return None
    listPrice_text = contentList[0].text.strip()
    percent_text = contentList[1].text.strip()
    finalPrice_text = contentList[2].text[1:contentList[2].text.index('+')].strip()
    listPrice = float(listPrice_text[1:].replace(',',''))
    percent = float(percent_text[:-1].replace(',',''))
    finalPrice = float(finalPrice_text.replace(',',''))
    addToCart_btn = card_field.find_element_by_class_name("span2")
    addToCart_btn.find_element_by_name("commit")

    return {"id":id,"listPrice":listPrice,"percent":percent,"finalPrice":finalPrice,"addToCart_btn":addToCart_btn}

def getCardList(giftCardName):
    global driver
    ret=[]
    url='https://www.raise.com/buy-'+giftCardName+'-gift-cards'
    gotoPage(url)

    card_field_list = driver.find_elements_by_class_name("toggle-details")
    for card_field in card_field_list:
        parsedCard = parseCardField(card_field)
        ret.append(parsedCard)

    return ret

def getOrderList(raw):
    global driver
    wantedOrders = None
    startDate = None
    try:
        if '/' in raw:
            startDate = parse(raw)
            print "Look up all orders placed on/after date {}.".format(startDate)
        else:
            wantedOrders = int(raw)
            print "Look up recent {} orders.".format(wantedOrders)
    except:
        wantedOrders = 3
        print "Can't understand what you input. Just gonna fetch you recent {} orders.".format(wantedOrders)
    base_url = 'https://www.raise.com/my_orders?page={}' # + page number
    ret=[]
    page = 0
    while page < 2:
        page+=1
        url = base_url.format(page)
        gotoPage(url)
        order_list = driver.find_elements_by_tag_name("tr")
        for order in order_list:
            contentList = order.find_elements_by_tag_name("td")
            if not contentList:
                continue
            orderDate = contentList[0].text.strip()
            if startDate:
                if parse(orderDate) < startDate:
                    return ret
            elif wantedOrders:
                if len(ret) >= wantedOrders:
                    return ret
            orderNumber = contentList[1].text.strip()
            ret.append(orderNumber)
    return ret

def getOrder(orderNumber):
    global driver
    url = 'https://www.raise.com/my_orders/{}'.format(orderNumber)
    gotoPage(url)
    time.sleep(1)
    main_content = driver.find_element_by_tag_name('tbody')
    price_list = main_content.find_elements_by_class_name("right")
    code_list = main_content.find_elements_by_class_name("inspectlet-sensitive")
    for i in range(0,len(price_list)):
        print price_list[i].text.strip(), code_list[i].text.strip()

def logout():
    global driver
    driver.close()

