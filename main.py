from tabulate import tabulate
import requests
from bs4 import BeautifulSoup
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By

# from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


# TODOs
# Below have been implemeted as of 09/23
#   Get all the hrefs for each torrent and store them in a dictionary ie (dict = {column_index: torrent_link})
#   Give user ability to select torrent based on index in torrent table.
#   Once user selects the index then get the href for that column from dictionary.
#   Scape that specific torrent page for .torrent file or magnet link and download to Downloads directory.

# Next up
# add search functionality
#   user argppare to allow user to search for torrents by category (https://1337x.to/category-search/miles%20davis/Music/1/)
#   Categories
#       Music
#       Movies
#       TV
#       Games
#       Applcation


#########################################################################################
# scrape html from torrent site                                                         #
#########################################################################################
url = "https://1337x.to/popular-music"
url_prefix = "https://1337x.to"
response = requests.get(url)
webpage = response.text
soup = BeautifulSoup(webpage, "lxml")

#########################################################################################
# get the column headers to the table of torrents (name, se, le, time, size, uploader)  #
#########################################################################################
torrent_table_headers = soup.find("thead")
# print(torrent_table_headers)

just_the_headers = torrent_table_headers.findChildren("th")
# print(just_the_headers)

headers = [header.getText() for header in just_the_headers]
# print(headers)


###########################################################################################
# get the entire torrent table from the html                                              #
###########################################################################################
torrent_table_body = soup.find("tbody")
# print(torrent_table_body)

# get just all the rows of the torrent table
torrent_tr = torrent_table_body.findChildren("tr")
# print(torrent_tr)

# strip \n from the text in the column data
torrent_data = [data.getText() for data in torrent_tr if data.getText().strip()]
# print(torrent_data)


############################################################################################
# write out each column as a list, all the values of each column are comma separated       #
############################################################################################

# going to put all the separate columns in a list of lists to loop through when i give them to tabulate
list_of_lists = []

for i in torrent_data:
    item = i.strip().split("\n")
    # new_list = []
    # new_list.append(i)
    list_of_lists.append(item)
# print(list_of_lists)


###########################################################################################
# get all torrent links from torrent table                                                #
###########################################################################################

# get all the a tags that contain  alink to the torrent
list_of_a_tags = [tag.find_all("a")[1] for tag in torrent_tr]
# print(list_of_a_tags)

# create a list of just the torrent links
links = [link.get("href") for link in list_of_a_tags]
# print(links)

# create a dict that contians the torrent index in torrren table as key and torrent link as value
link_dict = {i: links[i] for i in range(len(links))}
# print(link_dict)


###########################################################################################
# print scraped data from torrent site to a table with tabulate                           #
###########################################################################################

data_from_row_one = [i for i in list_of_lists]

table_1 = tabulate(
    data_from_row_one,
    headers=headers,
    numalign="center",
    stralign="center",
    tablefmt="fancy_grid",
    colalign="center",
    showindex="always",
)
print(table_1)


#########################################################################################
# ask user to choose which torrent and select index the appropriate index               #
# #######################################################################################
num_of_items = len(list_of_lists)
torrent_to_be_downladed = int(
    input(f"please choose the torrent you want to download 0 - {num_of_items - 1}: ")
)

print(f"you have chosen to downlaod: {link_dict[torrent_to_be_downladed]}")

this_torrent = f"{url_prefix}{link_dict[torrent_to_be_downladed]}"

########################################################################################
# get torrent link from torrent webpage                                                #
# ######################################################################################

# get html from chosen torrent page
# this_torrent_response = requests.get(this_torrent)
# this_torrent_webpage = this_torrent_response.text
# torrent_soup = BeautifulSoup(this_torrent_webpage, "lxml")
# drop_down = torrent_soup.find(".dropdown-menu")
# print(drop_down)

# link to download torrent file is in a dropdown-menu
# will most likely need to use selenium to click dropdown-menu and torrent download link

########################################################################################
# get drop-down menu of torrent link with selenium
# ######################################################################################

options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

driver.get(this_torrent)

time.sleep(10)

# "/html/body/main/div/div/div/div[2]/div[1]/ul[1]/li[6]/a/span/i"

torrent_download_button = driver.find_element(
    By.CSS_SELECTOR, "li.dropdown > a"
).click()

# (By.XPATH, "/html/body/main/div/div/div/div[2]/div[1]/ul[1]/li[5]/a").click()

print("torrent button clicked")


# once link is clicked a new tab opens need to get titles of both tabs and stay on original tab

# time.sleep(15)


windows_before = driver.current_window_handle
print(windows_before)
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
windows_after = driver.window_handles
new_window = [x for x in windows_after if x != windows_before][0]
driver.switch_to.window(new_window)
time.sleep(10)
print(new_window)
driver.close()
driver.switch_to.window(windows_before)

#######################################################################################
# Get url to .torrent file from dropdown-menu
######################################################################################

itorrents_mirror = driver.find_element(
    By.CSS_SELECTOR, "ul.dropdown-menu > li > a"
).get_attribute("href")

# itorrents_mirror.click()

print(itorrents_mirror)

driver.quit()

# print(f".torrent file has been downloaded. please check downloads directory")
# need to test both requests and urllib to download .torrent files from torrent site
# test torrent dowload using urllib
# https:stackoverflow.com/questions/46174458/how-to-download-torrent-file

##########################################################################################
# Use xdg-open to download .torrent file                                                 #
##########################################################################################

subprocess.Popen(
    ["xdg-open", itorrents_mirror], stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

print(".torrent file has been downloaded, please check Downloads folder")

print("Done.")


# torrents = soup.select(".table-list")
# print(torrents)


# data = [
#    ["Roll Number", "Student Name", "Marks"],
#    [1, "Sasha", 32],
#    [2, "Richard", 36],
#    [3, "Judy", 20],
#    [4, "Lori", 39],
#    [5, "Maggie", 40],
# ]

# table_1 = tabulate(data)
# table_2 = tabulate(data, headers="firstrow")
# print(table_1)
# print(table_2)
