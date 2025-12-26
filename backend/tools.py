from backend.models import Medication, Stock, Prescription
from backend.database import medications_db, stock_db, users_db

class ToolExecutor:
    """All tools the LLM can call."""

    # Returns basic medication information by name
    def get_medication_by_name(self, name: str) -> dict | None:
        for med in medications_db:
            if med.name.lower() == name.lower():
                return {
                    "name": med.name,
                    "active_ingredient": med.active_ingredient,
                    "prescription_required": med.prescription_required,
                    "dosage_text": med.dosage_text
                }
        return {"error": "We don’t sell this medication in our pharmacy"}

    # Chekcs if a medicine is in our stock and return the quantity
    def check_stock(self, name: str) -> dict | None:
        print("Called and the name is " + name)
        name_lower = name.lower()
        quantity = stock_db.get(name_lower)
        if quantity is not None:
            return {"name": name, "quantity": quantity, "available": True}
        return {"name": name, "quantity": 0, "available": False}

    # Checks if a medication requires prescription
    def check_prescription_requirement(self, name: str) -> dict | None:
        med = self.get_medication_by_name(name)
        if not med:
            return {"name": name, "message": "We don’t have this medication in our store."}
        if med:
            return {"name": name, "required": med["prescription_required"]}
        return {"error": "Medication not found"}
    
    # returns the ingridients in a medication by name
    def get_active_ingredients(self, name: str) -> dict:
        for med in medications_db:
            if med.name.lower() == name.lower():
                return {"name": med.name, "active_ingredient": med.active_ingredient}
        return {"error": "Medication not found"}
    
    # returs the reccomended dosage for a medication
    def get_dosage_info(self, name: str) -> dict:
        for med in medications_db:
            if med.name.lower() == name.lower():
                return {"name": med.name, "dosage_text": med.dosage_text}
        return {"error": "Medication not found"}
    

    # ------------------ User Tools ------------------
    # Returns basic information about a user
    def get_user_by_name(self, name: str) -> dict | None:
        for user in users_db:
            if user.name.lower() == name.lower():
                return {"name": user.name, "email": user.email, "age": user.age, "medication" : user.medications}
        return {"error": "User not found"}

    # returns a list of all the active users
    def list_users(self) -> list:
        return [{"name": user.name, "email": user.email} for user in users_db]

    # Returns the medication associated to a specific user
    def get_user_medications(self, name: str) -> dict | None:
        print("The name called: " , name)
        for user in users_db:
            if user.name.lower() == name.lower():
                return {"name": user.name, "medications": user.medications}
        return {"error": "User not found"}
