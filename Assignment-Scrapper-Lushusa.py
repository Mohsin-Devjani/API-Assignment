import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, jsonify, request

# Initialize Flask application
app = Flask(__name__)

# Create dictionary to store product information
products_dict = {
        "name":[],
        "link":[],
        "tagline":[],
        "size":[],
        "price":[]
    }

# Route for the main page of the application
@app.route(rule='/', methods=['GET'])
def main():
    return "Welcome to Scrappy World"

# Route for scraping product information from Lush USA website
@app.route(rule='/lushusa/<string:keyword>/', methods=['GET'])
def get_product_info(keyword):
    """
    Scrape product information from Lush USA website based on the given keyword
    :param keyword: keyword to search for products on Lush USA website
    :return: JSON object containing the scraped product information
    """
    # Create base URL for searching products on Lush USA website
    keywords = 'q='+keyword
    base_url = "https://www.lushusa.com/search?"+ keywords
    # Send GET request to Lush USA website
    response = requests.get(url=base_url)
    # Parse the HTML content of the response
    soup = BeautifulSoup(response.text, "html.parser")
    # Check if there is a "Load More" button to load more products
    more_result = soup.find('button',class_ = 'btn btn-outline-primary col-12 col-sm-4 more')
    
    # Loop to load more products until there are no more "Load More" buttons
    while (True):
        if(type(more_result) == type(None)):
            break
        # Extract the URL to load more products
        concat_str = more_result['data-url'].split(keywords)
        base_url2 = base_url +concat_str[1]
        # Send GET request to load more products
        response = requests.get(url=base_url2)
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.text, "html.parser")
        # Check if there is a "Load More" button to load more products
        more_result = soup.find('button',class_ = 'btn btn-outline-primary col-12 col-sm-4 more')

    # Clear product dictionary
    products_dict = {
        "name":[],
        "link":[],
        "tagline":[],
        "size":[],
        "price":[]
    }
    try:
        # Find all product information in the HTML content
        lists = soup.find_all('div',class_ = 'product-tile-body d-flex flex-column position-relative w-100 h-100 text-center')
        len(lists)
        for i,plist in enumerate(lists):
            print(i)
            name_div = plist.find('h3', class_= 'product-tile-name')
            print(name_div)
            product_name = name_div.text.replace('\n','')
            product_link = 'https://www.lushusa.com'+name_div.find('a')['href']
            product_tagline = plist.find('div', class_ = 'product-tile-tagline d-none black mb-2 text-center smaller-font-size d-md-block').text
            print(product_tagline)
            available_prices = plist.find('span', class_ = 'tile-price align-middle font-weight-bold').text
            print(available_prices)
            available_sizes = plist.find('span',class_ = 'tile-size align-middle smaller-font-size mr-2').text.replace(' / ','')
            print(available_sizes)
            products_dict['name'].append(product_name)
            products_dict['link'].append(product_link)
            products_dict['tagline'].append(product_tagline)
            products_dict['size'].append(available_sizes)
            products_dict['price'].append(available_prices)

        file_name = keyword +'.csv'
        pd.DataFrame(products_dict).to_csv(file_name)
        return jsonify(products_dict)
    except:
        return "Sorry Cant Fetch Info requested"

if __name__=='__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)