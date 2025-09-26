import xmlrpc.client
import pprint

SERVER_IP = "http://10.65.156.48:9000/"  # Replace with server IP
rpc = xmlrpc.client.ServerProxy(SERVER_IP, allow_none=True)
pp = pprint.PrettyPrinter(indent=2)

def doctor_flow():
    doc_id = int(input("Enter Doctor ID: "))
    pat_id = int(input("Enter Patient ID to update: "))
    edits = {}
    name = input("New patient name (Enter to skip): ")
    if name.strip(): edits["name"] = name
    age = input("New age (Enter to skip): ")
    if age.strip(): edits["age"] = int(age)
    gender = input("Gender (Enter to skip): ")
    if gender.strip(): edits["gender"] = gender
    disease = input("Disease (Enter to skip): ")
    if disease.strip(): edits["disease"] = disease
    medicines = input("Medicines (Enter to skip): ")
    if medicines.strip(): edits["medicines"] = medicines

    res = rpc.doctor(doc_id, pat_id, edits)
    pp.pprint(res)

def patient_flow():
    pat_id = int(input("Enter your Patient ID: "))
    edits = {}
    name = input("New name (Enter to skip): ")
    if name.strip(): edits["name"] = name
    age = input("New age (Enter to skip): ")
    if age.strip(): edits["age"] = int(age)
    gender = input("Gender (Enter to skip): ")
    if gender.strip(): edits["gender"] = gender

    res = rpc.patient(pat_id, edits)
    pp.pprint(res)

def main():
    while True:
        print("\n=== MENU ===")
        print("1. Doctor updates Patient")
        print("2. Patient updates Self")
        print("3. Exchange / View Database")
        print("4. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            doctor_flow()
        elif choice == "2":
            patient_flow()
        elif choice == "3":
            data = rpc.exchange()
            pp.pprint(data)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
