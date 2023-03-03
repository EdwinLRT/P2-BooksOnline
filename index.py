#Imports
import requests
import re
import csv
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlencode

#GET soup from url
def get_soup(url) : 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


#Get href from category list (from left vertical menu)
def get_categories() :
    print('Collecting categories links...')
    soup = get_soup('https://books.toscrape.com/index.html')
    categories_list = soup.select('ul.nav-list li ul li')
    categories = []
    for li in categories_list:
        link = li.find('a')
        if link is not None:
            href = link.get('href')
            href = href.replace('index.html','')
            categories.append(href)
    print('Categories links collected')
    return categories


#Get all pages of a category 
def get_category_pages(category_path): 
    print('Collecting category pages...')
    category_pages = []
    page = 1    
    while True : 
        url = 'https://books.toscrape.com/'+category_path+'page-'+str(page)+'.html'
        if 'page-1.html' in url :
            url = url.replace('page-1.html', 'index.html') 
        response = requests.get(url)
        if response.status_code == 200:
            category_pages.append(url)
            page += 1
        else:
            page = 1
            break
    return category_pages

def get_books_from_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    list_books = soup.select("article.product_pod > h3 > a")
    books = [("http://books.toscrape.com/catalogue/" + book["href"].replace("../", "")) for book in list_books]
    return books

def get_book_informations(book_url):
    url = book_url
    soup = get_soup(book_url)
    book_data = []
    response = requests.get(url)

    if response.ok : 
        article = soup.find('article')
        #Title
        product_title = article.select('.product_main h1')[0].get_text()
        product_title = re.sub('[^a-zA-Z0-9 \n\.]', '', product_title)
        
        #Product page URL
        page_url = response.url

        #Price including taxes
        th_product_price_incl_taxes = soup.find('th', string ='Price (incl. tax)')
        td_product_price_incl_taxes = th_product_price_incl_taxes.find_next_sibling('td')
        td_product_price_incl_taxes = td_product_price_incl_taxes.get_text().replace('Â£','')
        #Price excluding taxes 
        th_product_price_excl_taxes = soup.find('th', string ='Price (excl. tax)')
        td_product_price_excl_taxes = th_product_price_excl_taxes.find_next_sibling('td')
        td_product_price_excl_taxes = td_product_price_excl_taxes.get_text().replace('Â£','')
        #Number available
        th_product_availability = soup.find('th', string ='Availability')
        td_product_stock = th_product_availability.find_next_sibling('td').get_text()
        product_stock_quantity = int(re.findall(r'\d+', td_product_stock)[0])

        #Product description
        product_description_title = soup.find('div', {'id': 'product_description'})
        if product_description_title is None:
            product_description = "Description missing"
        else:
            product_description = product_description_title.find_next_sibling('p')
            product_description = product_description.get_text()
            product_description = product_description.replace('...more', '')
            product_description = re.sub('[^a-zA-Z0-9 \n\.]', '', product_description)
        #Category
        breadcrumb = soup.find('ul', {'class': 'breadcrumb'})
        product_category = breadcrumb.find_all('a')[2].text.strip()

        #Review rating
        product_rating_class = soup.find(class_='star-rating')
        product_rating_value_string = product_rating_class.get('class')[1]
        help_dict = {
        'Zero': '0',
        'One': '1',
        'Two': '2',
        'Three': '3',
        'Four': '4',
        'Five': '5'
        }
        product_rating_value = help_dict[product_rating_value_string] 

        #UPC
        th_product_upc = soup.find('th', string ='UPC')
        td_product_upc = th_product_upc.find_next_sibling('td')
        th_product_upc_text = soup.find('th', string ='UPC').get_text()
        td_product_upc_text = th_product_upc.find_next_sibling('td').get_text()
        #Image URL 
        base_url = "https://books.toscrape.com"
        gallery_div = soup.find('div', {'id':'product_gallery'})
        product_image = gallery_div.find('img')
        product_image_url = urljoin(str(base_url), str(product_image['src']))
        #Download image
        response = requests.get(product_image_url)
        directory = "book_images"
        if not os.path.exists(directory):
            os.makedirs(directory)
        category_directory = os.path.join(directory, product_category)
        if not os.path.exists(category_directory):
            os.makedirs(category_directory)
        filename = product_title + ".jpg"
        encoded_filename = urlencode({'name': filename})[5:]
        with open(os.path.join(category_directory, encoded_filename), "wb") as f:
            f.write(response.content)

        #Push it in a list
        book_data.append(td_product_upc_text)
        book_data.append(product_title)
        book_data.append(td_product_price_incl_taxes)
        book_data.append(td_product_price_excl_taxes)
        book_data.append(product_stock_quantity)
        book_data.append(product_description)
        book_data.append(product_category)
        book_data.append(product_rating_value)
        book_data.append(product_image_url)
        book_data.append(url)

        return book_data
    else :
        print('Data not found for this book :' + book_url)


# CSV generation 
def create_csv_file(category_name,book_data):
    print('Creating CSV file...')

    csv_directory = "CSV_files"
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)
    filename = category_name
    with open(os.path.join(csv_directory, f"{category_name}.csv"), "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        csv_header = ['UPC','Title','Price incl. taxes','Price excl. taxes','Stock quantity','Description','Category','Rating','Image URL','Article URL']
        writer.writerow(csv_header)
        writer.writerows(book_data)
    print('CSV file created')

#A function to rule them all
def scraping_all_categories():
    print('Scraping all categories...')
    print('Getting categories links...')
    categories = get_categories()
    for category in categories :
        category_name = category.replace('/','')
        category_name = category_name.replace('cataloguecategorybooks','')
        print('Scraping category : ' + category)
        category_pages = get_category_pages(category)
        book_data = []
        for page in category_pages :
            print('Scraping page : ' + page)
            books_on_page = get_books_from_page(page)
            
            for book_url in books_on_page :
                book_informations = get_book_informations(book_url)
                book_data.append(book_informations)
        print('Category scraped : '+ category_name)
        create_csv_file(category_name,book_data)
    print('All categories scraped')
scraping_all_categories()
