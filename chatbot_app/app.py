from flask import Flask, request, jsonify, render_template
from google.cloud import aiplatform_v1beta1
import os
from dotenv import load_dotenv
import vertexai
from vertexai.preview import reasoning_engines
import uuid
from functools import wraps
load_dotenv()

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Initializing VertexAI
vertexai.init(
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION"),
    staging_bucket=os.getenv("STAGING_BUCKET")
    )


ENGINE_NAME = os.getenv("ENGINE_NAME")

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/new_session", methods=["GET"])
def new_session():
    """
    Membuat sesi baru dan mengembalikan session ID.
    """
    session_id = str(uuid.uuid4())  # Buat session ID baru
    return jsonify({
        "session_id": session_id,
        "message": "Halo! Saya Eca. Saya di sini untuk membantu Anda."
    })
        
@app.route("/chat", methods=["POST"])
@require_api_key
def chat():
    data = request.json
    query = data.get("query")
    session_id = data.get("session_id", "default")

    engine = reasoning_engines.ReasoningEngine(ENGINE_NAME)
    response = engine.query(
        input=query,
        config={"configurable":{"session_id":session_id}}
    )

    return jsonify({"response": response['output']})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


