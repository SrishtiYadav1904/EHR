from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading
import time
import copy
from queue import PriorityQueue
import pprint
import socket

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# -------------------------
# Database
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
# Locks & Queue
# -------------------------
db_lock = threading.Lock()
editing = None
request_queue = PriorityQueue()
pp = pprint.PrettyPrinter(indent=2)

# Helper to update patient info
def update_patient(patient_id, edits):
    for p in patients:
        if p["id"] == patient_id:
            p.update(edits)
            return True
    return False

# -------------------------
# Functions
# -------------------------
def doctor(doc_id, patient_id, edits):
    timestamp = time.time()
    priority = 1  # doctor highest priority
    req = {"type": "doctor", "id": doc_id, "patient_id": patient_id, "edits": edits, "timestamp": timestamp}
    request_queue.put((priority, timestamp, req))
    print(f"[REQUEST] Doctor {doc_id} wants to edit Patient {patient_id} at {timestamp}")
    return handle_request(req)

def patient(patient_id, edits):
    timestamp = time.time()
    priority = 2 + patient_id  # patient priority by ID
    req = {"type": "patient", "id": patient_id, "patient_id": patient_id, "edits": edits, "timestamp": timestamp}
    request_queue.put((priority, timestamp, req))
    print(f"[REQUEST] Patient {patient_id} wants to edit at {timestamp}")
    return handle_request(req)

def exchange():
    return copy.deepcopy(patients)

# -------------------------
# Handle request with mutual exclusion
# -------------------------
def handle_request(req):
    global editing
    while True:
        with db_lock:
            if editing is None:
                first_in_queue = request_queue.queue[0][2]
                if first_in_queue == req:
                    editing = req
                    request_queue.get()
                    print(f"[EDITING] {req['type'].title()} {req['id']} editing Patient {req['patient_id']}")
                    success = update_patient(req['patient_id'], req.get("edits", {}))
                    time.sleep(2)  # simulate edit time
                    print(f"[DONE] {req['type'].title()} {req['id']} finished editing Patient {req['patient_id']}")
                    editing = None
                    return {"status": "success", "message": f"{req['type'].title()} {req['id']} updated Patient {req['patient_id']}"}
            else:
                print(f"[WAITING] {req['type'].title()} {req['id']} waiting. Currently editing: {editing['type'].title()} {editing['id']}")
        time.sleep(1)

# -------------------------
# Start Server
# -------------------------
def get_local_ip():
    """Detects the local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    HOST, PORT = get_local_ip(), 9000
    print(f"[INFO] Binding server to {HOST}:{PORT}")
    with ThreadedXMLRPCServer((HOST, PORT), allow_none=True) as server:
        server.register_function(doctor, "doctor")
        server.register_function(patient, "patient")
        server.register_function(exchange, "exchange")
        print(f"[SERVER] Running on {HOST}:{PORT}")
        server.serve_forever()