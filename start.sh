#!/bin/bash

echo "🫐 Starting BiteBerry servers..."

# Start backend in background
echo "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn main:app --reload &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Both servers started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait