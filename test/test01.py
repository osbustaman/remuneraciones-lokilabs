import time

# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils import obtener_nombre_aleatorio, obtener_rut_aleatorio


driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager(path=r".\\Drivers").install()))



driver.get("http://localhost:8080/")

title = driver.title

userName = driver.find_element(by=By.XPATH, value="//*[@id='id_username']")
userName.send_keys("osbustaman")
time.sleep(1)

password = driver.find_element(by=By.XPATH, value="//*[@id='id_password']")
password.send_keys("OAbn_3004")
time.sleep(1)

submitForm = driver.find_element(
    by=By.XPATH, value="/html/body/div/div/div/section/form/div[3]/input")
submitForm.click()
time.sleep(1)

sidebar_client = driver.find_element(
    by=By.XPATH, value="//*[@id='sidebar-menu']/div/ul/li[2]/a")
sidebar_client.click()
time.sleep(1)

a_list_client = driver.find_element(
    by=By.XPATH, value="//*[@id='sidebar-menu']/div/ul/li[2]/ul/li/a")
a_list_client.click()
time.sleep(1)

new_client = driver.find_element(
    by=By.XPATH, value="/html/body/div/div/div[3]/div/div/div[3]/div/div/div[1]/ul/li/button")
new_client.click()
time.sleep(1)

# Llenado del formulario
name_client = driver.find_element(
    by=By.XPATH, value='//*[@id="id_nombre_cliente"]')
name_client.send_keys(obtener_nombre_aleatorio())
time.sleep(1)

active_client = driver.find_element(
    by=By.XPATH, value='//*[@id="id_cliente_activo"]')
active_client.send_keys("N")
time.sleep(1)

cant_user = driver.find_element(
    by=By.XPATH, value='//*[@id="id_cantidad_usuarios"]')
cant_user.send_keys("10")
time.sleep(1)

dni_user = driver.find_element(by=By.XPATH, value='//*[@id="id_rut_cliente"]')
dni_user.send_keys(obtener_rut_aleatorio())
time.sleep(1)

date_admission = driver.find_element(
    by=By.XPATH, value='//*[@id="id_fecha_ingreso"]')
date_one = "12/06/2023"
driver.execute_script(
    "arguments[0].value = arguments[1]", date_admission, date_one)
time.sleep(1)

representative_name = driver.find_element(
    by=By.XPATH, value='//*[@id="id_nombre_representante"]')
representative_name.send_keys(obtener_nombre_aleatorio())
time.sleep(10)

file_input = driver.find_element(
    by=By.XPATH, value='//*[@id="id_imagen_cliente"]')
# Ruta al archivo que se va a subir
archivo = '/Users/osbustaman/sistemas-lokilabs/remuneraciones-lokilabs/test/imagen_test.png'
file_input.send_keys(archivo)
time.sleep(1)

date_finish = driver.find_element(
    by=By.XPATH, value='//*[@id="id_fecha_termino"]')
date_two = "12/07/2023"
driver.execute_script(
    "arguments[0].value = arguments[1]", date_finish, date_two)
time.sleep(1)

id_rut_representante = driver.find_element(
    by=By.XPATH, value='//*[@id="id_rut_representante"]')
id_rut_representante.send_keys(obtener_rut_aleatorio())
time.sleep(1)

id_correo_representante = driver.find_element(
    by=By.XPATH, value='//*[@id="id_correo_representante"]')
id_correo_representante.send_keys("homero@mail.cl")
time.sleep(1)

id_telefono_representante = driver.find_element(
    by=By.XPATH, value='//*[@id="id_telefono_representante"]')
id_telefono_representante.send_keys("56987824323")
time.sleep(1)

id_direccion_representante = driver.find_element(
    by=By.XPATH, value='//*[@id="id_direccion_representante"]')
id_direccion_representante.send_keys("lourdes 1012")
time.sleep(1)

"""id_pais = driver.find_element(by=By.XPATH, value='//*[@id="id_pais"]')
id_pais.send_keys("1")
time.sleep(1)

id_region = driver.find_element(by=By.XPATH, value='//*[@id="id_region"]')
id_region.send_keys("6")
time.sleep(1)

id_comuna = driver.find_element(by=By.XPATH, value='//*[@id="id_comuna"]')
id_comuna.send_keys("106")
time.sleep(10)"""

btn_add_client = driver.find_element(
    by=By.XPATH, value="/html/body/div/div/div[3]/div/div/div[3]/div/div/div[1]/ul/li/button[1]")
btn_add_client.click()

time.sleep(10)

driver.close()