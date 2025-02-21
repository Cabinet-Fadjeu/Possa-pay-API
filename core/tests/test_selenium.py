import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

@pytest.fixture
def browser():
    """Fixture pour initialiser et fermer Selenium WebDriver"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)  # Attendre 5 sec avant de lever une erreur
    yield driver
    # driver.quit()

# def test_homepage_title(browser):
#     """Test si la page d'accueil a le bon titre"""
#     browser.get("http://127.0.0.1:8000/")  # Ouvrir la page d'accueil
#     assert "Api de Paiement" in browser.title  # Vérifier le titre de la page


def test_register_user(browser):
    """Test d'inscription d'un utilisateur"""
    browser.get("http://127.0.0.1:8000/")  # URL de l'inscription

    browser.find_element(By.CLASS_NAME, "button").click()

    browser.find_element(By.ID, "signup").click()

    # Remplir le formulaire d'inscription
    browser.find_element(By.NAME, "username").send_keys("testuser1")
    browser.find_element(By.NAME, "email").send_keys("test1@example.com")
    browser.find_element(By.NAME, "phone_number").send_keys("650065034")
    browser.find_element(By.NAME, "password1").send_keys("Test@12345")
    browser.find_element(By.NAME, "password2").send_keys("Test@12345")

    # Soumettre le formulaire
    browser.find_element(By.NAME, "signup").click()
    time.sleep(2)

    assert "Votre compte a été créé avec succès." in browser.page_source  # Adapter selon ton site

    #definire le code secret
    browser.find_element(By.NAME, "code_secret").send_keys("12345")
    browser.find_element(By.CLASS_NAME, "button").click()

    time.sleep(2)

    # Vérifier si on est redirigé vers la page d'accueil après l'inscription
    assert "Code secret enregistré avec succès" in browser.page_source  # Adapter selon ton site

# def test_login_user(browser):
#     """Test de connexion d'un utilisateur"""
#     browser.get("http://127.0.0.1:8000/")  # URL de connexion
#     browser.find_element(By.CLASS_NAME, "button").click()

#     # Remplir le formulaire de connexion
#     browser.find_element(By.NAME, "email").send_keys("test1@example.com")
#     browser.find_element(By.NAME, "password").send_keys("Test@12345")

#     # Soumettre le formulaire
#     browser.find_element(By.NAME, "signup").click()
#     time.sleep(2)

#     # Vérifier si l'utilisateur est connecté (ex: présence du bouton "Déconnexion")
#     assert "Se deconnecter" in browser.page_source  # Adapter selon ton site
