from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.wait = WebDriverWait(driver, 5)


driver.get("https://vexdb.io/teams/view/5327B?t=rankings")
rank = driver.find_elements_by_class_name('rank')
rank = rank[1]
print(rank.text)

driver.close()
