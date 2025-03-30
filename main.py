from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fpdf import FPDF
from PIL import Image
import requests

def sanitize(text):
    new_text = ""
    for i in text.lower():
        if i in "abcdefghijklmnopqrstuvwxyz1234567890-_ ":
            new_text += i
        else:
            new_text += "_"
    return new_text
pdf = FPDF()

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)

def doThing(MANGA_ID):
    print("Getting data for " + str(MANGA_ID))

    driver.get(f"http://hentaifox.com/gallery/{MANGA_ID}/")

    FILE_NAME = sanitize(driver.title)

    print(FILE_NAME)

    gallery = driver.find_element(By.ID, "append_thumbs")

    initial_count = len(gallery.find_elements(By.TAG_NAME, "a"))

    driver.find_element(By.ID, "load_all").click()

    final_count = len(gallery.find_elements(By.TAG_NAME, "a"))
    if initial_count == 10:
        while final_count == initial_count:
            final_count = len(gallery.find_elements(By.TAG_NAME, "a"))

    print(f"Found {final_count} pages")

    images = []
    for i in range(1, final_count + 1):
        print(f"Downloading {i}/{final_count}")

        driver.get(f"https://hentaifox.com/g/{MANGA_ID}/{i}")
        src = driver.find_element(By.ID, "gimg").get_attribute("src")
        while "data:image/svg+xml" in src:
            src = driver.find_element(By.ID, "gimg").get_attribute("src")
        images.append(Image.open(requests.get(src, stream = True).raw))

    print("Creating pdf")

    images[0].save(
        f"./{FILE_NAME}.pdf", "PDF", resolution=100.0, save_all = True, append_images=images[1::]
    )

    print(f"PDF created: {FILE_NAME}.pdf")

doThing(input("Hentai id: "))