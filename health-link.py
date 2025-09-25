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
