from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Lock
import json
from collections import deque # New import for an efficient log
import datetime # New import for timestamps

app = Flask(__name__)
CORS(app)

# --- Database Setup ---
DB_FILE = "database.json"
patients = []
doctors = []
db_lock = Lock()

# --- NEW: Live Server Log ---
# We'll use a deque to keep a capped-size log of the last 50 events.
server_log = deque(maxlen=50)

def add_log(message):
    """Adds a timestamped message to the server log."""
    timestamp = datetime.datetime.now().strftime("%I:%M:%S %p")
    server_log.appendleft({"time": timestamp, "message": message}) # appendleft to show newest first

# --- Database Functions ---
def load_db():
    global patients, doctors
    with db_lock:
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                patients = data.get("patients", [])
                doctors = data.get("doctors", [])
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle case where DB file doesn't exist
            save_db() # This will create an empty one
    add_log("Server started and database loaded.")

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump({"patients": patients, "doctors": doctors}, f, indent=4)

# --- API Endpoints for Clients (doctor.html, patient.html) ---
@app.route("/api/get_patient_record", methods=["POST"])
def get_patient_record():
    patient_id = request.json.get("patient_id")
    with db_lock:
        record = next((p for p in patients if p["id"] == patient_id), None)
        if record:
            return jsonify(record)
        return jsonify({"error": "Patient not found"}), 404

@app.route("/api/get_all_patients", methods=["GET"])
def get_all_patients():
    with db_lock:
        return jsonify(patients)

@app.route("/api/get_doctor_details", methods=["POST"])
def get_doctor_details():
    doctor_id = request.json.get("doctor_id")
    with db_lock:
        record = next((d for d in doctors if d["doc_id"] == doctor_id), None)
        if record:
            return jsonify(record)
        return jsonify({"error": "Doctor not found"}), 404

@app.route("/api/update_patient_record", methods=["POST"])
def update_patient_record():
    patient_id = request.json.get("patient_id")
    new_data = request.json.get("new_data")
    
    # NEW: Log the update event
    add_log(f"Received update request for Patient ID: {patient_id}")
    
    with db_lock:
        index = next((i for i, p in enumerate(patients) if p["id"] == patient_id), -1)
        if index != -1:
            patients[index].update(new_data)
            save_db()
            add_log(f"Successfully updated Patient ID: {patient_id}")
            return jsonify({"message": f"Patient {patient_id} updated successfully."})
        
        add_log(f"Update failed: Patient ID {patient_id} not found.")
        return jsonify({"error": "Patient not found"}), 404

# --- NEW: API Endpoints for Monitoring Dashboard (server.html) ---

@app.route("/api/get_database_overview", methods=["GET"])
def get_database_overview():
    """Returns a snapshot of the entire database for the dashboard."""
    with db_lock:
        return jsonify({"patients": patients, "doctors": doctors})

@app.route("/api/get_server_log", methods=["GET"])
def get_server_log():
    """Returns the latest server log events."""
    return jsonify(list(server_log))

# --- Server Startup ---
if __name__ == "__main__":
    load_db()
    app.run(host="0.0.0.0", port=9000)