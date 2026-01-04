from app import app, db
import subprocess

with app.app_context():
    print("Dropping and recreating database...")
    db.drop_all()
    db.create_all()
    print("Database structure updated.")

print("Seeding database...")
subprocess.run(["python", "seed_db.py"])
print("Seeding complete.")

print("Starting Flask server...")
subprocess.run(["python", "app.py"])
