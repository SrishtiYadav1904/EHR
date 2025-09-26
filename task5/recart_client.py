import xmlrpc.client
import pprint

SERVER_IP = "http://10.65.156.48:9000/"  # same IP as server
rpc = xmlrpc.client.ServerProxy(SERVER_IP, allow_none=True)
pp = pprint.PrettyPrinter(indent=2)

def doctor_flow():
    doc_id = int(input("Enter Doctor ID: "))
    pat_id = int(input("Enter Patient ID to edit: "))
    edits = {}
    name = input("Enter new name (or Enter to skip): ")
    if name.strip(): edits["name"] = name
    disease = input("Enter new disease (or Enter to skip): ")
    if disease.strip(): edits["disease"] = disease
    medicines = input("Enter new medicines (or Enter to skip): ")
    if medicines.strip(): edits["medicines"] = medicines
    res = rpc.doctor(doc_id, pat_id, edits)
    pp.pprint(res)

def patient_flow():
    pat_id = int(input("Enter your Patient ID: "))
    edits = {}
    name = input("Enter new name (or Enter to skip): ")
    if name.strip(): edits["name"] = name
    disease = input("Enter new disease (or Enter to skip): ")
    if disease.strip(): edits["disease"] = disease
    medicines = input("Enter new medicines (or Enter to skip): ")
    if medicines.strip(): edits["medicines"] = medicines
    res = rpc.patient(pat_id, edits)
    pp.pprint(res)

def main():
    while True:
        print("\n=== MENU ===")
        print("1. Doctor edit")
        print("2. Patient edit")
        print("3. View Database")
        print("4. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            doctor_flow()
        elif choice == "2":
            patient_flow()
        elif choice == "3":
            db = rpc.exchange()
            pp.pprint(db)
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
