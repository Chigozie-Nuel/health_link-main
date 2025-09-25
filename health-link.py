import uuid
import qrcode
from datetime import datetime

# Predefined medical departments
MEDICAL_DEPARTMENTS = {
    "1": "General Practitioner",
    "2": "Dentist",
    "3": "Surgeon",
    "4": "Pediatrician",
    "5": "Cardiologist",
    "6": "Nurse",
    "7": "Admin"
}

# Diagnostic questions and possible outcomes
DIAGNOSTIC_QUESTIONS = {
    "fever": {
        "questions": [
            "Do you have chills?",
            "Is your temperature above 38°C?",
            "Do you feel fatigued?"
        ],
        "diagnosis": "You may have a viral infection or flu."
    },
    "headache": {
        "questions": [
            "Is the pain localized or general?",
            "Do you feel nauseous?",
            "Are you sensitive to light?"
        ],
        "diagnosis": "You may be experiencing a migraine."
    },
    "cough": {
        "questions": [
            "Is the cough dry or wet?",
            "Do you have chest pain?",
            "Are you experiencing shortness of breath?"
        ],
        "diagnosis": "You may have bronchitis or early pneumonia."
    }
}

# Audit trail
LOGIN_LOG = []


def show_welcome_screen():
    print("\n" + "=" * 50)
    print("Welcome to Health-Link")
    print("Your all-in-one mobile clinic")
    print("Secure | Accessible | Community-Driven")
    print("=" * 50 + "\n")


class Patient:
    def __init__(self, name, email, password, dob):
        self.name = name
        self.email = email
        self.password = password
        self.dob = dob
        self.medical_id = str(uuid.uuid4())
        self.symptom = None
        self.responses = {}
        self.diagnosis_history = []
        self.health_record = {
            "name": self.name,
            "email": self.email,
            "dob": self.dob,
            "medical_id": self.medical_id
        }
        self.generate_qr_code()
        self.save_id_to_txt()

    def generate_qr_code(self):
        qr = qrcode.make(self.medical_id)
        qr.save(f"{self.name}_QR.png")
        print(f"QR code saved as {self.name}_QR.png")

    def save_id_to_txt(self):
        with open(f"{self.name}_ID.txt", "w") as f:
            f.write(f"Patient ID: {self.medical_id}")
        print(f"Patient ID saved as {self.name}_ID.txt")

    def report_symptom(self):
        print("\nPlease describe your symptom:")
        self.symptom = input("Symptom: ").lower()
        print(f"Symptom '{self.symptom}' recorded.")


class HealthCareWorker:
    def __init__(self, name, email, password, dob, role, specialty):
        self.name = name
        self.email = email
        self.password = password
        self.dob = dob
        self.role = role.lower()
        self.specialty = specialty

    def interact_with_patient(self, patient):
        print(
            f"\nHello {patient.name}, nice to meet you. How may I help you today?")
        input("Patient: ")
        print("How are you feeling right now?")
        input("Patient: ")
        patient.report_symptom()
        self.run_diagnosis(patient)

    def run_diagnosis(self, patient):
        symptom = patient.symptom
        if not symptom:
            print("No symptom reported.")
            return

        flow = DIAGNOSTIC_QUESTIONS.get(symptom)
        if not flow:
            print(f"No diagnostic flow available for '{symptom}'.")
            return

        print(f"\nLet's ask a few questions to understand your condition better.")
        for q in flow["questions"]:
            ans = input(q + " (yes/no): ").lower()
            patient.responses[q] = ans

        diagnosis = flow["diagnosis"]
        patient.diagnosis_history.append({
            "symptom": symptom,
            "diagnosis": diagnosis,
            "responses": patient.responses.copy()
        })

        print("\nDiagnosis Summary:")
        print(diagnosis)

    def scan_patient(self, medical_id, patient_db):
        patient = patient_db.get(medical_id)
        if patient:
            print(f"\nAccessing health record for {patient['name']}:")
            for key, value in patient.items():
                print(f"{key}: {value}")
        else:
            print("Patient not found.")
class HealthLinkApp:
    def __init__(self):
        self.patients = {}  # medical_id → Patient object
        self.health_workers = {}  # specialty → list of HealthCareWorker objects

    def log_login(self, username, role):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        LOGIN_LOG.append(f"{timestamp} | {role} login | {username}")

    def onboard_patient(self):
        print("\nOnboarding Patient")
        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")
        dob = input("Date of Birth (YYYY-MM-DD): ")
        patient = Patient(name, email, password, dob)
        self.patients[patient.medical_id] = patient
        self.log_login(email, "Patient")
        print(f"Patient {name} onboarded successfully.")
        print(f"Medical ID: {patient.medical_id}")

    def onboard_health_worker(self):
        print("\nOnboarding Health Care Worker")
        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")
        dob = input("Date of Birth (YYYY-MM-DD): ")
        print("\nSelect your specialty:")
        for key, value in MEDICAL_DEPARTMENTS.items():
            print(f"{key}. {value}")
        choice = input("Enter number: ")
        specialty = MEDICAL_DEPARTMENTS.get(choice, "General Practitioner")
        role = specialty if specialty in [
            "Nurse", "Doctor", "Admin"] else "Doctor"
        worker = HealthCareWorker(name, email, password, dob, role, specialty)
        self.health_workers.setdefault(specialty, []).append(worker)
        self.log_login(email, "HealthCareWorker")
        print(
            f"Health Care Worker {name} ({specialty}) onboarded successfully.")

    def search_health_worker(self):
        print("\nSearch Health Care Worker")
        print("Available specialties:")
        for key, value in MEDICAL_DEPARTMENTS.items():
            print(f"{key}. {value}")
        choice = input("Enter specialty number: ")
        specialty = MEDICAL_DEPARTMENTS.get(choice)
        workers = self.health_workers.get(specialty, [])
        if workers:
            print(f"\nAvailable {specialty}s:")
            for worker in workers:
                print(f"- {worker.name} ({worker.email})")
        else:
            print(f"No {specialty}s available.")

    def simulate_scan(self):
        print("\nSimulate QR Scan")
        medical_id = input("Enter patient medical ID from QR or TXT file: ")
        print("Select your specialty:")
        for key, value in MEDICAL_DEPARTMENTS.items():
            print(f"{key}. {value}")
        choice = input("Enter number: ")
        specialty = MEDICAL_DEPARTMENTS.get(choice)
        workers = self.health_workers.get(specialty, [])
        if workers:
            worker = workers[0]
            patient = self.patients.get(medical_id)
            if patient:
                worker.scan_patient(
                    medical_id, {medical_id: patient.health_record})
            else:
                print("Patient not found.")
        else:
            print("No health care worker available for this specialty.")

    def match_and_interact(self):
        print("\nMatch Patient to Health Worker")
        medical_id = input("Enter patient medical ID: ")
        patient = self.patients.get(medical_id)
        if not patient:
            print("Patient not found.")
            return

        print("Select your specialty:")
        for key, value in MEDICAL_DEPARTMENTS.items():
            print(f"{key}. {value}")
        choice = input("Enter number: ")
        specialty = MEDICAL_DEPARTMENTS.get(choice)
        workers = self.health_workers.get(specialty, [])
        if workers:
            worker = workers[0]
            worker.interact_with_patient(patient)
        else:
            print("No health care worker available for this specialty.")

    def show_audit_trail(self):
        print("\nAudit Trail:")
        for log in LOGIN_LOG:
            print(log)


# Main program
app = HealthLinkApp()
show_welcome_screen()

print("To begin, please select your role:")
print("1. Patient")
print("2. Health Care Worker")
role_choice = input("Enter your role (1 or 2): ")

if role_choice == "1":
    app.onboard_patient()
elif role_choice == "2":
    app.onboard_health_worker()
else:
    print("Invalid choice. Proceeding to main menu.")

while True:
    print("\nMain Menu")
    print("1. Onboard Another Patient")
    print("2. Onboard Another Health Care Worker")
    print("3. Search Health Care Worker")
    print("4. Health Worker Scan Patient QR")
    print("5. View Audit Trail")
    print("6. Match Patient to Health Worker and Diagnose")
    print("7. Exit")

    choice = input("Select an option: ")

    if choice == "1":
        app.onboard_patient()
    elif choice == "2":
        app.onboard_health_worker()
    elif choice == "3":
        app.search_health_worker()
    elif choice == "4":
        app.simulate_scan()
    elif choice == "5":
        app.show_audit_trail()
    elif choice == "6":
        app.match_and_interact()
    elif choice == "7":
        print("Exiting Health-Link. Stay healthy.")
        break
    else:
        print("Invalid choice. Please try again.")
