from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5


app = Flask(__name__)
bootstrap = Bootstrap5(app)

load_dotenv()
API_KEY = os.getenv('API_KEY')
# print('spoonacular api key:', os.getenv('API_KEY'))
BASE_URL = 'https://api.spoonacular.com/recipes'

@app.route('/')
def home():
    response = requests.get(f'{BASE_URL}/random', params={'apiKey': API_KEY, 'number': 5})
    trending_recipes = response.json()
    return render_template('index.html', trending=trending_recipes)

@app.route('/search', methods=['GET','POST'])
def search():
    ingredients = request.form.get('ingredients')
    if not ingredients:
        return 'Please enter ingredients'

    params = {
        'apiKey': API_KEY,
        'ingredients': ingredients,
        'number': 5
    }
    response = requests.get(f'{BASE_URL}/findByIngredients', params=params)
    if response.status_code == 401:
        return 'Unauthorized. Please check your API key'

    data = response.json()
    print('recipe response', data)

    return render_template('results.html', recipes=data)

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    response = requests.get(f'{BASE_URL}/{recipe_id}/information', params={'apiKey': API_KEY})
    recipe_details = response.json()
    return render_template('recipe.html', recipes=recipe_details)

@app.route('/random')
def random_recipes():
    response = requests.get(f'{BASE_URL}/random', params={'apiKey': API_KEY, 'number':5})
    random_data = response.json().get('recipes', [])[0]
    return render_template('recipe.html', recipes=random_data)


if __name__ == '__main__':
    app.run(debug=True)