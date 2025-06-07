from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from langdetect import detect
import time

def is_russian(text):
    try:
        lang = detect(text)
        return lang == 'ru'
    except:
        return False

def get_mlbb_news():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")

    driver_path = r"C:\chromedriver-win32\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://m.mobilelegends.com/ru/news")
        time.sleep(3)

        cards = driver.find_elements(By.CLASS_NAME, "news-card")
        for card in cards:
            try:
                title = card.find_element(By.CLASS_NAME, "news-title").text.strip()
                summary = card.find_element(By.CLASS_NAME, "news-desc").text.strip()
                link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

                if title and summary and is_russian(title + summary):
                    return {
                        "title": f"[Official RU] {title}",
                        "summary": summary,
                        "link": link
                    }
            except:
                continue
    except Exception as e:
        print("Selenium error:", e)
    finally:
        driver.quit()

    return None
