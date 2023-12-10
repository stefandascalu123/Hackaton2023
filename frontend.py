from flask import Flask, render_template, request
import json
import api_calls
app = Flask(__name__)

# Simulated data for demonstration
data = [
    {"score": 0.84, "country": "Country A", "city": "City A"},
    {"score": 0.66, "country": "Country B", "city": "City B"},
    {"score": 0.43, "country": "Country C", "city": "City C"},
    {"score": 0.91, "country": "Country D", "city": "City D"},
    {"score": 0.75, "country": "Country E", "city": "City E"}
]

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_query1 = request.form.get('search1', '').strip()
        search_query2 = request.form.get('search2', '').strip()
        search_query3 = request.form.get('search3', '').strip()  # Optional search field 3
        search_query4 = request.form.get('search4', '').strip()  # Optional search field 4
        search_query5 = request.form.get('search5', '').strip()  # Optional search field 5

    if not search_query1 or not search_query2:
        error_message = "Search fields 1 and 2 cannot be empty."
        return jsonify({'error': error_message}), 400

        # Process the search queries here
    payload = {
                "legal_names": search_query3,
                "commercial_names": search_query1,
                "address_txt": search_query4,
                "phone_number": search_query5,
                "website": search_query2
            }
    # Save the search_data to a JSON file
    with open('data.json', 'w') as file:
        json.dump(payload, file)
    return f"You searched for: {search_query1} and {search_query2}"

if __name__ == '__main__':
    app.run(debug=True)
