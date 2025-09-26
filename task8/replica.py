import xmlrpc.client
import time

SERVER_IP = "192.168.29.217"  # replace with exchange server IP
proxy = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:8000/")

print(proxy.exchange())

print("\nSending 10 patient requests")

for i in range(1, 11):
    patient_id = i % 5 + 1
    response = proxy.patient(patient_id)
    if response["status"] == "notice":
        print(f"Request {i} for Patient ID {patient_id}: Request granted → {response['msg']}")
    elif response["status"] == "error":
        print(f"Request {i} for Patient ID {patient_id}: Failed → {response['msg']}")
    else:
        print(f"Request {i} for Patient ID {patient_id}: {response}")
    time.sleep(0.2)
