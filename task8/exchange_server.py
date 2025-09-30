from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading
import copy
import pprint

# Threaded server
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# -------------------------
# Patient dataset
# -------------------------
MASTER_DB = {
    "patients": [
        {"id": 1, "name": "Aarav", "age": 25, "gender": "M", "disease": "Flu", "medicines": "Paracetamol", "blood": "O+"},
        {"id": 2, "name": "Srishti", "age": 22, "gender": "F", "disease": "Diabetes", "medicines": "Metformin", "blood": "A+"},
        {"id": 3, "name": "Vikram", "age": 30, "gender": "M", "disease": "Asthma", "medicines": "Inhaler", "blood": "B+"},
        {"id": 4, "name": "Neha", "age": 27, "gender": "F", "disease": "Hypertension", "medicines": "Amlodipine", "blood": "AB+"},
        {"id": 5, "name": "Rahul", "age": 40, "gender": "M", "disease": "Covid-19", "medicines": "Remdesivir", "blood": "O-"},
    ],
    "doctors": [
        {"doc_id": 101, "name": "Dr. Mehta", "age": 45, "gender": "M", "specialization": "Cardiologist"},
        {"doc_id": 102, "name": "Dr. Sharma", "age": 38, "gender": "F", "specialization": "Pulmonologist"},
        {"doc_id": 103, "name": "Dr. Joshi", "age": 50, "gender": "M", "specialization": "General Medicine"}
    ]
}

# Create replicas of database
REPLICAS = [copy.deepcopy(MASTER_DB) for _ in range(3)]
db_lock = threading.Lock()
pp = pprint.PrettyPrinter(indent=2)

def print_replicas(title):
    print(f"\n--- {title} ---")
    for i, r in enumerate(REPLICAS, 1):
        print(f"Replica {i}:")
        pp.pprint(r)

def update_patient_in_replica(replica, patient_id, fields):
    for p in replica["patients"]:
        if p["id"] == patient_id:
            p.update(fields)
            return True
    return False

# -------------------------
# Doctor function
# -------------------------
def doctor(doctor_id, patient_id, edits):
    results = []
    updated_any = False

    print_replicas(f"BEFORE Doctor {doctor_id} updates Patient {patient_id}")
    print(f"[LOCK ACQUIRED] Doctor {doctor_id} is updating Patient {patient_id}")

    with db_lock:  # lock only while editing
        for i, replica in enumerate(REPLICAS):
            updated = update_patient_in_replica(replica, patient_id, edits)
            results.append(f"Replica {i+1}: {'UPDATED' if updated else 'NOT FOUND'}")
            if updated:
                updated_any = True

    print(f"[LOCK RELEASED] Doctor {doctor_id} finished updating Patient {patient_id}")
    print_replicas(f"AFTER Doctor {doctor_id} updated Patient {patient_id}")

    return {
        "status": "success" if updated_any else "fail",
        "message": f"Doctor {doctor_id} updated Patient {patient_id}" if updated_any else "Patient not found.",
        "replica_status": results,
        "final_db": copy.deepcopy(REPLICAS)
    }

# -------------------------
# Patient function
# -------------------------
def patient(patient_id, edits):
    allowed_fields = {"name", "age", "gender"}  # patient can only edit these
    safe_edits = {k: v for k, v in edits.items() if k in allowed_fields}

    results = []
    updated_any = False

    print_replicas(f"BEFORE Patient {patient_id} updates self")
    print(f"[LOCK ACQUIRED] Patient {patient_id} is updating their own record")

    with db_lock:
        for i, replica in enumerate(REPLICAS):
            updated = update_patient_in_replica(replica, patient_id, safe_edits)
            results.append(f"Replica {i+1}: {'UPDATED' if updated else 'NOT FOUND'}")
            if updated:
                updated_any = True

    print(f"[LOCK RELEASED] Patient {patient_id} finished updating")
    print_replicas(f"AFTER Patient {patient_id} updated self")

    return {
        "status": "success" if updated_any else "fail",
        "message": f"Patient {patient_id} updated their record" if updated_any else "Patient not found.",
        "replica_status": results,
        "final_db": copy.deepcopy(REPLICAS)
    }

# -------------------------
# Exchange function
# -------------------------
def exchange():
    return copy.deepcopy(REPLICAS)

# -------------------------
# Run the server
# -------------------------
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9000
    with ThreadedXMLRPCServer((HOST, PORT), allow_none=True) as server:
        server.register_function(doctor, "doctor")
        server.register_function(patient, "patient")
        server.register_function(exchange, "exchange")
        print(f"[SERVER] Running XML-RPC on {HOST}:{PORT}")
        server.serve_forever()