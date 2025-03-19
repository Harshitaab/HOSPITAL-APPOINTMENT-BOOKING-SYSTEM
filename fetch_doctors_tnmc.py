from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from appointments.models import Doctor, Hospital
from webdriver_manager.chrome import ChromeDriverManager

def fetch_tnmc_doctors():
    print("📌 Fetching doctors from TNMC using Selenium...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    try:
        driver.get("https://www.tamilnadumedicalcouncil.org/info/doctors/search")
        time.sleep(3)
        search_box = driver.find_element(By.NAME, "search")
        search_box.send_keys(" ")
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        doctors = driver.find_elements(By.XPATH, "//table//tr")
        for doctor in doctors[1:]:
            details = doctor.find_elements(By.TAG_NAME, "td")
            if len(details) < 4:
                continue
            doctor_name = details[0].text.strip()
            speciality = details[2].text.strip()
            hospital_name = details[3].text.strip()
            languages_spoken = "Tamil, English"
            hospital, _ = Hospital.objects.get_or_create(name=hospital_name)
            Doctor.objects.get_or_create(
                name=doctor_name,
                speciality=speciality,
                languages_spoken=languages_spoken,
                hospital=hospital
            )
            print(f"✅ Added Doctor: {doctor_name} - {speciality} at {hospital.name}")
        print("🎉 TNMC doctors successfully added!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

fetch_tnmc_doctors()
