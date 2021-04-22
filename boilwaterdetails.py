from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import csv
import nltk.data
import pandas as pd
import spacy
from spacy import displacy 

#REPLACE "YOUR FILE NAME AND LOCATION" with the csv file name and where you have it saved
#ex : "C:\\Users\\saman\\Desktop\SI405-485\boilwateradvisories_allarticles.csv"
newsbankarticles = pd.read_csv(r"YOUR FILE NAME AND LOCATION")

#this data set was found on github (see documentation) and holds all cities and counties in US
#REPLACE "YOUR FILE LOCATION" with where you have the csv file saved
#ex : "C:\\Users\\saman\\Desktop\SI405-485\us_cities_states_counties.csv.csv"
united_states = pd.read_csv(r"YOUR FILE LOCATION\\us_cities_states_counties.csv",sep='|')

michigan = united_states[united_states["State short"] == "MI"]
minnesota = united_states[united_states["State short"] == "MN"]
wisconsin = united_states[united_states["State short"] == "WI"]
ohio = united_states[united_states["State short"] == "OH"]
indiana = united_states[united_states["State short"] == "IN"]
illinois = united_states[united_states["State short"] == "IL"]
pennsylvania = united_states[united_states["State short"] == "PA"]
newyork = united_states[united_states["State short"] == "NY"]



nlp_wk = spacy.load("xx_ent_wiki_sm")

driver = webdriver.Chrome(ChromeDriverManager().install())

#create new columns for cause and specific location
newsbankarticles["cause"] = " "
newsbankarticles["specific_location"] = " "

#itterate through all rows in newsbankarticles file.  Open the link in the row
for index, a in newsbankarticles.iloc[0: ].iterrows():
    try:   
        s = 0

        #if first article pause for 30 seconds to allow user to login
        if s < 1:     
            url = str(a["link"])
            
            driver.get(url)

            time.sleep(30)
            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content,"html.parser")
        else:
            url = str(a["link"])
            
            driver.get(url)

            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content,"html.parser")
        
        #itterate through every sentence in text of article
        try:
            
            article = soup.find("div",{'class':"document-view__body read document-view__body--ascii"}).text
            
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

            paragraph_sentence_list = tokenizer.tokenize(str(article))
           
            cities = []
            cities2 = []
            testing_reasons = []
            for line in range(0,len(paragraph_sentence_list)):

                #look for "cause" phrase in sentence, if found update the pandas dataframe with phrase
                if 'boil water'in paragraph_sentence_list[line]:
                    simple_reason = "boil water advisory"
                    oldreason = a["cause"]
                    testing_reasons.append(oldreason)
                    testing_reasons.append(simple_reason)
                    reasons2 = list(dict.fromkeys(testing_reasons))

                if 'do not drink'in paragraph_sentence_list[line]:
                    simple_reason = "do not drink advisory"
                    oldreason = a["cause"]
                    testing_reasons.append(oldreason)
                    testing_reasons.append(simple_reason)
                    reasons2 = list(dict.fromkeys(testing_reasons))
        
                if 'loss in water pressure' in paragraph_sentence_list[line]:
                    simple_reason = "loss in water pressure"
                    oldreason = a["cause"]
                    testing_reasons.append(oldreason)
                    testing_reasons.append(simple_reason)
                    reasons2 = list(dict.fromkeys(testing_reasons))
                   
                if 'water main break' in paragraph_sentence_list[line]:
                    simple_reason = "water main break"
                    oldreason = a["cause"]
                    testing_reasons.append(oldreason)
                    testing_reasons.append(simple_reason)
                    reasons2 = list(dict.fromkeys(testing_reasons))
                    
                if 'bacteria' in paragraph_sentence_list[line]:
                    simple_reason = "bacteria found in water"
                    oldreason = a["cause"]
                    testing_reasons.append(oldreason)
                    testing_reasons.append(simple_reason)
                    reasons2 = list(dict.fromkeys(testing_reasons))
                    
                if 'contaminants'in paragraph_sentence_list[line]:
                    simple_reason = "contaminants"
                    oldreason = a["cause"]
                    testing_reasons.append(oldreason)
                    testing_reasons.append(simple_reason)
                    reasons2 = list(dict.fromkeys(testing_reasons))

                #clean "cause" text to allow more than one to appear in column if multiple causes are found    
                filter_object = filter(lambda x: x != " ", reasons2)
                without_empty_strings = list(filter_object)
                newsbankarticles.at[index,'cause'] = without_empty_strings

                #finding specific location
                # get state from "location" column, look for appearance of any city or county from that state in article text, update pandas dataframe with specific location           
                written_location = a["location"]
                if "MN" in written_location:
                    for city in minnesota["City"]:
                        if str(city) in paragraph_sentence_list[line]:
                            oldcity = a["specific_location"]
                            cities.append(oldcity)
                            newcity = str(city) + ",MN"
                            cities.append(newcity)
                            cities2 = list(dict.fromkeys(cities))
                            
                if "MI" in written_location:
                    for city in michigan["City"]:
                        if str(city) in paragraph_sentence_list[line]:
                            oldcity = a["specific_location"]
                            cities.append(oldcity)
                            newcity = str(city) + ",MI"
                            cities.append(newcity)
                            cities2 = list(dict.fromkeys(cities))
                       
                if "WI" in written_location:
                    for city in wisconsin["City"]:
                        if str(city) in paragraph_sentence_list[line]:
                            oldcity = a["specific_location"]
                            cities.append(oldcity)
                            newcity = str(city) + ",WI"
                            cities.append(newcity)
                            cities2 = list(dict.fromkeys(cities))
                            
                if "OH" in written_location:
                    for city in ohio["City"]:
                        if str(city) in paragraph_sentence_list[line]:
                            oldcity = a["specific_location"]
                            cities.append(oldcity)
                            newcity = str(city) + ",OH"
                            cities.append(newcity)
                            cities2 = list(dict.fromkeys(cities))
                            
                if "IN" in written_location:
                    for city in indiana["City"]:
                        if str(city) in paragraph_sentence_list[line]:
                            oldcity = a["specific_location"]
                            cities.append(oldcity)
                            newcity = str(city) + ",IN"
                            cities.append(newcity)
                            cities2 = list(dict.fromkeys(cities))
                            
                if "IL" in written_location:
                    for city in illinois["City"]:
                        if str(city) in paragraph_sentence_list[line]:
                            oldcity = a["specific_location"]
                            cities.append(oldcity)
                            newcity = str(city) + ",IL"
                            cities.append(newcity)
                            cities2 = list(dict.fromkeys(cities))
                            
                if "PN" in written_location:
                    for city in pennsylvania["City"]:
                        if str(city) in paragraph_sentence_list[line]:
                            oldcity = a["specific_location"]
                            cities.append(oldcity)
                            newcity = str(city) + ",PN"
                            cities.append(newcity)
                            cities2 = list(dict.fromkeys(cities))
                           
                if "NY" in written_location:
                    for city in newyork["City"]:
                        if str(city) in paragraph_sentence_list[line]:
                            oldcity = a["specific_location"]
                            cities.append(oldcity)
                            newcity = str(city) + ",NY"
                            cities.append(newcity)
                            cities2 = list(dict.fromkeys(cities))
                           
        
                #clean "specific_location" text to allow more than one to appear in column if multiple cities/counties are found  
                filter_object = filter(lambda x: x != " ", cities2)
                without_empty_strings = list(filter_object)
                newsbankarticles.at[index,'specific_location'] = without_empty_strings

            #write updated csv with new cause and specific location columns added to row 
            #we write new file our at the end of ever iteration to avoid code breaking halfway through 10,000 articles and having to completely restart process
            #all of the following four file names and locations should be exactly the same
            #REPLACE "YOUR FILE NAME AND LOCATION" with the csv file name and where you want it to be saved
            #ex : "C:\\Users\\saman\\Desktop\SI405-485\boilwateradvisories_detailed.csv"
            s+=1
            newsbankarticles.to_csv(r"YOUR FILE NAME AND LOCATION")
        except:

            #write updated csv with new cause and specific location columns added to row(even if no data found)
            #REPLACE "YOUR FILE NAME AND LOCATION" with the csv file name and where you want it to be saved
            #ex : "C:\\Users\\saman\\Desktop\SI405-485\boilwateradvisories_detailed.csv"
            s+=1
            newsbankarticles.to_csv(r"YOUR FILE NAME AND LOCATION")
            continue

    except:

        #write updated csv with new cause and specific location columns added to row(this step occurs when pdf documents are read in or broken link)
        #REPLACE "YOUR FILE NAME AND LOCATION" with the csv file name and where you want it to be saved
        #ex : "C:\\Users\\saman\\Desktop\SI405-485\boilwateradvisories_detailed.csv"
        print("Skipping :")
        s+=1
        newsbankarticles.to_csv(r"YOUR FILE NAME AND LOCATION")
     

#write final updated csv with new cause and specific location columns
#REPLACE "YOUR FILE NAME AND LOCATION" with the csv file name and where you want it to be saved
#ex : "C:\\Users\\saman\\Desktop\SI405-485\boilwateradvisories_detailed.csv"
newsbankarticles.to_csv(r"YOUR FILE NAME AND LOCATION")
print("Part2 Done")