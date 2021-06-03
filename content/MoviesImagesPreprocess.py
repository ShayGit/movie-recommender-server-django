
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

chrome_driver_path = "chromedriver"
driver = webdriver.Chrome(chrome_driver_path)

from_df = pd.read_csv("movies_metadata.csv")
from_df = from_df.drop_duplicates(subset=["title", "combined"], keep="first").reset_index(drop=True)
from_df = from_df.drop_duplicates(subset=["title"], keep="first").reset_index(drop=True)

# Copy images urls from existing csv first
images_data = pd.read_csv("MovieGenre.csv")

for (idx, row) in images_data.iterrows():
    if not pd.isna(row['Poster']):
        try:
            title = row['Title'].split(" (")[0]
            img_url = row['Poster']
            from_df.loc[from_df['title'] == title, 'image'] = img_url
        except:
            continue

# Scrape the rest of images urls from imdb website
driver.get('https://www.imdb.com/')
wait = WebDriverWait(driver, 4)

for (idx, row) in from_df.iterrows():
    movie_title = row['title']
    movie_data = row['combined']
    cast = []
    if pd.isna(row['image']):
        try:
            search_input = wait.until(EC.visibility_of_element_located((By.ID, 'suggestion-search')))
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.DELETE)
            search_input.send_keys(row['title'])
            time.sleep(1)
            sug_html = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'react-autosuggest__suggestions-list'))).get_attribute(
                'innerHTML')
            soup = BeautifulSoup(sug_html, 'lxml')
            cast = [x.text.replace(" ", "").lower() for x in soup.find_all('div', {
                "class": "searchResults__ResultTextItem-sc-1pmqwbq-2 lolMki _1DoAqrviL4URifsx8tYz_V"})[1::2]]
            images_container = soup.find_all('div', {"class": "_2xcsB5_XEiRCOYGbWQ05C9__image"})
        except:
            continue
        for i in range(len(cast)):
            try:
                a2 = ""
                alist = cast[i].split(',')
                if len(alist) > 1:
                    a1 = alist[0]
                    a2 = alist[1]
                else:
                    a1 = alist[0]

                if (a1 and str(movie_data).find(a1) != -1) or (a2 and str(movie_data).find(a2) != -1):
                    img = images_container[i].find('img')
                    if img:
                        img_url = img['src'].split('_')[0] + '_V1_UX182_CR0,0,182,250_.jpg'
                        from_df.loc[idx, 'image'] = img_url
                        break
            except:
                pass

to_df = from_df[from_df['image'].notna()]
to_df.to_csv("movies_data_final.csv", index=False)
driver.quit()
print("Done!")
