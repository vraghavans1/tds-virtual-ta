# save_login_cookies.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

def save_cookies():
    options = Options()
    options.add_experimental_option("detach", True)  # stays open after script ends
    driver = webdriver.Chrome(options=options)

    driver.get(BASE_URL + "/login")
    print("🟢 Chrome opened. Log in manually.")
    print("🕒 After logging in and seeing the Discourse home page...")
    input("📩 Press ENTER here to save cookies and close the browser.\n")

    cookies = driver.get_cookies()
    with open("cookies.json", "w") as f:
        json.dump(cookies, f)

    print("✅ Cookies saved to cookies.json")
    driver.quit()

if __name__ == "__main__":
    save_cookies()
