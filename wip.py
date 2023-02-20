#Boucle  pour recuperer tous les articles de la page 
# boucle pour recuperer tous les liens du menu
#Imports
import requests
import re
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import numpy as np

# GET url request 
url = 'http://books.toscrape.com/'

response =requests.get(url)

if response.ok: 
#  https://books.toscrape.com/catalogue/category/books/mystery_3/page-1.html incrementer page 1 pour avoir toute la categorie
    # Analyse HTML with beautifulsoup 
    soup = BeautifulSoup(response.text, 'html.parser')
    # Sélectionner tous les éléments li dans la liste nav-list
    categories_list = soup.select('ul.nav-list li')

# Parcourir les éléments li et extraire les liens href

    categories_link_list = []
    for li in categories_list:
        link = li.find('a')
        if link is not None:
            href = link.get('href')
            categories_link_list.append(href)
        print(categories_link_list)

            #delete the 'index.html' part of every link
            # href = href.replace('index.html','')
            # pages= np.arange(1,10)
            # for page in pages : 
            #     cat_url = 'https://books.toscrape.com/'+href+'page-'+str(page)+'.html'
            #     print(cat_url)
            




    #category_pages = soup.select('ul')
    #for li in 

    #np.arange(1,51)
    #for page in pages :
#             categories_list = []
#     for li in categories_list:
#         link = li.find('a')
#         if link is not None:
#             href = link.get('href')
#             categories_list.append(href)
# #Function - Then modify the link for page navigation 
#             href = href.replace('index.html','')
#             pages= np.arange(1,11)
#             for page in pages : 
#                 cat_url = 'https://books.toscrape.com/'+href+'page-'+str(page)+'.html'
#                 print(cat_url)