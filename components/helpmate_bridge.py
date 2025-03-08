import os
import subprocess
import threading
import streamlit as st
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS

app = Flask(__name__, static_folder='../Helpmate-AI/dist')
# Configure CORS to allow embedding in iframe from any origin
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})

@app.route('/')
def serve_helpmate():
    """Serve the Helpmate-AI React frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from the React app's build directory"""
    return send_from_directory(app.static_folder, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests and integrate with coderAI's backend services"""
    data = request.json
    question = data.get('question')
    
    # Here we'll integrate with coderAI's model service
    try:
        # Access the model service from the imported st session state
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx():
            model_service = st.session_state.model_service
            response = model_service.generate_response(question)
            return jsonify({'answer': response})
        else:
            return jsonify({'answer': 'Unable to access Streamlit session state. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def check_helpmate_build():
    """Check if Helpmate-AI is built, and build it if not"""
    if not os.path.exists(app.static_folder):
        # Build the React app
        try:
            print("Building Helpmate-AI React app...")
            subprocess.run(
                ["npm", "run", "build"], 
                cwd=os.path.join(os.getcwd(), "../Helpmate-AI"),
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to build Helpmate-AI: {str(e)}")
            return False
    return True

def run_flask_app():
    """Run the Flask app in a separate thread"""
    # Set Flask server headers to allow iframe embedding
    @app.after_request
    def add_header(response):
        response.headers['X-Frame-Options'] = 'ALLOW-FROM *'
        response.headers['Content-Security-Policy'] = "frame-ancestors *"
        return response
        
    app.run(host='0.0.0.0', port=5173, debug=False, use_reloader=False)

def init_helpmate_bridge():
    """Initialize the Helpmate-AI bridge"""
    # Ensure the static folder exists or build it
    if not os.path.exists(app.static_folder):
        if not check_helpmate_build():
            raise Exception('Helpmate-AI build directory not found and build failed. Please build the React app manually.')
    
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Helpmate-AI bridge initialized on port 5173")
    return flask_thread