from flask import Flask, Response, request
import requests
from flask_cors import CORS
from chatbot import Chatbot

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # allow all origins

chatbot = None

with app.app_context():
    chatbot = Chatbot()
    print("Setup done")

@app.teardown_appcontext
def cleanup():
    global chatbot
    chatbot.cleanup()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    # 1. Get user query
    query = data.get('query', '')

    # 2. Classify intent
    intent = chatbot.intent_classfier.predict_intent(query)
    print("intent:", intent)
    payload = ""
    if intent == "general":
        # 3a. Create general prompt
        payload = chatbot.llm.get_general_payload(query)

    else:
        # 3b1,2. Search query
        db_results =  chatbot.search_engine.search(query)
        payload = chatbot.llm.get_db_search_payload(db_results, query)


    #4. Generate response    
    def generate():
        with requests.post(chatbot.ollama_api, json=payload, stream=True) as resp:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                   yield chunk

    return Response(generate(), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)