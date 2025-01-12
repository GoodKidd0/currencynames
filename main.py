from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Access the API key from the environment variable
api_key = os.getenv('API_KEY')
endpoint = 'http://api.marketstack.com/v1/currencies'


@app.route('/', methods=['GET', 'POST'])
def index():
    currency_data = None
    if request.method == 'POST':
        search_query = request.form['currency_name'].lower()
        params = {
            'access_key': api_key
        }
        response = requests.get(endpoint, params=params)
        print("API Response Status Code:", response.status_code)  # Debugging
        print("API Response JSON:", response.json())  # Debugging

        if response.status_code == 200:
            data = response.json()
            # Filter results manually and keep the symbol in the filtered data
            currency_data = [
                currency for currency in data['data']
                if search_query in currency['name'].lower()
            ]
            print("Filtered Currency Data:", currency_data)  # Debugging
        else:
            currency_data = {'error': f'Error: {response.status_code}'}

    # Print currency_data before passing to the template
    print("Currency Data Sent to Template:", currency_data)

    return render_template('index.html', currency_data=currency_data)


if __name__ == '__main__':
    app.run(debug=True)
