# Remember to brew install chromedriver
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import openpyxl

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


main_url = input("Robot Events URL: ")
doc_name = "teams.xlsx"
driver = webdriver.Chrome()
driver.wait = WebDriverWait(driver, 5)
driver.get(main_url)
teams = '//*[@id="events_tab"]/li[9]/a'
teams = driver.find_element_by_link_text("Team List")
teams.click()
html = driver.page_source
soup = BeautifulSoup(html)

all_trs = soup.find_all("tbody")
tr1 = all_trs[1]
tds = tr1.find_all("td")
teams = []

for td in range(len(tds)):
    if td % 4 == 0 or td == 0:
        teams.append(strip_tags(str(tds[td])))
#teamname
names = []
for td in range(len(tds)):
    if td % 4 == 1 or td == 1:
        names.append(strip_tags(str(tds[td])))
#Organization
organizations = []
for td in range(len(tds)):
    if td % 4 == 2 or td == 2:
        organizations.append(strip_tags(str(tds[td])))

wb = openpyxl.load_workbook(doc_name)
sheet = wb.get_sheet_by_name('Sheet1')

a1 = sheet['A1']
sheet["A1"].value = "Team #"
sheet["B1"].value = "Team Name"
sheet["C1"].value = "Organization"
sheet["D1"].value = "Most Recent Competition"
sheet["E1"].value = "OPR"
sheet["F1"].value = "Rank"

sheet.column_dimensions['A'].width = 10
sheet.column_dimensions['B'].width = 20
sheet.column_dimensions['C'].width = 20
sheet.column_dimensions['D'].width = 20


for i in range(len(teams)):
    try:
        print("On team {0}.".format(str(i+1)))
        sheet['A'+str(i+2)].value = teams[i]
        sheet['B'+str(i+2)].value = names[i]
        sheet['C'+str(i+2)].value = organizations[i]
        print(teams[i])

        driver.get("https://vexdb.io/teams/view/"+teams[i]+"?t=rankings")
        '''html = driver.page_source
        soup = BeautifulSoup(html)
        tbody = soup.find_all("tbody")
        tbody = tbody[3]
        trs = tbody.find_all("tr")
        trs = trs[0]
        tds = trs.find_all("td")

        rank = tds[2]
        event = tds[1]
        opr = tds[7]

        sheet['E'+str(i+2)].value = strip_tags(str(rank))
        sheet['F'+str(i+2)].value = strip_tags(str(opr))
        sheet['D'+str(i+2)].value = strip_tags(str(event))'''

        rank = driver.find_elements_by_class_name('rank')
        rank = rank[1]
        rank = rank.text
        event = driver.find_elements_by_class_name('event')
        event = event[1]
        event = event.text
        opr = driver.find_elements_by_class_name('opr')
        opr = opr[1]
        opr = opr.text
        sheet['E'+str(i+2)].value = str(rank)
        sheet['F'+str(i+2)].value = str(opr)
        sheet['D'+str(i+2)].value = str(event)


    except:
        '''sheet['A'+str(i+2)].value = "New Team"
        sheet['B'+str(i+2)].value = "New Team"
        sheet['C'+str(i+2)].value = "New Team"'''
        sheet['D'+str(i+2)].value = "New Team"
        sheet['E'+str(i+2)].value = "New Team"
        sheet['F'+str(i+2)].value = "New Team"
        print("On team {0}, new team.".format(i))

wb.save(doc_name)

driver.close()
