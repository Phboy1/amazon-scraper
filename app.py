import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load environment variables
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

        for result in response.get("organic_results", []):
            title = result.get("title", "No title")
            price_str = result.get("price", "No price")
            thumbnail = result.get("thumbnail", "https://via.placeholder.com/100")  
            link = result.get("link", "#")  

            items.append({
                "title": title,
                "price": price_str,
                "thumbnail": thumbnail,
                "link": link
            })

            try:
                price = float(price_str.replace("$", "").replace(",", ""))
                total_price += price
                count += 1
            except:
                continue

        if count > 0:
            average = total_price / count 
        else: 
            average = 0

        return render_template("results.html", keyword=keyword, items=items, average=average)

    return render_template("index.html")
