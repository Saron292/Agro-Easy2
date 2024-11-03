from flask import Flask, render_template, jsonify, request
import requests
import google.generativeai as genai
import os
import ssl
print(ssl.OPENSSL_VERSION)

genai.configure(api_key=os.environ["GENAI_API_KEY"])

app = Flask(__name__)

API_KEY = 'ba289a817457428cb6a2b16507698f3d'


def fetch_news(query):
    response = requests.get(f'https://newsapi.org/v2/everything?q={query}&from=2024-10-03&sortBy=publishedAt&apiKey={API_KEY}')
    return response.json()  # Returns the news data as a JSON object

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    data= request.get_json()
    products = data.get('products')

    print(f"Received products for recommendation: {products}")

    prompt = (
        f"Based on the following products: {products}, provide safe and effective "
        "step-by-step instructions for using these products in pest control, "
        "formatted as follows: First: Materials Needed, Next: Mix, Then: Application, "
        "Finally: Important Notes. Emphasize safety and effectiveness.limited to "
        "less than 2000 characters."
    )
    

    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the appropriate Gemini model
    response = model.generate_content(prompt)

    print(f"Model response: {response.text}")
        
    recommendation = response.text.splitlines()
    return jsonify({'recommendations': recommendation})

@app.route('/get-crop-recommendations', methods=['POST'])
def get_crop_recommendations():
    data = request.get_json()
    land_size = data.get('landSize')
    location = data.get('location')
    
    season = data.get('season')

    print(f"Received data for crop recommendation: Land Size: {land_size}, Location: {location}, Season: {season}")

    prompt = (
        f"Based on the following data: Land Size: {land_size} acres, Location: {location}, "
        f"Season: {season}, provide recommendations for suitable crops to plant, "
        "formatted as follows: Recommended Crops: [Crop1, Crop2, ...]. Include any important notes. "
        "Limit response to less than 2000 characters."
    )

    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the appropriate Gemini model
    response = model.generate_content(prompt)

    print(f"Model response: {response.text}")

    crop_recommendations = response.text.strip()
    return jsonify({'crop_recommendations': crop_recommendations})

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/news/<topic>')
def news(topic):

    news_data = fetch_news(topic)
    return jsonify(news_data)


if __name__ == '__main__':
    app.run(port=5001)
