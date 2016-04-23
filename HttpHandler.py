from selenium import webdriver
import time

current_url=""
driver=None

def login(user, password):
    global driver
    driver = webdriver.Firefox()
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
    login_btn.click()

def gotoPage(url):
    global current_url
    global driver
    if(current_url == url):
        return
    current_url = url
    driver.get(current_url)
    
def addToCartById(giftCardName, id):
    global driver
    #Add to cart
    url='https://www.raise.com/buy-'+giftCardName+'-gift-cards'
    gotoPage(url)
    
    card_field = driver.find_element_by_xpath('//tr[@id="'+id+'"]')
    parsedCard = parseCardField(card_field)

    addToCart_btn = card_field.find_element_by_class_name("span2")
    addToCart_btn.find_element_by_name("commit").submit()
    
def checkout():
    global driver
    #Checkout
    url = "https://www.raise.com/cart"
    gotoPage(url)
    checkout_btn = driver.find_element_by_xpath('//a[@class="btn btn-primary btn-block btn-xlarge"]')
    checkout_btn.click()

def parseCardField(card_field):
    id = card_field.get_attribute("id")
    contentList = card_field.find_elements_by_class_name("right")

    if(len(contentList)!=3):
        return None
    listPrice = contentList[0].text
    percent = contentList[1].text
    finalPrice = contentList[2].text

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

def logout():
    global driver
    driver.close()
