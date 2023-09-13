from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


def run_sheets():
    browser = webdriver.Firefox()
    browser.get("Google sheets link")
    # time.sleep(2)

    submitbutton = browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]/div[3]/div/div/div/a')
    submitbutton.click() 
    # time.sleep(3)

    textbox = browser.find_element(By.XPATH,'//*[@id="identifierId"]')
    textbox.send_keys("cs19b045@iittp.ac.in")
    # time.sleep(2)

    submitbutton = browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[3]')
    ActionChains(browser).move_to_element(submitbutton).click().perform()
    time.sleep(2)



    textbox = browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
    # time.sleep(2)

    submitbutton = browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[3]')
    ActionChains(browser).move_to_element(submitbutton).click().perform()
    time.sleep(10)


    submitbutton = browser.find_element(By.XPATH,'//*[@id="docs-extensions-menu"]')
    submitbutton.click() 
    time.sleep(5)
    submitbutton = browser.find_element(By.XPATH,'//*[@id="MAEPJr-hA4Zv3r19JF0IqQVDOcoke7-2l"]/div')
    submitbutton.click()
    # time.sleep(3)
    submitbutton = browser.find_element(By.XPATH,"//*[text()='Start Geocoding']")
    print(submitbutton)
    submitbutton.click() 
    time.sleep(10)

    iframe = browser.find_element(By.CSS_SELECTOR, ".script-application-sidebar-content > iframe:nth-child(1)")

    browser.switch_to.frame(iframe)

    iframe = browser.find_element(By.CSS_SELECTOR, "#sandboxFrame")

    browser.switch_to.frame(iframe)

    iframe = browser.find_element(By.CSS_SELECTOR, "#userHtmlFrame")

        # switch to selected iframe
    browser.switch_to.frame(iframe)

        # Now click on button
    # browser.find_element(By.TAG_NAME, 'button').click()
    submitbutton = browser.find_element(By.XPATH,"//*[text()='Geocode!']")
    submitbutton.click() 
    time.sleep(3)
    #browser.close()
    
# run_sheets()

