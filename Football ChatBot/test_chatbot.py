# test_chatbot.py
# FBref Bot
#
# Interactive terminal-based interface to test the chatbot locally.

from app.chatbot import handle_query  # Import the chatbot's main handler function

# Display a welcome message
print("🧠 Football Stats Chatbot (type 'exit' to quit)\n")

# Run a continuous input loop until the user types 'exit' or 'quit'
while True:
    user_input = input("🗣 You: ")

    # Check for exit command
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # Process the user query using the chatbot
    response = handle_query(user_input)

    # Display the chatbot's reply
    print(f"🤖 Bot: {response}\n")
