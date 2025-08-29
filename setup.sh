#!/bin/bash

echo "🫐 Setting up BiteBerry..."

# Backend setup
echo "Setting up backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python reset_db.py
cd ..

# Frontend setup
echo "Setting up frontend..."
cd frontend
npm install
cd ..

echo "✅ Setup complete! Run ./start.sh to start both servers"