from flask import Flask, render_template_string, url_for
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import os
import random

app = Flask(__name__)

# Azure Cosmos DB configuration
url = "https://aifacetest.documents.azure.com:443/"
key = "WOEPydZ8aUEJBM3kVcViJnwPeT1WgsieJCPCHhXo1zgbRJiwSgxzivpZJw0yvxXps8PYSLEHlPdlACDbbpnGJQ=="
client = CosmosClient(url, credential=key)
database = client.get_database_client("GuessingGameDB")
container = database.get_container_client("GuessStatistics")

@app.route('/')
def show_images():
    local_image_filename = random.choice(os.listdir("static"))
    local_image_path = url_for('static', filename=local_image_filename)

    web_image_url = "https://thispersondoesnotexist.com"

    images = [
        {"id": "local_image", "src": local_image_path, "callback": "submitGuess('local_image')"},
        {"id": "web_image", "src": web_image_url, "callback": "submitGuess('web_image')"}
    ]
    random.shuffle(images)

    stats = get_stats() # Fetch statistics from DB
    return render_template_string("""...""",
                                  correct_guesses=stats['correct'], incorrect_guesses=stats['incorrect'],
                                  ...)

@app.route('/submit/<guess>')
def submit_guess(guess):
    if guess == "local_image":
        # Increment correct guess in the database
        update_stats(True)
    else:
        # Increment incorrect guess in the database
        update_stats(False)

    return jsonify(success=True)

def get_stats():
    # Fetch the statistics from Azure Cosmos DB.
    # If not present, initialize with zeros.
    try:
        item = container.read_item(item="stats", partition_key="stats")
        return item
    except exceptions.CosmosResourceNotFoundError:
        container.create_item(body={"id": "stats", "correct": 0, "incorrect": 0, "partitionKey": "stats"})
        return {"correct": 0, "incorrect": 0}

def update_stats(is_correct):
    stats = get_stats()
    if is_correct:
        stats["correct"] += 1
    else:
        stats["incorrect"] += 1
    container.replace_item(item=stats, body=stats)

if __name__ == "__main__":
    app.run(port=8080)

