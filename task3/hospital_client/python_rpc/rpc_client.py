import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://172.16.233.206:9000/")

print("1. Access Doctor Details")
print("2. Access My Own Details")
choice = int(input("Enter choice: "))

if choice == 1:
    patient_id = int(input("Enter your Patient ID: "))
    doctor_id = int(input("Enter Doctor ID you want to access: "))
    response = server.exchangebypatient(patient_id, doctor_id)
    print("Response from server:", response)

elif choice == 2:
    patient_id = int(input("Enter your Patient ID: "))
    response = server.getpatientdetails(patient_id)
    print("Response from server:", response)

else:
    print("Invalid choice")
