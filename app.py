from flask import Flask, jsonify
import os, json, firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
firebase_creds = json.loads(os.environ["FIREBASE_CREDS"])
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/",methods=["GET","HEAD"])
def home():
    print("Ping received at:", datetime.now())
    return jsonify({"status": "Backend is running"}),200

@app.route("/add_sample")
def add_sample():
    # Add a sample document to Firestore
    doc_ref = db.collection("samples").document()
    doc_ref.set({
        "message": "Hello from Flask & Firebase!",
        "timestamp": datetime.now()
    })
    return jsonify({"status": "Document added"})

@app.route("/get_samples")
def get_samples():
    docs = db.collection("samples").stream()
    data = [{doc.id: doc.to_dict()} for doc in docs]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
