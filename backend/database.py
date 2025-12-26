from backend.models import Medication, Stock,User

# Basic database of 10 users and 5 medications

# 5 medications
medications_db = [
    Medication(name="amoxicillin", active_ingredient="Amoxicillin trihydrate", dosage_text="Take 1 pill every 8h", prescription_required=True),
    Medication(name="aspirin", active_ingredient="Acetylsalicylic acid", dosage_text="Take 1 pill daily", prescription_required=False),
    Medication(name="paracetamol", active_ingredient="Acetaminophen", dosage_text="Take 1-2 pills every 6h", prescription_required=False),
    Medication(name="ibuprofen", active_ingredient="Ibuprofen", dosage_text="Take 1 pill every 8h", prescription_required=False),
    Medication(name="metformin", active_ingredient="Metformin hydrochloride", dosage_text="Take 1 pill with meals", prescription_required=True),
]

# Stock info
stock_db = {
    "amoxicillin": 12,
    "aspirin": 20,
    "paracetamol": 15,
    "ibuprofen": 8,
    "metformin": 10
}

# 10 synthetic users
users_db = [
    User(name="Alice Smith", email="alice@example.com", age=28, medications=["aspirin", "paracetamol"]),
    User(name="Bob Johnson", email="bob@example.com", age=35, medications=["amoxicillin"]),
    User(name="Charlie Lee", email="charlie@example.com", age=42, medications=["ibuprofen"]),
    User(name="David Schwartzman", email="david@example.com", age=30, medications=["metformin", "aspirin"]),
    User(name="Eli Cohen", email="eli@example.com", age=25, medications=["paracetamol"]),
    User(name="Fiona Davis", email="fiona@example.com", age=33, medications=["amoxicillin", "ibuprofen"]),
    User(name="Grace Kim", email="grace@example.com", age=29, medications=["aspirin"]),
    User(name="Hannah Wilson", email="hannah@example.com", age=31, medications=["metformin"]),
    User(name="Isaac Brown", email="isaac@example.com", age=40, medications=["paracetamol", "ibuprofen"]),
    User(name="Julia Martinez", email="julia@example.com", age=27, medications=["aspirin", "amoxicillin"]),
]
