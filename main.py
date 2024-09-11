from tabulate import tabulate
import requests
from bs4 import BeautifulSoup


# Here's what's next:
# Get all the hrefs for each torrent and store them in a dictionary ie (dict = {column_index: torrent_link})
# Give user ability to select torrent based on index in torrent table.
# Once user selects the index then get the href for that column from dictionary.
# Scape that specific torrent page for .torrent file or magnet link and download to Downloads directory
# where transadd script gets called to add file to transmission client
# will add search functionality at a later date...working with popular music page for now.

#########################################################################################
# scrape html from torrent site                                                         #
#########################################################################################
url = "https://1337x.to/popular-music"
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
num_of_items = len(list_of_lists - 1)
torrent_to_be_downladed = input(
    f"please choose the torrent you want to download {0 - num_of_items}: "
)
print(f"you have chosen to donwlaod: {link_dict[torrent_to_be_downladed]}")


# make request to link chosen by user and download the .torret file
# need to test both requests and urllib to download .torrent files from torrent site
# test torrent dowload using urllib
# https:stackoverflow.com/questions/46174458/how-to-download-torrent-file

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
