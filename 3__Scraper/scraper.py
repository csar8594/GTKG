import csv
import os
import random
import re

import numpy as np
import phonenumbers
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm


def logToFile(url, prox):
    '''
    this function writes the proxy server which has crawled a specific website to a csv file log.csv in order to
    know how the request proxy changes

    @param url: the website url that gets written to csv file
    @param prox: the proxy url that gets written to csv file
    @return: None
    '''
    row = [prox, url]
    with open('log.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def getHTMLSource(siteUrl):
    '''
    this function uses a random proxy server from https://geonode.com/free-proxy-list/ and loads the source code
    of this site using BeautifulSoup and logs the request into a csv file

    @param siteUrl: the URL from where BeautifulSoup loads the source complete source code
    @return: source code
    '''
    proxiesList = [
        "85.25.108.234:5566",
        "85.25.91.155:5566",
        "167.172.178.193:46105",
        "85.25.150.32:5566",
        "138.201.125.229:8118",
        "147.135.255.62:8129",
        "147.135.255.62:8139",
        "167.172.173.210:39403",
        "216.169.73.65:34679",
        "85.25.91.155:5566",
        "78.47.227.89:8118",
        "151.80.136.138:3128",
        "62.75.229.77:5566",
        "157.230.233.189:3008",
        "20.47.108.204:8888"
    ]

    # if the request fails to get an answer (e.g. timeout) then the request gets sent again
    # for a total of 5 times
    retryStrategy = Retry(
        total=5,
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retryStrategy)
    http = requests.Session()
    http.mount(siteUrl, adapter)

    prox = random.choice(proxiesList)
    proxies = {'https': prox}

    # reduce the request rate in order to prevent server failure
    # time.sleep(2)

    f = http.get(siteUrl, proxies=proxies)
    soup = BeautifulSoup(f.content, 'lxml')

    logToFile(siteUrl, prox)

    return soup


def filterPagesUrl(soup):
    '''
    this function uses a regex to find the URLs of a given source code which links to all the other websites listing
    hotels

    therefore a regex is used and the "amp" string including spaces at beginning and end of url get removed

    @param soup: HTML source code of the original URL
    @return: URL that links to all the other n websites
    '''
    regex = r'\"register\.php\?cmd=mysearch&amp;fr=\w*&amp;auswahl=alle&amp;ap=\d+"'
    matches = re.findall(regex, str(soup))
    pagesURL = (matches[0].replace("amp;", "").replace("\"", ""))[:-1]

    return pagesURL


def getPages(soup):
    '''
    this function uses the same regex but this time the goal is to grab the minimum and maximum page number

    @param soup: HTML source code of the original URL
    @return: list of all pages beginning at min to max
    '''
    regex = r'\"register\.php\?cmd=mysearch&amp;fr=\w*&amp;auswahl=alle&amp;ap=\d+"'
    matches = re.findall(regex, str(soup))

    pagesList = []

    # find the indices of a page-number in every URL that links to a new page and append these to a list
    # remove the duplicates from the list and search for the minimum and maximum value
    for line in matches:
        regex = "&amp;ap="
        index1 = line.find(regex) + len(regex)  # start index (=0)
        index2 = len(line) - 1  # end index (=n)
        pageNum = line[index1:index2]
        pagesList.append(int(pageNum))

    pagesList = list(dict.fromkeys(pagesList))
    pageMin = min(pagesList)
    pageMax = max(pagesList)

    return list(range(pageMin, pageMax + 1))


def filterHotelUrl(soup):
    '''
    this function filters all the hotel URLs per site listing hotels by using a regex and replacing the
    "amp" string

    @param soup: HTML source of every site website listing hotels
    @return: a list of hotel links per website listing hotels
    '''
    txt = soup.findAll('tr', {'valign': 'top'})
    regex = r'\"register.php\?cmd=anzeige&amp;fr=\w*&amp;auswahl=alle&amp;ap=\d+&amp;eid=\d+"'

    matches = re.findall(regex, str(txt))
    hotelLinks = list({x.replace("amp;", "").replace("\"", "") for x in matches})

    return hotelLinks


def getAllHotelURL(pageurl, pageslist):
    '''
    this function gets all the hotel URLs which represent per hotel information using the filerHotelUrl
    function in a loop

    @param pageurl: the url of the hotel site
    @param pageslist: the list containing all page URLs
    @return: list containing all hotel page URLs
    '''
    allHotelURLList = []

    print("Scraping all " + str(len(pageslist)) + " websites containing hotels:")
    for page in tqdm(pageslist):
        url = "http://firmenregister.de/" + str(pageurl) + str(page)
        soup = getHTMLSource(url)

        allHotelURLList += filterHotelUrl(soup)

    return allHotelURLList


def getHotelInfo(hotelURL):
    '''
    this function loads all the hotel info of a single hotel

    @param hotelURL: the URL represent a specific hotel's information
    @return: 2D array containing the hotel info
    '''
    escapes = ''.join([chr(char) for char in range(7, 15)])
    translator = str.maketrans('', '', escapes)

    url = "http://firmenregister.de/" + str(hotelURL)
    soup = getHTMLSource(url)

    # grab data until "Branchen" and replace non standard characters in every line and replace double spaces
    hoteldata = []
    for td_tag in soup.find_all('td'):
        if 'Branchen' in td_tag.text:
            break
        if td_tag.text == "\xa0":
            hoteldata.append('')
        else:
            tmp = re.sub(r'[^\x00-\x7F\xe4\xc4\xdc\xfc\xf6\xd6\xdf]+', ' ',
                         (td_tag.text.replace('\xa0', ' ').replace('  ', ' ')).strip())
            hoteldata.append(tmp.translate(translator))

    # remove first empty string if available in case firmenregister.de shows a hotel logo
    if hoteldata[0] == '':
        del hoteldata[0]

    # remove space in case of "Produkte/Infos" and format PLZ and Ort as separate elements
    # format Telefon, Fax and Mobil number in an international format using +49 and two spaces inbetween the
    # country code and prefix and prefix and number respectively
    for element in hoteldata:
        index = hoteldata.index(element)
        if element == 'Produkte / Infos':
            hoteldata[index] = element.replace(' ', '')
        if element == 'PLZ / Ort':
            if hoteldata[index + 1].isnumeric():
                hoteldata[index] = 'PLZ'
            elif hoteldata[index + 1].isalpha():
                hoteldata[index] = 'Ort'
            else:
                tmp = hoteldata[index + 1].split(' ', 1)
                hoteldata[index] = 'PLZ'
                hoteldata.insert(index + 1, tmp[0])
                hoteldata.insert(index + 2, 'Ort')
                hoteldata[index + 3] = tmp[1]
        if (element == 'Telefon' or element == 'Fax' or element == 'Mobil'):
            if hoteldata[index]:
                if '-' in hoteldata[index + 1]:
                    numStr = hoteldata[index + 1].replace('-', '').replace('  ', '').replace(' ', '')
                    try:
                        numGer = phonenumbers.parse(numStr, "DE")
                        formattedNum = phonenumbers.format_number(numGer,phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                        hoteldata[index + 1] = formattedNum
                    except:
                        hoteldata[index + 1] = numStr

    # covert to 2D array with 2 elements per row and remove rows where there is no element in the corresponding
    # field in the right column
    hotelArray = np.array(hoteldata).reshape(-1, 2)
    mask = np.where(hotelArray == '')[0]
    hotelArray = np.delete(hotelArray, mask, axis=0)

    return hotelArray


def convertToJsonFile(hotelArrayList):
    '''
    this function takes the list containing all the hotel arrays into a string formatted in json and writes it to
    a json file hotel after hotel

    @param hotelArrayList: list containing all the hotel arrays
    @return: None
    '''
    f = open("firmenregister.json", "a")

    f.write("[\n")

    for arr in tqdm(hotelArrayList):
        if not np.array_equal(arr, hotelArrayList[len(hotelArrayList) - 1]):
            strToWrite = "\t{\n"
            for line in arr:
                if line[1].isnumeric():
                    strToWrite += "\t\t\"" + line[0] + "\": " + line[1] + ",\n"
                else:
                    strToWrite += "\t\t\"" + line[0] + "\": \"" + line[1] + "\",\n"

            f.write(strToWrite[:-2])
            f.write("\n\t},\n")
        else:
            strToWrite = "\t{\n"
            for line in arr:
                if line[1].isnumeric():
                    strToWrite += "\t\t\"" + line[0] + "\": " + line[1] + ",\n"
                else:
                    strToWrite += "\t\t\"" + line[0] + "\": \"" + line[1] + "\",\n"

            f.write(strToWrite[:-2])
            f.write("\n\t}\n]")

    f.close()


def main():
    # install all requirements
    os.system('pip install -r requirements.txt')

    print("\n\nStarting scraper ....")

    startUrl = "http://www.firmenregister.de/register.php?cmd=search&stichwort=&firma=&branche=Hotels%2C+Gasth%E4user+und+Pensionen&vonplz=&ort=&strasse=&vorwahl=&bundesland=alle&Suchen=Suchen"

    # get first html source and grab the page url and all page numbers
    soup = getHTMLSource(startUrl)
    pageurl = filterPagesUrl(soup)
    pagesList = getPages(soup)

    # get hotel urls from all pages
    allHotelURLList = getAllHotelURL(pageurl, pagesList)

    # get all the info from every hotel
    hotelArrayList = []
    print("Scraping information of all " + str(len(allHotelURLList)) + " hotels:")
    for hotelUrl in tqdm(allHotelURLList):
        hotelArrayList.append(getHotelInfo(hotelUrl))

    # convert hotelArraylist to json
    print("Writing " + str(len(hotelArrayList)) + " hotels to firmenregister.json")
    convertToJsonFile(hotelArrayList)


if __name__ == '__main__':
    main()
