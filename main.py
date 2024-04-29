from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json
import csv

options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

driver.get("https://sitval.com/#/cita_previa")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/app-root/itv-alertas/p-dialog/div/div/div[4]/p-footer/button"))
).click()

headers = driver.find_elements(By.CSS_SELECTOR, "span.p-tabview-title")
header_valencia = None

for header in headers:
    if header.text == "València":
        header_valencia = header
        break

header_valencia.click()

time.sleep(1)

localidadesList = driver.find_element(By.XPATH, "/html/body/app-root/div/div/div/itv-cita-previa/div/div/div[2]/itv-select-localidad/div/div/p-tabview/div/div[2]/p-tabpanel[3]/div/div[1]")

localidades = localidadesList.find_elements(By.CSS_SELECTOR, "button.localidad")

for localidad in localidades:
    if localidad.text == "Riba-roja de Túria":
        localidad.click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control"))
        ).send_keys("1234GPT")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "#topDiv > div > div:nth-child(2) > itv-select-vehiculo > div.row.text-center > div > div:nth-child(1) > div > span.desc-vehiculo").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/div/div/itv-cita-previa/p-dialog[1]/div/div/div[3]/div/div[1]/div"))
        ).click()
        time.sleep(1)
        listaMeses = driver.find_element(By.CSS_SELECTOR, "#topDiv > div > div:nth-child(2) > itv-select-cita > div > div > div:nth-child(1) > div > ul")
        meses = listaMeses.find_elements(By.TAG_NAME, "a")
        for mes in meses:
            mes.click()
            nohaycita = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/div/div/itv-cita-previa/div/div/div[2]/itv-select-cita/div/div/div[2]/div/div[1]"))
            ) 
            if nohaycita.text.strip() == "SIN TURNOS DISPONIBLES":
                print(f"No hay citas en {mes.text}")
            else:
                print(f"Hay citas en {mes.text}")
                
            
        time.sleep(2)
        break





time.sleep(5)
driver.quit()
