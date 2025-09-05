"""
A utility script to seed the Firebase Emulator Suite with test data.

This script reads data from JSON files and populates the corresponding
Firestore collections. It is designed to be run from the project root.

Usage:
  - Ensure the Firebase emulators are running.
  - Set the FIRESTORE_EMULATOR_HOST environment variable.
  - Run the script: `python util/seed_emulator.py`
"""
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

def seed_collection(db, collection_name, data_path, id_field):
    """Seeds a single Firestore collection from a JSON file."""
    print(f"Seeding collection '{collection_name}'...")
    collection_ref = db.collection(collection_name)
    
    with open(data_path, 'r') as f:
        data = json.load(f)

    for item in data:
        doc_id = item[id_field]
        # Convert ISO date strings to datetime objects for fields that need it
        if 'createdAt' in item:
            item['createdAt'] = datetime.fromisoformat(item['createdAt'].replace('Z', '+00:00'))
        if 'modifiedAt' in item:
            item['modifiedAt'] = datetime.fromisoformat(item['modifiedAt'].replace('Z', '+00:00'))
            
        collection_ref.document(doc_id).set(item)
        print(f"  - Added document: {doc_id}")
    print(f"Seeding for '{collection_name}' complete.")

def main():
    """Main function to run the seeding process."""
    if not os.getenv('FIRESTORE_EMULATOR_HOST'):
        print("Error: FIRESTORE_EMULATOR_HOST environment variable not set.")
        print("This script is intended for emulator use only.")
        exit(1)

    # Use a dummy credential for emulator, as it doesn't require authentication.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    print("Starting Firestore emulator seeding...")
    
    seed_collection(db, 'users', 'e2e/data/users.json', 'uid')
    seed_collection(db, 'portfolios', 'e2e/data/portfolios.json', 'portfolioId')

    print("\nEmulator seeding finished successfully!")

if __name__ == "__main__":
    main()