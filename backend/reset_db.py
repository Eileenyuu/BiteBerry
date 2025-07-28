#!/usr/bin/env python3
"""
Simple database reset utility

Usage:
  python reset_db.py    # Reset the database to clean state
"""
import os
import sys

def reset_database():
    """Reset the database by deleting the file"""
    # Change to the backend directory first
    os.path.dirname(os.path.dirname(__file__))
    db_file = "biteberry.db"
    
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print(f"✅ Database reset successfully! Deleted: {db_file}")
            print("\nNow you can start the server:")
            print("uvicorn main:app --reload")
        except Exception as e:
            print(f"❌ Error deleting database: {e}")
            sys.exit(1)
    else:
        print(f"ℹ️  Database file '{db_file}' doesn't exist. Nothing to reset.")
        print("\nYou can start the server:")
        print("uvicorn main:app --reload")

if __name__ == "__main__":
    print("🔄 Resetting database...")
    reset_database()