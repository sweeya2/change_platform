from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

def get_list_of_songs(url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5) # wait a second for <div id="root"> to be fully loaded
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    music_links = soup.findAll("div", {"class": "col1"})
    song_titles = []
    for link in music_links:
        song_title = link.findChild("music-link")['title']
        song_titles.append(song_title)
    return song_titles


# playlist_url = "https://music.amazon.com/playlists/B07WV4DNDR"
# get_list_of_songs(playlist_url)

        

