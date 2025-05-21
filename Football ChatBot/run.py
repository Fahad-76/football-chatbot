#
#  run.py
#  FBref Bot
#
#  Created by Fahad on 20/05/2025.
#
#  This is the main entry point to start the Flask API server for the FBref Bot.

from app.api import app  # Import the Flask app instance from the API module

# Only run the app if this file is executed directly (not when imported)
if __name__ == "__main__":
    # Start the Flask development server with debug mode enabled
    app.run(debug=True)
