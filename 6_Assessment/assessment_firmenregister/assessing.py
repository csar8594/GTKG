import json
import random
import re

import numpy
import numpy as np
import pgeocode
import phonenumbers
import requests
import validators
from email_validator import validate_email, EmailNotValidError
from tqdm import tqdm


def loadJSONintoArray():
    '''
    this function loads the json file and appends every line as numpy array to a list

    :return: list containing arrays - one array per hotel
    '''
    f = open('firmenregister.json')
    jsonData = json.load(f)

    hotelList = []

    for i in jsonData:
        l = list(i.items())
        arr = np.array(l)
        hotelList.append(arr)

    f.close()

    return hotelList


def getRandomHotels(hotelArr):
    '''
    this function gets random indices to 10% of all hotels in the hotelArr list

    :param hotelArr: the list containing all the hotel arrays
    :return: list containing random indices
    '''
    min = 0
    max = int(len(hotelArr) * 0.10)
    length = len(hotelArr)

    randIndex = random.sample(range(min, length), max)

    return randIndex


def getSubHotelArr(hotelArr, indices):
    '''
    this function gets the hotels from the indices and returns this sub list

    :param hotelArr: the list containing all hotel arrays
    :param indices: the random indices
    :return: list containing all hotels at the random indices positions
    '''
    hotelArrSub = []

    for i in range(0, len(hotelArr)):
        if i in indices:
            hotelArrSub.append(hotelArr[i])

    return hotelArrSub


def getInstanceCompleteness(hotelArrSub):
    '''
    this function calculates how many hotels actually have all 4 mandatory properties

    :param hotelArrSub: the list containing 10% of hotels
    :return: number of hotels having all 4 mandatory properties
    '''
    globalCounter = 0

    for hotel in hotelArrSub:
        localCounter = 0
        col = hotel[:, 0]

        if 'Firmenname' in col:
            localCounter += 1
        if 'Telefon' or 'Mobil' in col:
            localCounter += 1
        if 'E-Mail' in col:
            localCounter += 1
        if 'Adresse' or 'PLZ' or 'Ort' or 'Bundesland' in col:
            localCounter += 1

        if localCounter == 4:
            globalCounter += 1

    return globalCounter


def getPopulationCompletenes(hotelArr):
    '''
    this function returns the total number of hotels listed by firmenregister.de

    :param hotelArr: list containing all hotels
    :return: total number of hotels listed by firmenregister.de
    '''
    return len(hotelArr)


def urlChecker(url):
    '''
    this function checks if an url is reachable or not

    :param url: the url to be checked
    :return: true or false
    '''
    try:
        get = requests.get(url)
        if get.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def semPostalCode(postalCode):
    '''
    this fucntion checks if a postal code is a valid postal code in Germany

    :param postalCode:the postal code to be checked
    :return: true or false
    '''
    ret = False
    nomi = pgeocode.Nominatim('de')
    countrydata = nomi.query_postal_code(postalCode)

    if countrydata[1] == 'DE':
        ret = True

    return ret


def semTelephone(phoneNumber):
    '''
    this function checks if a phone number is a valid phone number in Germany

    :param phoneNumber: the phone number to be checked
    :return: true or false
    '''
    numGer = phonenumbers.parse(phoneNumber, "DE")
    formattedNum = phonenumbers.format_number(numGer, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    parsedNum = phonenumbers.parse(formattedNum, None)
    ret = phonenumbers.is_valid_number(parsedNum)

    return ret


def semFax(faxNumber):
    '''
    this function checks if a fax number is a valid fax number in Germany

    :param faxNumber: the fax number to be checked
    :return: true or false
    '''
    numGer = phonenumbers.parse(faxNumber, "DE")
    formattedNum = phonenumbers.format_number(numGer, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    parsedNum = phonenumbers.parse(formattedNum, None)
    ret = phonenumbers.is_valid_number(parsedNum)

    return ret


def semMail(email):
    '''
    this function checks if an email is a valid email

    :param email: the email to be checked
    :return: true or false
    '''
    ret = True
    try:
        validate_email(email).email
    except EmailNotValidError as e:
        ret = False

    return ret


def semWebsite(website):
    '''
    this function checks if a website is a valid website using a validator if a url is valid and
    also if the site is reachable using the urlChecker

    :param website: the website to be checked
    :return: true ot false
    '''
    ret = False
    valid = validators.url(website)
    if valid == True:
        ret = urlChecker(website)

    return ret


def semStreet(street):
    '''
    this function checks if a street name is valid using a regex (containing letters, numbers, dots, etc.)

    :param street: the street name and number to be checked
    :return: true or false
    '''
    ret = False

    m = re.match(
        "^(?:[A-Z] \d|[^\W\d_]{2,}\.?)(?:[- '][^\W\d_]+\.?)*\s+[1-9]\d{0,3} ?[a-zA-Z]?(?: ?[/-] ?[1-9]\d{0,3} ?[a-zA-Z]?)?$",
        street)

    if m:
        ret = True

    return ret


def semValid(hotelArrSub):
    '''
    this function combines all semantic check functions from above checks if a single hotel instance is valid or not
    only valid if all are valid

    :param hotelArrSub: list containing all hotel arrays
    :return: number showing how many hotels are semantically valid
    '''
    globalCounter = 0

    for hotel in tqdm(hotelArrSub):
        localBool = []
        for line in hotel:
            if line[0] == 'PLZ':
                localBool.append(semPostalCode(line[1]))
                # print("PLZ", semPostalCode(line[1]))
            if line[0] == 'Telefon':
                localBool.append(semTelephone(line[1]))
                # print("Telefon", semTelephone(line[1]))
            if line[0] == 'Fax':
                localBool.append(semFax(line[1]))
                # print("Fax", semFax(line[1]))
            if line[0] == 'E-Mail':
                localBool.append(semMail(line[1]))
                # print("E-Mail", semMail(line[1]))
            if line[0] == 'Homepage':
                localBool.append(semWebsite(line[1]))
                # print("Homepage", semWebsite(line[1]))
            if line[0] == 'Adresse':
                localBool.append(semStreet(line[1]))
                # print("Adresse", semStreet(line[1]))

        if all(localBool) == True:
            globalCounter += 1

    return globalCounter


def synPostalCode(postalCode):
    '''
    this function checks if a postal code is numeric/a number

    :param postalCode: the postal code to be checked
    :return: true or false
    '''
    ret = False

    if postalCode.isnumeric():
        ret = True

    return ret


def synTelephone(phoneNumber):
    '''
    this function checks if a phone number is numeric or has a + or a space

    :param phoneNumber: the phone number to be checked
    :return: true or false
    '''
    ret = False

    for element in phoneNumber:
        if element.isnumeric() or element == ' ' or element == '+':
            ret = True
        else:
            ret = False
            break

    return ret


def synFax(faxNumber):
    '''
    this function checks if a fux number is numeric or has a + or space

    :param faxNumber: the fax number to be checked
    :return: true or false
    '''
    ret = False

    for element in faxNumber:
        if element.isnumeric() or element == ' ' or element == '+':
            ret = True
        else:
            ret = False
            break

    return ret


def synMail(email):
    '''
    this function checks if an email is a string

    :param email: the email address to be checked
    :return: true or false
    '''
    ret = False

    if type(email) == numpy.str_:
        ret = True

    return ret


def synWebsite(website):
    '''
    this function checks if a website isa string

    :param website: the website to be checked
    :return: true or false
    '''
    ret = False

    if type(website) == numpy.str_:
        ret = True

    return ret


def synStreet(street):
    '''
    this function checks if a street name is valid

    :param street: the street to be checked
    :return: true or false
    '''
    ret = False

    if type(street) == numpy.str_:
        ret = True

    return ret


def synValid(hotelArrSub):
    '''
    this function combines all syntactic check functions from above checks if a single hotel instance is valid or not
    only valid if all are valid

    :param hotelArrSub: list containing all hotel arrays
    :return: number showing how many hotels are syntactically valid
    '''
    globalCounter = 0

    for hotel in tqdm(hotelArrSub):
        localBool = []
        for line in hotel:
            if line[0] == 'PLZ':
                localBool.append(synPostalCode(line[1]))
                # print("PLZ", semPostalCode(line[1]))
            if line[0] == 'Telefon':
                localBool.append(synTelephone(line[1]))
                # print("Telefon", semTelephone(line[1]))
            if line[0] == 'Fax':
                localBool.append(synFax(line[1]))
                # print("Fax", semFax(line[1]))
            if line[0] == 'E-Mail':
                localBool.append(synMail(line[1]))
                # print("E-Mail", semMail(line[1]))
            if line[0] == 'Homepage':
                localBool.append(synWebsite(line[1]))
                # print("Homepage", semWebsite(line[1]))
            if line[0] == 'Adresse':
                localBool.append(synStreet(line[1]))
                # print("Adresse", semStreet(line[1]))

        if all(localBool) == True:
            globalCounter += 1

    return globalCounter


def main():
    '''
    main function calling all functions and showing results

    :return: None
    '''
    hotelArr = loadJSONintoArray()
    randIndex = getRandomHotels(hotelArr)
    hotelArrSub = getSubHotelArr(hotelArr, randIndex)

    instaceCompleteness = getInstanceCompleteness(hotelArrSub)
    print(str(instaceCompleteness) + " out of " + str(len(hotelArrSub)) + " hotel(s) have all 4 mandatory properties")

    populationCompleteness = getPopulationCompletenes(hotelArr)
    print("firmenregister.de has " + str(populationCompleteness) + " hotels -- GTKG has 259")

    semValidity = semValid(hotelArrSub)
    print(str(semValidity) + " out of " + str(len(hotelArrSub)) + " hotel(s) follow semantic validity")

    synValidity = synValid(hotelArrSub)
    print(str(synValidity) + " out of " + str(len(hotelArrSub)) + " hotel(s) follow syntactic validity")


if __name__ == '__main__':
    main()
