from datetime import date

import mysql.connector


# Connect to MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Replace with your host
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="patients"  # Replace with your database name
        )
        print("Connected successfully!")
        return conn
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None

# Add a patient to the 'patients' table
def add_patient(conn):
    name = input("Enter patient name: ")
    birth_year = int(input("Enter birth year: "))
    gender = input("Enter gender (Male/Female): ")
    address = input("Enter address: ")

    cursor = conn.cursor()
    query = "INSERT INTO patients (name, birth_year, gender, address) VALUES (%s, %s, %s, %s)"
    values = (name, birth_year, gender, address)
    cursor.execute(query, values)
    conn.commit()
    print(f"Patient '{name}' added.")

# Add a doctor to the 'doctors' table
def add_doctor(conn):
    name = input("Enter doctor name: ")
    
    cursor = conn.cursor()
    query = "INSERT INTO doctors (name) VALUES (%s)"
    values = (name,)
    cursor.execute(query, values)
    conn.commit()
    print(f"Doctor '{name}' added.")

# Add an appointment to the 'appointments' table
def add_appointment(conn):
    patient_id = int(input("Enter patient ID: "))
    doctor_id = int(input("Enter doctor ID: "))
    reason = input("Enter appointment reason: ")
    appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
    status = input("Enter appointment status (Pending/Confirmed/Completed/Cancelled): ")
    note = input("Enter any notes for the appointment: ")

    cursor = conn.cursor()
    query = """INSERT INTO appointments 
               (patient_id, doctor_id, reason, appointment_date, status, note) 
               VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (patient_id, doctor_id, reason, appointment_date, status, note)
    cursor.execute(query, values)
    conn.commit()
    print("Appointment added.")

# Generate a report of all appointments
def generate_report(conn):
    cursor = conn.cursor()
    query = """
    SELECT p.name, p.birth_year, p.gender, p.address, d.name, a.reason, a.appointment_date
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    """
    cursor.execute(query)
    results = cursor.fetchall()

    print("{:<5} {:<15} {:<10} {:<10} {:<15} {:<15} {:<10}".format(
        "No", "Patient", "Birth Year", "Gender", "Address", "Doctor", "Reason"
    ))

    for idx, (patient_name, birth_year, gender, address, doctor_name, reason, appointment_date) in enumerate(results, 1):
        print(f"{idx:<5} {patient_name:<15} {birth_year:<10} {gender:<10} {address:<15} {doctor_name:<15} {reason:<10}")

# Get all appointments for today
def get_todays_appointments(conn):
    cursor = conn.cursor()
    today = date.today()
    query = """
    SELECT p.address, p.name, p.birth_year, p.gender, d.name, a.status, a.note
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    WHERE a.appointment_date = %s
    """
    cursor.execute(query, (today,))
    results = cursor.fetchall()

    print("{:<15} {:<10} {:<10} {:<10} {:<15} {:<10} {:<10}".format(
        "Address", "Patient", "Birth Year", "Gender", "Doctor", "Status", "Note"
    ))

    for address, patient_name, birth_year, gender, doctor_name, status, note in results:
        print(f"{address:<15} {patient_name:<10} {birth_year:<10} {gender:<10} {doctor_name:<15} {status:<10} {note:<10}")

# Main program execution
if __name__ == "__main__":
    # Connect to the database
    conn = connect_to_database()

    if conn:
        while True:
            print("\nMenu:")
            print("1. Add a patient")
            print("2. Add a doctor")
            print("3. Add an appointment")
            print("4. Generate appointment report")
            print("5. View today's appointments")
            print("6. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                add_patient(conn)
            elif choice == '2':
                add_doctor(conn)
            elif choice == '3':
                add_appointment(conn)
            elif choice == '4':
                print("\n---- Appointment Report ----")
                generate_report(conn)
            elif choice == '5':
                print("\n---- Today's Appointments ----")
                get_todays_appointments(conn)
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")
        
        # Close the connection when done
        conn.close()
