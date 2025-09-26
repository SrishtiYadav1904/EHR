import xmlrpc.client

# Server IP and Port (keep same as server)
SERVER_IP = "10.65.156.48"
proxy = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:8000/")

# Test connection
print(proxy.exchange())  # plain text only

while True:
    print("\nChoose option:")
    print("1. Doctor Access (specific patient)")
    print("2. Doctor Access (all patients)")
    print("3. Patient Access")
    print("4. Exit")

    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Invalid input, try again")
        continue

    if choice == 1:
        try:
            doc_id = int(input("Enter Doctor ID: "))
            patient_id = int(input("Enter Patient ID to fetch record: "))
            response = proxy.doctor(doc_id, patient_id)
            print("Server Response:", response)
        except Exception as e:
            print("Error:", e)

    elif choice == 2:
        try:
            doc_id = int(input("Enter Doctor ID: "))
            response = proxy.doctor_all_records(doc_id)
            if response['status'] == "success":
                print("All Patient Records:")
                for p in response['records']:
                    print(p)
            else:
                print("Server Response:", response)
        except Exception as e:
            print("Error:", e)

    elif choice == 3:
        try:
            patient_id = int(input("Enter Patient ID: "))
            response = proxy.patient(patient_id)
            print("Server Response:", response)
        except Exception as e:
            print("Error:", e)

    elif choice == 4:
        print("Exiting client...")
        break

    else:
        print("Invalid choice, try again")
