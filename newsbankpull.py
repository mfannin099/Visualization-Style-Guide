from bs4 import BeautifulSoup
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import csv
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

#create lists for information storing
titles = []
links = []
dates = []
locations = []
years = []

#i represents page number
i=0

#loop through every page of url search result (20 articles per page -- 10,000 articles would need to go to 500 different pages)
while i < 500 :

    #if on the first page go to main results url and pause for 90seconds to allow user to log in
    if i == 0:
        url2 = 'https://infoweb-newsbank-com.proxy.lib.umich.edu/apps/news/results/?p=WORLDNEWS&t=country%3AUSA%21USA/state%3ANY%7CPA%21Multiple%2520States%2520and%2520Territories%2520%282%29&sort=_rank_%3AD&maxresults=20&f=advanced&val-base-0=%22boil%20water%22&fld-base-0=alltext&bln-base-1=or&val-base-1=%22do%20not%20drink%22&fld-base-1=alltext&fld-nav-1=YMD_date&val-nav-1=2007%20-%202019%27'
        driver.get(url2)
        time.sleep(90)
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content,"html.parser")

        #pull article information from html elements of page
        for div in soup.find_all("h3",{'class':"search-hits__hit__title search-hits__title"}):
            for a in div.find_all("a"):
                link = "https://infoweb-newsbank-com.proxy.lib.umich.edu" + str(a["href"])
                links.append(link)
                text = a.text
                title = text.split("Go to the document viewer for ")
                titles.append(title[-1])

        for div2 in soup.find_all("ul",{"class":"search-hits__hit__meta"}):
            for date in div2.find_all("li",{"class":"search-hits__hit__meta__item search-hits__hit__meta__item--display-date"}):
                datetext = date.text
                dateclean = datetext.strip()
                dates.append(dateclean)
                year = "20" + str(dateclean[-2:])
                years.append(year)
            for location in div2.find_all("li",{"class":"search-hits__hit__meta__item search-hits__hit__meta__item--source"}):
                loctext = location.text
                locclean1 = loctext.strip().split("(")
                locclean2 = locclean1[-1].split(")")
                locations.append(locclean2[0])
        i = i+1
    else:

        try:

            #go to url of next page (i)
            url2 = 'https://infoweb-newsbank-com.proxy.lib.umich.edu/apps/news/results?page=' + str(i) + '&p=WORLDNEWS&t=country%3AUSA%21USA/state%3ANY%7CPA%21Multiple%2520States%2520and%2520Territories%2520%282%29&sort=_rank_%3AD&maxresults=20&f=advanced&val-base-0="boil%20water"&fld-base-0=alltext&bln-base-1=or&val-base-1="do%20not%20drink"&fld-base-1=alltext&fld-nav-1=YMD_date&val-nav-1=2007%20-%202019%27'
            driver.get(url2)
            time.sleep(90)
            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content,"html.parser")

            #pull article information from html elements of page
            for div in soup.find_all("h3",{'class':"search-hits__hit__title search-hits__title"}):
                for a in div.find_all("a"):
                    link = "https://infoweb-newsbank-com.proxy.lib.umich.edu" + str(a["href"])
                    links.append(link)
                    text = a.text
                    title = text.split("Go to the document viewer for ")
                    titles.append(title[-1])

            for div2 in soup.find_all("ul",{"class":"search-hits__hit__meta"}):
                for date in div2.find_all("li",{"class":"search-hits__hit__meta__item search-hits__hit__meta__item--display-date"}):
                    datetext = date.text
                    dateclean = datetext.strip()
                    dates.append(dateclean)
                    year = "20" + str(dateclean[-2:])
                    years.append(year)
                for location in div2.find_all("li",{"class":"search-hits__hit__meta__item search-hits__hit__meta__item--source"}):
                    loctext = location.text
                    locclean1 = loctext.strip().split("(")
                    locclean2 = locclean1[-1].split(")")
                    locations.append(locclean2[0])
            i = i+1
        except:
            
            #fallback results -- if something goes wrong with internet connection or url the page number (i) will be printed and the loop will break
            #this will allow you to see where it failed to start the next run and avoid infinte looping
            print(i)
            print( "is where I stopped")
            break

#write the information into a csv with column headers: title, date, year, location, link
articles = [{'title': title, 'date': date, 'year': year, 'location': location, 'link': link} for title,date,year,location,link in zip(titles,dates,years,locations,links)]
headers = ["title","date",'year',"location","link"]

#REPLACE "YOUR FILE NAME AND LOCATION" with what you want the csv file to be named and where you want the csv file to be saved
#ex : "C:\\Users\\saman\\Desktop\SI405-485\boilwateradvisories_allarticles.csv" 
with open(r'YOUR FILE NAME AND LOCATION', 'w', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(articles)

print("Part 1 DONE")