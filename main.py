from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
from dotenv import load_dotenv
from send_mail import send_mail

load_dotenv()

localidades_to_check = ["València (Campanar)", "Catarroja", "Riba-roja de Túria"]
localidades_disponibles = []

def hay_citas(municipio):
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

    # for localidad in localidades:
    #     print(localidad.text)

    for localidad in localidades:
        localidad_nombre = localidad.text
        if localidad.text == municipio:
            print(localidad.text)
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
                    print(f"No hay citas en {mes.text} en {localidad_nombre}")
                else:
                    print(f"Hay citas en {mes.text} en {localidad_nombre}")
                    localidades_disponibles.append("Hay citas en " + mes.text + " en " + localidad_nombre)
                
            break

    time.sleep(1)
    driver.quit()

for localidad in localidades_to_check:
    hay_citas(localidad)

print('-------------------Resultado:-------------------')
for localidad in localidades_disponibles:
    print(localidad)

if len(localidades_disponibles) > 0:
    send_mail(os.getenv("SENDER_EMAIL"), os.getenv("PASSMAIL"), os.getenv("RECEIVER_EMAIL"), "Citas disponibles", localidades_disponibles)