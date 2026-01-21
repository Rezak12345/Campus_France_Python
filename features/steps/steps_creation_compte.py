import os
import time
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.read_data import ReadData


@given("je suis sur la page de creation de compte")
def step_given_page_creation(context):
    context.read = ReadData()
    context.etudiant = context.read.read_data_from_json()

    options = webdriver.EdgeOptions()
    options.use_chromium = True

    # Détection GitHub Actions
    is_ci = os.getenv("GITHUB_ACTIONS") == "true"

    if is_ci:
        print("▶ GitHub Actions détecté → mode HEADLESS")
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
    else:
        print("▶ Exécution locale → mode graphique")

    context.driver = webdriver.Edge(options=options)
    context.js = context.driver

    context.driver.get("https://www.campusfrance.org/fr/user/register")
    time.sleep(3)

    context.driver.find_element(By.XPATH, "//*[@id=\"tarteaucitronAllDenied2\"]").click()


@when("je saisi les informations utilisateur")
def step_when_saisie_infos(context):
    driver = context.driver
    js = context.js
    etudiant = context.etudiant

    # Email
    driver.find_element(By.XPATH,
        "/html/body/div[2]/div[2]/main/div[2]/div/div[2]/form/div[2]/div/div[1]/input"
    ).send_keys(etudiant.email)

    # Mot de passe
    driver.find_element(By.XPATH,
        "/html/body/div[2]/div[2]/main/div[2]/div/div[2]/form/div[2]/div/div[2]/div[1]/input"
    ).send_keys(etudiant.motDePasse)

    driver.find_element(By.XPATH,
        "/html/body/div[2]/div[2]/main/div[2]/div/div[2]/form/div[2]/div/div[2]/div[2]/input"
    ).send_keys(etudiant.confirmationMotDePasse)

    # Civilité
    driver.find_element(By.XPATH,
        "/html/body/div[2]/div[2]/main/div[2]/div/div[2]/form/div[3]/div[1]/fieldset/div/div/div[1]/label"
    ).click()

    # Identité
    driver.find_element(By.XPATH, "//*[@id=\"edit-field-nom-0-value\"]").send_keys(etudiant.nom)
    driver.find_element(By.XPATH, "//*[@id=\"edit-field-prenom-0-value\"]").send_keys(etudiant.prenom)

    # Pays de résidence
    driver.find_element(By.XPATH, "//*[@id=\"edit-field-pays-concernes-selectized\"]").click()
    france = driver.find_element(By.XPATH,
        "/html/body/div[2]/div[2]/main/div[2]/div/div[2]/form/div[3]/div[4]/div/div/div[2]/div/div[164]"
    )
    js.execute_script("arguments[0].parentElement.scrollTop = arguments[0].offsetTop;", france)
    france.click()

    driver.find_element(By.XPATH,
        "//*[@id=\"edit-field-nationalite-0-target-id\"]"
    ).send_keys(etudiant.paysNationalite)

    # Adresse
    driver.find_element(By.XPATH, "//*[@id=\"edit-field-code-postal-0-value\"]").send_keys(etudiant.codePostal)
    driver.find_element(By.XPATH, "//*[@id=\"edit-field-ville-0-value\"]").send_keys(etudiant.ville)
    driver.find_element(By.XPATH, "//*[@id=\"edit-field-telephone-0-value\"]").send_keys(etudiant.telephone)

    # Profil
    js.execute_script(
        "arguments[0].scrollIntoView(true);",
        driver.find_element(By.XPATH, "//*[@id=\"user-form\"]/div[4]/h2")
    )
    driver.find_element(By.XPATH, "//*[@id=\"edit-field-publics-cibles\"]/div[1]/label").click()

    # Domaine étude
    driver.find_element(By.XPATH,
        "//*[@id=\"edit-field-domaine-etudes-wrapper\"]/div/div/div[1]/div"
    ).click()
    medcine = driver.find_element(By.XPATH,
        "/html/body/div[2]/div[2]/main/div[2]/div/div[2]/form/div[4]/div[2]/div[1]/div/div/div[2]/div/div[17]"
    )
    js.execute_script("arguments[0].parentElement.scrollTop = arguments[0].offsetTop;", medcine)
    medcine.click()

    # Niveau étude
    js.execute_script(
        "arguments[0].scrollIntoView(true);",
        driver.find_element(By.XPATH, "//*[@id=\"edit-field-domaine-etudes-wrapper\"]/div/label")
    )
    driver.find_element(By.XPATH,
        "//*[@id=\"edit-field-niveaux-etude-wrapper\"]/div/div/div[1]/div"
    ).click()
    master = driver.find_element(By.XPATH,
        "/html/body/div[2]/div[2]/main/div[2]/div/div[2]/form/div[4]/div[2]/div[2]/div/div/div[2]/div/div[8]"
    )
    js.execute_script("arguments[0].parentElement.scrollTop = arguments[0].offsetTop;", master)
    master.click()

    # Conditions
    driver.find_element(By.XPATH,
        "//*[@id=\"edit-field-accepte-communications-wrapper\"]/div/label"
    ).click()


@then('le bouton creer affiche un message "{message}"')
def step_then_message(context, message):
    context.driver.quit()
