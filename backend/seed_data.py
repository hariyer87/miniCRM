from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models import User, Patient, TestCatalog


def run():
    db = SessionLocal()
    if not db.query(User).filter(User.username == "admin").first():
        admin = User(username="admin", full_name="Administrator", role="admin", password_hash=get_password_hash("admin123"))
        db.add(admin)
    if not db.query(Patient).first():
        patient = Patient(patient_code="P001", first_name="John", last_name="Doe")
        db.add(patient)
    if not db.query(TestCatalog).first():
        test = TestCatalog(code="CBC", name="Complete Blood Count", sample_type="blood", price=500)
        db.add(test)
    db.commit()
    db.close()


if __name__ == "__main__":
    run()
