import requests
import re
from bs4 import BeautifulSoup

# GET url request 
url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
requests.get(url)
response =requests.get(url)

if response.ok: 
    # Analyse HTML with beautifulsoup 
    soup = BeautifulSoup(response.text, 'html.parser')
    for article in soup.findAll('article'):
    #Title
        title = article.select('.product_main h1')[0].get_text()

    #Product page URL

    
    #Price including taxes
        th_product_price_incl_taxes = soup.find('th', text ='Price (incl. tax)')
        td_product_price_incl_taxes = th_product_price_incl_taxes.find_next_sibling('td')
    
    #Price excluding taxes 
        th_product_price_excl_taxes = soup.find('th', text ='Price (excl. tax)')
        td_product_price_excl_taxes = th_product_price_excl_taxes.find_next_sibling('td')

    #Number available
        th_product_availability = soup.find('th', text ='Availability')
        td_product_stock = th_product_availability.find_next_sibling('td').get_text()
        product_stock_quantity = int(re.findall(r'\d+', td_product_stock)[0])

    #Product description
        product_description_title = soup.find('div', {'id':'product_description'})
        product_description = product_description_title.find_next_sibling('p')

    #Category
        th_product_type = soup.find('th', text ='Product Type')
        td_product_category = th_product_type.find_next_sibling('td')

    #Review rating


    #UPC
        th_product_upc = soup.find('th', text ='UPC')
        td_product_upc = th_product_upc.find_next_sibling('td')
        th_product_upc_text = soup.find('th', text ='UPC').get_text()
        td_product_upc_text = th_product_upc.find_next_sibling('td').get_text()
    #Image URL 
        gallery_div = soup.find('div', {'id':'product_gallery'})
        product_image = gallery_div.find('img')
        product_image_url = product_image['src']
    #

    #Print function 
        #print(th_product_upc_text, td_product_upc_text)
        #print(product_image_url)
        #print(th_product_price_excl_taxes.get_text(), td_product_price_excl_taxes.get_text())
        #print(th_product_price_incl_taxes.get_text(), td_product_price_incl_taxes.get_text())
        #print(product_description.get_text())
        print(product_stock_quantity)


    
