from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import api_calls
import os
app = Flask(__name__)

# Simulated data for demonstration
data = []

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/', methods=['POST'])
def search():
    if request.method == 'POST':
        search_query1 = request.form.get('search1', '').strip()
        search_query2 = request.form.get('search2', '').strip()
        search_query3 = request.form.get('search3', '').strip()  # Optional search field 3
        if (search_query3 == ""):
            search_query3 = []
        search_query4 = request.form.get('search4', '').strip()  # Optional search field 4
        search_query5 = request.form.get('search5', '').strip()  # Optional search field 5

    if not search_query1 or not search_query2:
        error_message = "Search fields 1 and 2 cannot be empty."
        return jsonify({'error': error_message}), 400

        # Process the search queries here
    payload = {
                "legal_names": search_query3,
                "commercial_names": [search_query1],
                "address_txt": search_query4,
                "phone_number": search_query5,
                "website": search_query2
            }
    # Save the search_data to a JSON file
    with open('data.json', 'w') as file:
        json.dump(payload, file)
        data = []
    print("Data saved successfully.")
    while True:
        if (os.stat("output.json").st_size == 0):
            continue
        with open('output.json', 'r') as file:
            data = json.load(file)
        break

    for entry in data:  # Iterate over dictionaries in the list
        # Access the score from the dictionary
        score = entry.get("score")

        if score is not None:  # Check if the "score" key exists in the dictionary
            # Convert the score to a float
            score_float = float(score)

            # Round the score to a maximum of 2 decimals
            score_rounded = round(score_float, 2)

            print(score_rounded)

            # Modify the dictionary with the rounded score
            entry["score"] = score_rounded
        print(data)
        redirect(url_for('search'))
            
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
