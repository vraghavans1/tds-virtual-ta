from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
from tqdm import tqdm
import os

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_ID = "56"
CATEGORY_URL = f"{BASE_URL}/c/tools-in-data-science/{CATEGORY_ID}"

def load_cookies(driver):
    with open("cookies.json") as f:
        cookies = json.load(f)
    driver.get(BASE_URL)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_post_links(driver):
    driver.get(BASE_URL)
    load_cookies(driver)
    driver.get(CATEGORY_URL)
    scroll_to_bottom(driver)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []
    for a in soup.select("a.title.raw-link.raw-topic-link"):
        href = a.get("href")
        if href and href.startswith("/t/"):
            links.append(href)
    return list(set(links))

def scrape_post(driver, url):
    full_url = BASE_URL + url
    driver.get(full_url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        title = soup.find("title").text.strip()
        body_div = soup.find("div", class_="cooked")
        if not body_div:
            return None
        body = body_div.get_text(separator="\n").strip()
        return {
            "title": title,
            "body": body,
            "url": full_url
        }
    except:
        return None

def scrape_all_posts():
    options = Options()
    # options.add_argument("--headless")  # you can turn this on later
    driver = webdriver.Chrome(options=options)

    print("🌐 Logging in using saved cookies...")
    links = get_post_links(driver)
    print(f"🔗 Found {len(links)} post links.")

    posts = []
    for link in tqdm(links[:50]):  # scrape 50 posts max for testing
        post = scrape_post(driver, link)
        if post:
            posts.append(post)
        time.sleep(1)

    driver.quit()

    os.makedirs("data", exist_ok=True)
    with open("data/discourse.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print("✅ Scraped posts saved to data/discourse.json")

if __name__ == "__main__":
    if not os.path.exists("cookies.json"):
        print("❌ Please run save_login_cookies.py first to save your session.")
    else:
        scrape_all_posts()
