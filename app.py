import requests
import os
import json
from flask import Flask, render_template, request  

app = Flask(__name__)

SERPAPI_API_KEY = "YOUR_SERPAPI_GOES_HERE"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form.get('keyword')

        parameters = {
            "apikey": SERPAPI_API_KEY,
            "engine": "amazon",
            "k": keyword
        }

        search = requests.get("https://serpapi.com/search", params=parameters)
        response = search.json()
        counter = 0
        total_price = 0

        items = []
        for result in response.get("organic_results", []):
            title = result.get("title", "No title")
            price_str = result.get("price", "No price")
            thumbnail = result.get("thumbnail", "No image")

            items.append({"title": title, "price": price_str, "thumbnail": thumbnail})

            try:
                price = float(price_str.replace("$", "").replace(",", ""))
                total_price += price
                counter += 1
            except:
                continue


        if counter > 0:
            average = total_price / counter 
        else: 
            average = 0

        return render_template("results.html", keyword=keyword, items=items, thumbnail=thumbnail, average=average)

    return render_template("index.html")