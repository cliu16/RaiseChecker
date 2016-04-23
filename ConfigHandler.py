
configFile="config.txt"
GiftCardName=""
PriceMin=100000
PercentMin=0
RaiseUser=""
RaisePass=""
GmailUser=""
GmailPass=""

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
    
    if key == "Gift Card Name":
        GiftCardName=val
    elif key == "Price Min":
        PriceMin=val
    elif key == "Percent Min":
        PercentMin=val
    elif key == "Raise Username":
        RaiseUser=val
    elif key == "Raise Password":
        RaisePass=val
    elif key == "Gmail Username":
        GmailUser=val
    elif key == "Gmail Password":
        GmailPass=val

def displayConfig():
    ret = "Gift Card Name : " + str(GiftCardName) + "\n"
    ret += "Price Min : " + str(PriceMin) + "\n"
    ret += "Percent Min : " + str(PercentMin) + "\n"
    ret += "Raise Username : " + str(RaiseUser) + "\n"
    ret += "Raise Password : " + str(RaisePass) + "\n"
    ret += "Gmail Username : " + str(GmailUser) + "\n"
    ret += "Gmail Password : " + str(GmailPass) + "\n"
    print ret
        
        
