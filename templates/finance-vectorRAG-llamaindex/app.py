from flask import Flask, request, jsonify, render_template, url_for, redirect, session
import os

# Import the RAG chatbot and the VectorDatabase class
from rag_public_finance import RAG, VectorDatabase

# Create a vector database object
vector_database = VectorDatabase()

# Create a RAG chatbot object
rag = RAG(vector_database)

# Flask setup
app = Flask(__name__)

##############################################################################################################################
#                                                   Flask Routes                                                             #
##############################################################################################################################

@app.route("/")
def index():
    # Home page
    messages = rag.messages
    return render_template("index.html", messages=messages, model=rag.vector_database.settings.llm.model)

@app.route("/add_input", methods=["POST", "GET"])
def add_input():
    # Process user input
    user_query = request.form["question"]
    rag.respond(user_query)
    return redirect(url_for("index"))

@app.route("/switch_model", methods=["POST", "GET"])
def switch_model():
    # Switch the model
    model = request.form.get("model")
    rag.switch_model(model)
    return redirect(url_for("index"))

@app.route("/reset", methods=["POST", "GET"])
def reset():
    rag.reset_history()
    return redirect(url_for("index"))

# Run app in development mode
if __name__ == "__main__": 
    app.run(debug=True, port=8080)