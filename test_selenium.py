import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

BASE_URL = "http://localhost:8000"  

@pytest.fixture(scope="module")
def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    screenshots_path = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshots_path, exist_ok=True)  # Crear carpeta para capturas de pantalla dentro de `tasks/test`
    driver.screenshots_path = screenshots_path  # Guardar la ruta en el driver
    yield driver
    driver.quit()

def test_registro_inicio_crear_tarea(setup_browser):
    driver = setup_browser

    # 1. Registro de un nuevo usuario
    driver.get(f"{BASE_URL}/signup/")  # URL de registro
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("usuario_prueba08")
    driver.find_element(By.NAME, "password1").send_keys("contraseña_segura123")
    driver.find_element(By.NAME, "password2").send_keys("contraseña_segura123")
    driver.save_screenshot(os.path.join(driver.screenshots_path, "registro_form.png"))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    driver.save_screenshot(os.path.join(driver.screenshots_path, "registro_resultado.png"))
    assert "Tareas Pendientes" in driver.page_source or "/tasks" in driver.current_url, "El registro no fue exitoso"

    # 2. Iniciar sesion
    driver.get(f"{BASE_URL}/login/")  # URL de inicio de sesion
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("usuario_prueba08")
    driver.find_element(By.NAME, "password").send_keys("contraseña_segura123")
    driver.save_screenshot(os.path.join(driver.screenshots_path, "login_form.png"))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    driver.save_screenshot(os.path.join(driver.screenshots_path, "login_resultado.png"))
    assert "Tareas Pendientes" in driver.page_source or "/tasks" in driver.current_url, "El inicio de sesión no fue exitoso"

    # 3. Crear una nueva tarea
    driver.get(f"{BASE_URL}/tasks/create/")  # URL del formulario de creacion de tareas
    time.sleep(1)
    driver.find_element(By.NAME, "title").send_keys("Tarea de prueba")
    driver.find_element(By.NAME, "description").send_keys("Descripción de la tarea de prueba.")
    driver.find_element(By.NAME, "important").click()  # Marcar como importante
    driver.save_screenshot(os.path.join(driver.screenshots_path, "crear_tarea_form.png"))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    driver.save_screenshot(os.path.join(driver.screenshots_path, "crear_tarea_resultado.png"))
    assert "Tarea de prueba" in driver.page_source, "No se pudo crear la tarea"