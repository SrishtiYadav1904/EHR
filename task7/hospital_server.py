from xmlrpc.server import SimpleXMLRPCServer
import threading
import time

# -------------------------
# Datasets
# -------------------------
patients = [
    {"id": 1, "name": "Aarav", "age": 25, "gender": "M", "disease": "Flu", "medicines": "Paracetamol", "blood": "O+"},
    {"id": 2, "name": "Srishti", "age": 22, "gender": "F", "disease": "Diabetes", "medicines": "Metformin", "blood": "A+"},
    {"id": 3, "name": "Vikram", "age": 30, "gender": "M", "disease": "Asthma", "medicines": "Inhaler", "blood": "B+"},
    {"id": 4, "name": "Neha", "age": 27, "gender": "F", "disease": "Hypertension", "medicines": "Amlodipine", "blood": "AB+"},
    {"id": 5, "name": "Rahul", "age": 40, "gender": "M", "disease": "Covid-19", "medicines": "Remdesivir", "blood": "O-"},
]

doctors = [
    {"doc_id": 101, "name": "Dr. Mehta", "age": 45, "gender": "M", "specialization": "Cardiologist"},
    {"doc_id": 102, "name": "Dr. Sharma", "age": 38, "gender": "F", "specialization": "Pulmonologist"},
]

# -------------------------
# Buffer
# -------------------------
BUFFER_CAPACITY = 5
patient_buffer = []
buffer_lock = threading.Lock()

# -------------------------
# Clone function (internal)
# -------------------------
def clone_patient_request(patient_id):
    """Handles overflow requests internally"""
    print(f"[CLONE] Handling Patient ID {patient_id} internally")
    time.sleep(0.1)  # simulate processing delay
    for p in patients:
        if p["id"] == patient_id:
            return {"status": "notice", "msg": f"Patient ID {patient_id} has requested their record"}
    return {"status": "error", "msg": "Patient not found"}

# -------------------------
# RPC Functions
# -------------------------
def exchange():
    return "Secure Patient Record Exchange Server Running..."

def doctor(doc_id, patient_id):
    for doc in doctors:
        if doc["doc_id"] == doc_id:
            for p in patients:
                if p["id"] == patient_id:
                    return {"status": "success", "record": p}
            return {"status": "error", "msg": "Patient not found"}
    return {"status": "error", "msg": "Doctor not authorized"}

def patient(patient_id):
    """Patient requests handled with buffer & transparent clone"""
    with buffer_lock:
        if len(patient_buffer) < BUFFER_CAPACITY:
            patient_buffer.append(patient_id)
            if len(patient_buffer) == int(0.9 * BUFFER_CAPACITY):
                print(f"[WARNING] Buffer ≥90% full! Next requests may go to clone")
            print(f"[MAIN] Patient ID {patient_id} handled by main buffer")
            return {"status": "notice", "msg": f"Patient ID {patient_id} has requested their record"}
        else:
            # Buffer full → handled by clone internally
            return clone_patient_request(patient_id)

# -------------------------
# Start RPC Server
# -------------------------
server = SimpleXMLRPCServer(("0.0.0.0", 8000))
print("Exchange server (with internal clone) started at port 8000...")

server.register_function(exchange, "exchange")
server.register_function(doctor, "doctor")
server.register_function(patient, "patient")

server.serve_forever()