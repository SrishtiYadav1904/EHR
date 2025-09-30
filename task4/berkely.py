def time_to_minutes(t):
    h, m = map(int, t.split(":"))
    return h * 60 + m

def minutes_to_time(m):
    h = m // 60
    m = m % 60
    return f"{h}:{m:02d}"

# Initial times (simulate local clocks)
patient_time = "9:05"
doctor_time = "9:55"
server_time = "9:30"

# Convert to minutes
patient_mins = time_to_minutes(patient_time)
doctor_mins = time_to_minutes(doctor_time)
server_mins = time_to_minutes(server_time)

# Server collects times from all clients (including itself)
times = {
    "Patient": patient_mins,
    "Doctor": doctor_mins,
    "Server": server_mins
}

# Calculate average time
avg_time = sum(times.values()) // len(times)

print(f"Average Time: {minutes_to_time(avg_time)}\n")

# Calculate offsets and adjusted times
for device, t in times.items():
    offset = avg_time - t
    adjusted = t + offset
    print(f"{device}:")
    print(f"  Original Time: {minutes_to_time(t)}")
    print(f"  Offset: {offset} minutes")
    print(f"  Adjusted Time: {minutes_to_time(adjusted)}\n")