import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form.get('keyword')

        parameters = {
            "engine": "amazon",
            "k": keyword,
            "api_key": SERPAPI_API_KEY
        }

        response = requests.get("https://serpapi.com/search", params=parameters).json()

        items = []
        total_price = 0
        count = 0
        best_deal = None
        lowest = float('inf')

        for result in response.get("organic_results", []):
            title = result.get("title", "No title")
            price_str = result.get("price", "No price")
            thumbnail = result.get("thumbnail", "https://via.placeholder.com/100")  
            link = result.get("link", "#")  

            item = {
                "title": title,
                "price": price_str,
                "thumbnail": thumbnail,
                "link": link
            }

            items.append(item)

            try:
                price = float(price_str.replace("$", "").replace(",", ""))
                total_price += price
                count += 1
                if price < lowest:
                    lowest = price
                    best_deal = item
            except:
                continue

        if count > 0:
            average = total_price / count 
        else: 
            average = 0

        return render_template("results.html", keyword=keyword, items=items, average=average, best_deal=best_deal)

    return render_template("index.html")
