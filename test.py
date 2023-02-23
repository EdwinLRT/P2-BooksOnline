import requests



def test(): 
    category_pages = []
    page = 1    
    while True : 
        url = 'https://books.toscrape.com/'+'catalogue/category/books/mystery_3/'+'page-'+str(page)+'.html'
        if 'page-1.html' in url :
            url = url.replace('page-1.html', 'index.html')

        response = requests.get(url)
        if response.status_code == 200:
            print(f"Page {page} : {url}")
            category_pages.append(url)
            page += 1
        else:
            print(category_pages)
            break
        
    

test()

# def get_all_category_pages() :
#  # cat_url = 'https://books.toscrape.com/'+'catalogue/category/books/mystery_3'+'page-'+str(page)+'.html'

#     page = 1
    

#     while response.ok :



#     else : print('404')
    


    # Tant que réponse = 200 alors incrementer 
                # pages= np.arange(1,11)
            # for page in pages : 
            #     cat_url = 'https://books.toscrape.com/'+href+'page-'+str(page)+'.html'
            #     print(cat_url)