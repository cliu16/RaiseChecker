
configFile="config.txt"
GiftCardName=""
PriceMin=100000
PercentMin=0
RaiseUser=""
RaisePass=""
GmailUser=""
GmailPass=""
MaxCardsPerOrder=0
MaxPricePerOrder=0
VisibleBrowser=True

def initConfig():
    with open(configFile) as f:
        contents = f.readlines()
        for content in contents:
            line = content.split(':')
            fillParams(line[0].strip(),line[1].strip())

def fillParams(key, val):
    global GiftCardName
    global PriceMin
    global PercentMin
    global RaiseUser
    global RaisePass
    global GmailUser
    global GmailPass
    global MaxCardsPerOrder
    global MaxPricePerOrder
    global VisibleBrowser
    
    if key == "Gift Card Name":
        GiftCardName=val
    elif key == "Price Min Per Card":
        PriceMin=float(val)
    elif key == "Percent Min Per Card":
        PercentMin=float(val)
    elif key == "Raise Username":
        RaiseUser=val
    elif key == "Raise Password":
        RaisePass=val
    elif key == "Gmail Username":
        GmailUser=val
    elif key == "Gmail Password":
        GmailPass=val
    elif key == "Max Cards Per Order":
        MaxCardsPerOrder=int(val)
    elif key == "Max Price Per Order":
        MaxPricePerOrder=float(val)
    elif key == "Visible Browser":
        if val.lower() == "false":
            VisibleBrowser=False
        else:
            VisibleBrowser=True

def displayConfig():
    ret = "Gift Card Name : " + str(GiftCardName) + "\n"
    ret += "Price Min Per Card: " + str(PriceMin) + "\n"
    ret += "Percent Min Per Card: " + str(PercentMin) + "\n"
    ret += "Raise Username : " + str(RaiseUser) + "\n"
    ret += "Raise Password : " + str(RaisePass) + "\n"
    ret += "Gmail Username : " + str(GmailUser) + "\n"
    ret += "Gmail Password : " + str(GmailPass) + "\n"
    ret += "Max Cards Per Order : " + str(MaxCardsPerOrder) + "\n"
    ret += "Max Price Per Order : " + str(MaxPricePerOrder) + "\n"
    ret += "Visible Browser : " + str(VisibleBrowser) + "\n"
    print ret
        
        
