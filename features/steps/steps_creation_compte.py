import os
import sys
import time
# Fix PYTHONPATH pour GitHub Actions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from selenium.webdriver.edge.options import Options
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.read_data import ReadData


@given("je suis sur la page de creation de compte")
def step_given_page_creation(context):
    context.read = ReadData()
    context.etudiant = context.read.read_data_from_json()

    # 🔧 DETECTION HEADLESS AUTO
    headless = os.getenv('HEADLESS') == 'true' or 'GITHUB_ACTIONS' in os.environ

    # Configuration Edge
    edge_options = Options()

    if headless:
        print("🖥️ Mode HEADLESS (GitHub Actions)")
        edge_options.add_argument('--headless')
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--disable-dev-shm-usage')
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument('--window-size=1920,1080')
    else:
        print("🖥️ Mode GRAPHIQUE (local)")

    # Initialisation driver
    context.driver = webdriver.Edge(options=edge_options)
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

    # Domaine étude - VERSION ROBUSTE avec scroll + wait
    print("🎓 Sélection Domaine d'études...")
    time.sleep(1)

    # Ouvrir dropdown domaine
    driver.find_element(By.XPATH, "//*[@id=\"edit-field-domaine-etudes-wrapper\"]/div/div/div[1]/div").click()
    time.sleep(1)  # Attendre ouverture dropdown

    # Scroll vers section "Médecine" + sélection
    medcine = driver.find_element(By.XPATH,
                                  "/html/body/div[2]/div[2]/main/div[2]/div/div[2]/form/div[4]/div[2]/div[1]/div/div/div[2]/div/div[17]")
    js.execute_script("arguments[0].scrollIntoView({block: 'center'});", medcine)
    time.sleep(0.5)
    js.execute_script("arguments[0].parentElement.scrollTop = arguments[0].offsetTop;", medcine)
    time.sleep(0.5)
    medcine.click()
    print("✅ Médecine sélectionné")
    time.sleep(1)

    # Niveau étude - VERSION ROBUSTE avec scroll + wait
    print("📚 Sélection Niveau d'études...")
    time.sleep(1)

    # Scroll vers section Niveau + ouvrir dropdown
    js.execute_script("arguments[0].scrollIntoView({block: 'center'});",
                      driver.find_element(By.XPATH, "//*[@id=\"edit-field-domaine-etudes-wrapper\"]/div/label"))
    time.sleep(1)

    driver.find_element(By.XPATH, "//*[@id=\"edit-field-niveaux-etude-wrapper\"]/div/div/div[1]/div").click()
    time.sleep(1.5)  # Dropdowns Select2 ont besoin de + de temps

    # Scroll vers "Master" + sélection
    master = driver.find_element(By.XPATH,
                                 "/html/body/div[2]/div[2]/main/div[2]/div/div[2]/form/div[4]/div[2]/div[2]/div/div/div[2]/div/div[8]")
    js.execute_script("arguments[0].scrollIntoView({block: 'center'});", master)
    time.sleep(0.7)
    js.execute_script("arguments[0].parentElement.scrollTop = arguments[0].offsetTop;", master)
    time.sleep(0.5)
    master.click()
    print("✅ Master sélectionné")
    time.sleep(1)

    # Conditions - SOLUTION ANTI-CHEVAUCHEMENT
    print("📋 Acceptation des conditions... (anti-chevauchement)")

    # Méthode 1: JavaScript Click (INFALLIBLE)
    conditions_checkbox = driver.find_element(By.XPATH,
                                              "//*[@id=\"edit-field-accepte-communications-wrapper\"]/div/label")
    js.execute_script("arguments[0].checked = true;", conditions_checkbox)
    js.execute_script("arguments[0].click();", conditions_checkbox)  # Force le clic
    print("✅ Conditions cochées via JavaScript ✓")
    time.sleep(1)


@then('je ferme le navigateur')
def step_then_close_browser(context):
    print("✅ NAVIGATEUR FERMÉ")
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit()
