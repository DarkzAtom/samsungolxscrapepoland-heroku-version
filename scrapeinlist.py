import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions

def insidelist(url):

    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    elements_for_neg_pam_stan = soup.select('li.css-1r0si1e')

    name = soup.select_one('h4', class_='css-77x51t').get_text() # pasuje
    cena = soup.select_one('h3', class_='css-93ez2t').get_text() if soup.select_one('h3', class_='css-93ez2t') is not None else None #pasuje
    for element in elements_for_neg_pam_stan:
        if "do negocjacji" in element.get_text().lower():
            negocjacja = element.get_text()  #pasuje
            break
        else:
            negocjacja = 'blablabla'




    wysylka = soup.select_one('span', class_='css-tj1qbd').get_text() if soup.select_one('span', class_='css-tj1qbd') is not None else None #pasuje
    miasto = soup.select_one('p.css-1cju8pu.er34gjf0').get_text() if soup.select_one('p.css-1cju8pu.er34gjf0') is not None else None # pasuje
    opis = soup.select_one('div.css-1t507yq.er34gjf0').get_text() if soup.select_one('div.css-1t507yq.er34gjf0') is not None else None # pasuje

    for element in elements_for_neg_pam_stan:
        if 'wbudowana' in element.get_text().lower():
            pamiec = element.get_text(strip=True).split(':')[1].strip() if ':' in element.get_text() else None
            break #pasuje
        else:
            pamiec = ''

    for element in elements_for_neg_pam_stan:
        if 'stan' in element.get_text().lower():
            stan = desired_text = element.get_text(strip=True).split(':')[1].strip() if ':' in element.get_text() else None

            break
        else:
            stan = ''


    image_section = soup.select_one('div.swiper.swiper-initialized.swiper-horizontal.swiper-backface-hidden')
    image_class = image_section.select('img') # NIE PASUJE SPRW
    image_list = []

    for image in image_class:
        image_url = image.get('src')
        parts = image_url.split(":443")
        modified_image_url = "".join(parts)
        image_list.append(modified_image_url)




    item = {
        'Nazwa': name,
        'Cena': cena,
        'Negocjacja': negocjacja,
        'Wysylka': wysylka,
        'Miasto': miasto,
        'Opis': opis,
        'Pamiec': pamiec,
        'Stan': stan,
        'image': image_list,
        'Url': url
    }

    return item





