from PIL import Image
from PIL.ExifTags import TAGS
from GPSPhoto import gpsphoto
import os
from geopy.geocoders import Nominatim

# writes to a temp file
def writeTemp(text):
    file1 = open("C:/Users/danw5/Documents/AnywhereHack/Temp/temp.txt","w") 
    file1.write(text) 
    file1.close() 

# reads from a temp file
def readTemp():
    file1 = open("C:/Users/danw5/Documents/AnywhereHack/Temp/temp.txt","r+")
    return file1.readline()

# Get the data from image file and return a dictionary
def gps(fileName):
    data = gpsphoto.getGPSData(getOutdoorImage(fileName))
    gpsData = str(data['Latitude']) + "," + str(data['Longitude'])
    writeTemp(gpsData)
    if "Latitude" in data:
        return gpsData
    else:
        return "No GPS Data"

# creates a friendly name from the time stamp to save all files in 
def friendlyName(data):
    time = data["emailReceivedTime"]
    return time.replace(':','')

# gets the location of the OCR image
def getOCRImage(fileName):
    folder = "C:/Users/danw5/Documents/AnywhereHack/Emails/"
    folder += fileName
    file = folder + "/" + os.listdir(folder)[0]
    return file

# gets order id value from ocr output
def findOrderId(ocrText):
    ocrText = ocrText.upper()
    index = ocrText.find("ID:")

    foundInt = False
    intValue = ""
    
    while True:
        
        if index == len(ocrText):
            if foundInt == True:
                return intValue
            else:
                return "-1"
            
        if ocrText[index].isdigit():
            foundInt = True
            intValue += ocrText[index]
            
        elif foundInt == True:
            break
        
        
        
        index += 1
    return intValue

# gets the location of the outdoor image
def getOutdoorImage(fileName):
    folder = "C:/Users/danw5/Documents/AnywhereHack/Emails/"
    folder += fileName
    file = folder + "/" + os.listdir(folder)[1]
    return file

# verifies the address against google geolocator
def verifyAddress(address):
    gps = readTemp()
    gpsValues = gps.split(",")

    geolocator = Nominatim(user_agent="googlvev3")
    location = geolocator.geocode(address[1])

    if abs(float(location.latitude) - float(gpsValues[0])) < 1 and abs(float(location.longitude) - float(gpsValues[1])) < 1:
        return "True"
    else:
        return "False"



