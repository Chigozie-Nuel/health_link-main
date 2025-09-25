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