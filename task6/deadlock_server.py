 
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading
import copy
import pprint
import queue
import time

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
# Priority setup
# Higher number = higher priority
# Doctors > Patients (higher patient_id = higher priority)
# -------------------------
def get_priority(role, id_):
    if role == "doctor":
        return 100 + id_  # doctors always higher than patients
    elif role == "patient":
        return id_  # patient priority based on id
    else:
        return 0

# -------------------------
# Lock and Queue
# -------------------------
db_lock = threading.Lock()
waiting_queue = queue.PriorityQueue()  # stores (priority, timestamp, caller info)
current_editor = None  # who is editing now
pp = pprint.PrettyPrinter(indent=2)

def print_db(title="Current Database"):
    print(f"\n--- {title} ---")
    for p in patients:
        pp.pprint(p)

def acquire_lock(role, id_):
    global current_editor
    prio = -get_priority(role, id_)  # negative because PriorityQueue pops smallest first
    event = threading.Event()
    waiting_queue.put((prio, time.time(), (role, id_, event)))
    print(f"[QUEUE] {role.title()} {id_} is waiting with priority {abs(prio)}")

    while True:
        with db_lock:
            top_prio, _, top_info = waiting_queue.queue[0]
            if top_info[0] == role and top_info[1] == id_:
                current_editor = (role, id_)
                waiting_queue.get()
                print(f"[LOCK ACQUIRED] {role.title()} {id_} is now editing")
                return
        event.wait(0.1)  # wait and check again

def release_lock(role, id_):
    global current_editor
    with db_lock:
        if current_editor == (role, id_):
            print(f"[LOCK RELEASED] {role.title()} {id_} finished editing")
            current_editor = None
            # notify all waiting threads
            for _, _, (_, _, ev) in list(waiting_queue.queue):
                ev.set()

# -------------------------
# Functions
# -------------------------
def doctor(id_, patient_id, edits):
    acquire_lock("doctor", id_)
    try:
        for p in patients:
            if p["id"] == patient_id:
                p.update(edits)
                print_db(f"After Doctor {id_} edited Patient {patient_id}")
                return {"status": "success", "message": f"Doctor {id_} updated Patient {patient_id}"}
        return {"status": "fail", "message": "Patient not found"}
    finally:
        release_lock("doctor", id_)

def patient(id_, edits):
    acquire_lock("patient", id_)
    try:
        for p in patients:
            if p["id"] == id_:
                # patients can only edit certain fields
                allowed = {"name", "age", "gender"}
                safe_edits = {k:v for k,v in edits.items() if k in allowed}
                p.update(safe_edits)
                print_db(f"After Patient {id_} edited self")
                return {"status": "success", "message": f"Patient {id_} updated self"}
        return {"status": "fail", "message": "Patient not found"}
    finally:
        release_lock("patient", id_)

def exchange():
    # just show current DB
    print_db("Exchange - current state")
    return copy.deepcopy(patients)

# -------------------------
# Server startup
# -------------------------
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9000
    with ThreadedXMLRPCServer((HOST, PORT), allow_none=True) as server:
        server.register_function(doctor, "doctor")
        server.register_function(patient, "patient")
        server.register_function(exchange, "exchange")
        print(f"[SERVER] Running on {HOST}:{PORT}")
        server.serve_forever()