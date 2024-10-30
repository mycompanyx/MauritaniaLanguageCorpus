from flask import Flask, render_template, request, redirect, url_for
import redis
import random
from cassandra.cluster import Cluster

# Initialize Flask app
app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Change if your Cassandra instance is on a different host
session = cluster.connect('corpus')

@app.route('/')
def index():
    # Fetch a random sentence from Redis
    sentence_key = random.choice(r.keys('*'))  
    key_type = r.type(sentence_key)
    print(f"The type of the key '{sentence_key}' is: {key_type}")

    sentence = r.get(sentence_key)  # Get the sentence value
    return render_template('index.html', sentence=sentence, sentence_key=sentence_key)

@app.route('/submit_translation', methods=['POST'])
def submit_translation():
    if request.method == 'POST':
        sentence_key = request.form['sentence_key']
        translation = request.form['translation']
        
        # Store the sentence and its translation in Cassandra
        original_sentence = r.get(sentence_key)
        
        # Prepare the CQL statement
        cql = "INSERT INTO translations (sentence_key, original, translation) VALUES (%s, %s, %s)"
        session.execute(cql, (sentence_key, original_sentence, translation))

        print(f"Stored in Cassandra: {sentence_key}, Original: {original_sentence}, Translation: {translation}")
        
        # Redirect to the main page to show the next sentence
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
