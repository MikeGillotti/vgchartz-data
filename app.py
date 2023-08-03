from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

import math

# I'm creating a list of each genre and sorting the games by genre rather than going to each game's page individually
# The webscraper goes by each of the genres one by one, and since it's already filtered by that genre, it has that data.
genres = [
    "Action",
    "Action-Adventure",
    "Adventure",
    "Board Game",
    "Education",
    "Fighting",
    "Misc",
    "MMO",
    "Music",
    "Party",
    "Platform",
    "Puzzle",
    "Racing",
    "Role-Playing",
    "Sandbox",
    "Shooter",
    "Simulation",
    "Sports",
    "Strategy",
    "Visual Novel"
]
genre_index=0
results_per_page=1000

title_data =[]
console_data =[]
publisher_data = []
developer_data = []
vgchartz_score_data= []
critic_score_data= []
user_score_data = []
total_shipped_data = []
total_sales_data = []
na_sales_data = []
pal_sales_data = []
japan_sales_data = []
other_sales_data = []
release_data = []
last_update_data = []
genre_data = []
        
# I had to manually include the results for each genre, because I the automatic method I tried to make wasn't reliable
# and kept throwing errors. No idea why
total_results = [8401, 1755, 6166, 26, 34, 2319, 9300, 113, 285, 148, 3943, 3471, 3374, 5609, 20, 5332, 3078, 5565, 3643, 491]


for genre_index in range(0, len(genres)):
    genre_result_url = 'https://www.vgchartz.com/games/games.php?name=&keyword=&console=&region=All&developer=&publisher=&goty_year=&genre='+genres[genre_index]+'&boxart=Both&banner=Both&ownership=Both&showmultiplat=No&results=100&order=Sales&showtotalsales=0&showtotalsales=1&showpublisher=0&showpublisher=1&showvgchartzscore=0&showvgchartzscore=1&shownasales=0&shownasales=1&showdeveloper=0&showdeveloper=1&showcriticscore=0&showcriticscore=1&showpalsales=0&showpalsales=1&showreleasedate=0&showreleasedate=1&showuserscore=0&showuserscore=1&showjapansales=0&showjapansales=1&showlastupdate=0&showlastupdate=1&showothersales=0&showothersales=1&showshipped=0&showshipped=1'
    genre_result_page = requests.get(genre_result_url)
    genre_result_soup = BeautifulSoup(genre_result_page.text, 'html')

    #This is the automatic method I tried to make. Sometimes it worked, sometimes it didn't
    #total_results=int(genre_result_soup.find('th', attrs={"colspan": "3"}).text.split()[1][1:-1].replace(",", ""))
   
    #The total page amount is calculated here
    total_pages=math.ceil(total_results[genre_index]/results_per_page)
    
    #Each page is iterated per genre filter and all the data is simply collected from the results table.
    for page_number in range(1, total_pages):
        data_group=[]
        dev_pub =[]

        url = 'https://www.vgchartz.com/games/games.php?name=&keyword=&console=&region=All&developer=&publisher=&goty_year=&genre='+genres[genre_index]+'&boxart=Both&banner=Both&ownership=Both&showmultiplat=No&results='+str(results_per_page)+'&order=Sales&showtotalsales=0&showtotalsales=1&showpublisher=0&showpublisher=1&showvgchartzscore=0&showvgchartzscore=1&shownasales=0&shownasales=1&showdeveloper=0&showdeveloper=1&showcriticscore=0&showcriticscore=1&showpalsales=0&showpalsales=1&showreleasedate=0&showreleasedate=1&showuserscore=0&showuserscore=1&showjapansales=0&showjapansales=1&showlastupdate=0&showlastupdate=1&showothersales=0&showothersales=1&showshipped=0&showshipped=1&page='+str(page_number)

        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'html')
        script_data=soup.find_all('td', attrs={"style": "font-size:12pt;"})
        for title in script_data:
            title.find('a')
            title_data.append(title.text.replace("Read the review", "").strip())
            genre_data.append(genres[genre_index])
        script_data=soup.find_all('td', attrs={"width": "100"})
        for publisher in script_data:
            #title.find('a', attrs={"style": "color:#e60012"})
            dev_pub.append(publisher.text.strip())
        for i in range(0, len(dev_pub),2):
            publisher_data.append(dev_pub[i])
        for i in range(1, len(dev_pub),2):
            developer_data.append(dev_pub[i])
        script_data=soup.find_all('td', attrs={"align": "center"})
        for dg in script_data:
            data_group.append(dg)
        for i in range(1, len(data_group),12):
            console_data.append(data_group[i-1].find('img').get('alt', ''))
            vgchartz_score_data.append(data_group[i].text.strip())
            critic_score_data.append(data_group[i+1].text.strip())
            user_score_data.append(data_group[i+2].text.strip())
            total_shipped_data.append(data_group[i+3].text.strip())
            total_sales_data.append(data_group[i+4].text.strip())
            na_sales_data.append(data_group[i+5].text.strip())
            pal_sales_data.append(data_group[i+6].text.strip())
            japan_sales_data.append(data_group[i+7].text.strip())
            other_sales_data.append(data_group[i+8].text.strip())
            release_data.append(data_group[i+9].text.strip())
            last_update_data.append(data_group[i+10].text.strip())

        

#Column header
column_header=[
    'Title',
    'Console',
    'Publisher',
    'Developer',
    'VGChartz Score',
    'Critic Score',
    'User Score',
    'Total Shipped',
    'Total Sales',
    'NA Sales',
    'PAL Sales',
    'Japan Sales',
    'Other Sales',
    'Release Date',
    'Last Update',
    'Genre'
]


#Data values
column_values=[
        title_data,
        console_data,
        publisher_data,
        developer_data,
        vgchartz_score_data,
        critic_score_data,
        user_score_data,
        total_shipped_data,
        total_sales_data,
        na_sales_data,
        pal_sales_data,
        japan_sales_data,
        other_sales_data,
        release_data,
        last_update_data,
        genre_data
]
                
pd.set_option('display.max_rows', None)

#Add header to dataframe
df=pd.DataFrame(columns=column_header)

#Add data to data frame
for column, value in zip( column_header, column_values):
    df[column] = value


df.to_csv('vg_data.csv')
