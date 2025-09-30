from xmlrpc.server import SimpleXMLRPCServer

# -------------------------
# Patient dataset
# -------------------------
patients = [
    {"id": 1, "name": "Aarav", "age": 25, "gender": "M", "disease": "Flu", "medicines": "Paracetamol", "blood": "O+"},
    {"id": 2, "name": "Srishti", "age": 22, "gender": "F", "disease": "Diabetes", "medicines": "Metformin", "blood": "A+"},
    {"id": 3, "name": "Vikram", "age": 30, "gender": "M", "disease": "Asthma", "medicines": "Inhaler", "blood": "B+"},
    {"id": 4, "name": "Neha", "age": 27, "gender": "F", "disease": "Hypertension", "medicines": "Amlodipine", "blood": "AB+"},
    {"id": 5, "name": "Rahul", "age": 40, "gender": "M", "disease": "Covid-19", "medicines": "Remdesivir", "blood": "O-"},
]

# -------------------------
# Doctor dataset
# -------------------------
doctors = [
    {"doc_id": 101, "name": "Dr. Mehta", "age": 45, "gender": "M", "specialization": "Cardiologist"},
    {"doc_id": 102, "name": "Dr. Sharma", "age": 38, "gender": "F", "specialization": "Pulmonologist"},
]

# -------------------------
# RPC Functions
# -------------------------
def exchange():
    return "Secure Patient Record Exchange Server Running..."

def doctor(doc_id, patient_id):
    """Doctor requests specific patient record"""
    for doc in doctors:
        if doc["doc_id"] == doc_id:
            for p in patients:
                if p["id"] == patient_id:
                    log_msg = f"[SERVER LOG] Doctor {doc['name']} accessed record of Patient {p['name']} (ID {p['id']})"
                    print(log_msg)
                    return {"status": "success", "record": p}
            print(f"[SERVER LOG] Doctor {doc['name']} tried to access Patient ID {patient_id}, but not found")
            return {"status": "error", "msg": "Patient not found"}
    print(f"[SERVER LOG] Unauthorized doctor tried to access Patient ID {patient_id}")
    return {"status": "error", "msg": "Doctor not authorized"}

def doctor_all_records(doc_id):
    """Doctor requests all patient records"""
    for doc in doctors:
        if doc["doc_id"] == doc_id:
            log_msg = f"[SERVER LOG] Doctor {doc['name']} accessed ALL patient records"
            print(log_msg)
            return {"status": "success", "records": patients}
    print(f"[SERVER LOG] Unauthorized doctor (ID {doc_id}) tried to access all records")
    return {"status": "error", "msg": "Doctor not authorized"}

def patient(patient_id):
    """Patient requests their record (only notification)"""
    for p in patients:
        if p["id"] == patient_id:
            msg = f" Patient ID {patient_id} ({p['name']}) requested their record"
            print("[SERVER LOG]", msg)
            with open("requests.log", "a") as f:
                f.write(msg + "\n")
            return {"status": "notice", "msg": msg}
    print(f"[SERVER LOG] Unknown Patient ID {patient_id} tried to access record")
    return {"status": "error", "msg": "Patient not found"}

# -------------------------
# Start RPC Server
# -------------------------
server = SimpleXMLRPCServer(("0.0.0.0", 8000))
print(" RPC Server started at port 8000...")

server.register_function(exchange, "exchange")
server.register_function(doctor, "doctor")
server.register_function(doctor_all_records, "doctor_all_records")
server.register_function(patient, "patient")

server.serve_forever()
