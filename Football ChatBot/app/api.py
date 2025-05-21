#
#  api.py
#  FBref Bot
#
#  Created by Fahad on 20/05/2025.
#
#  This file sets up a Flask web API that accepts football-related user queries via POST
#  and returns player stats using the chatbot module.

from flask import Flask, request, jsonify
from app.chatbot import handle_query  # Import the chatbot's query handler

# Initialize the Flask web app
app = Flask(__name__)

# Define an endpoint that handles POST requests at /query
@app.route("/query", methods=["POST"])
def query():
    # Get JSON data sent in the request
    data = request.get_json()

    # Validate that 'query' field exists in the request body
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' in request body."}), 400

    # Extract the actual query string
    user_input = data["query"]

    # Let the chatbot process the input and get a reply
    response = handle_query(user_input)

    # Return the chatbot's reply in JSON format
    return jsonify({"reply": response})
