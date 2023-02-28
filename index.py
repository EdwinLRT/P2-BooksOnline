#Imports
import requests
import re
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#GET soup from url
def get_soup(url) : 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

print('Starting scraping...')

#Get href from category list (from left vertical menu)
def get_categories_links() :
    print('Collecting categories links...')
    soup = get_soup('https://books.toscrape.com/index.html')
    categories_list = soup.select('ul.nav-list li ul li')
    categories_link_list = []
    for li in categories_list:
        link = li.find('a')
        if link is not None:
            href = link.get('href')
            href = href.replace('index.html','')
            categories_link_list.append(href)
    print('Categories links collected')
    return categories_link_list


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

#Get every book links from category pages
def get_articles_links(category_pages) : 
    articles_link_list = []
    print('Collecting articles links from category pages...')
    for i in category_pages : 
        url = i
        soup = get_soup(url)
        articles_list = soup.select('div section div ol.row li article h3') 

        for li in articles_list:
            link = li.find('a')
            if link is not None:
                href = link.get('href')
                # href = href.replace('index.html','')
                base_url = "https://books.toscrape.com/"
                href = href.replace('../../../','')
                full_article_link = urljoin(('https://books.toscrape.com/catalogue/'), str(href))
                articles_link_list.append(full_article_link)
    print('Articles links collected')
    return articles_link_list

print('Collecting each book informations...')
def get_book_informations(book_url):
    url = book_url
    soup = get_soup(book_url)
    book_data = []
    response = requests.get(url)

    if response.ok : 
        article = soup.find('article')
        #Title
        product_title = article.select('.product_main h1')[0].get_text()

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
        product_description_title = soup.find('div', {'id':'product_description'})
        product_description = product_description_title.find_next_sibling('p')

        #Category
        th_product_type = soup.find('th', string ='Product Type')
        td_product_category = th_product_type.find_next_sibling('td')

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

        #Push it in a list
        book_data.append(td_product_upc_text)
        book_data.append(product_title)
        book_data.append(td_product_price_incl_taxes)
        book_data.append(td_product_price_excl_taxes)
        book_data.append(product_stock_quantity)
        book_data.append(product_description.get_text())
        book_data.append(td_product_category.get_text())
        book_data.append(product_rating_value)
        book_data.append(product_image_url)
        book_data.append(url)

        return book_data
    else :
        print('Data not found for this book :' + book_url)

    print('Books informations collected')

# CSV generation 
def create_csv_file():
    print('CSV generation...')
    #header for column names
    header = ['UPC',
            'Title',
            'Price incl. taxes',
            'Price excl. taxes',
            'Stock quantity',
            'Description',
            'Category',
            'Rating',
            'Image URL',
            'Article URL'
            ]
    
    # create csv file / enter in writing mode
    for category in categories_list :
        #cleaning files names
        category = category.replace('/','')
        category = category.replace('cataloguecategorybooks','')
        file_name = f'{category}.csv'
        #creating files and writing in 
        with open(file_name, 'w', newline='') as csvfile :
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header)
            for i in articles_links : 
                    print(i)
                    writer.writerow(get_book_informations(i))
    print('CSV generated')

print('End of the program')


#A function to rule them all
def scraping_all_categories():
    print('Scraping all categories...')
    print('Getting categories links...')
    categories_links = get_categories_links()
    all_categories_pages = []
    for category in categories_links:
        print('Scraping category : ' + category)
        category_pages = get_category_pages(category)
        all_categories_pages.append(category_pages)
        print('OK')
    print(all_categories_pages)
    for pages in all_categories_pages:
        articles_links = get_articles_links(pages)
        print(articles_links)

        
        #for category in all_categories_pages:
         #   category_pages.append(category)
    #     articles_links = get_articles_links()
    #     create_csv_file()
    print('All categories scraped')

scraping_all_categories()

