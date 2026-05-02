#!/bin/bash
echo "1. Creating Depot..."
curl -s -X POST "http://localhost:8000/api/v1/depots" \
     -H "Content-Type: application/json" \
     -d '{"id": "DEPOT-001", "mechanic_hours": 10}'
echo -e "\n"

echo "2. Adding Task V-101..."
curl -s -X POST "http://localhost:8000/api/v1/tasks" \
     -H "Content-Type: application/json" \
     -d '{"taskID": "V-101", "Impact": 50, "duration": 4}'
echo -e "\n"

echo "3. Adding Task V-102..."
curl -s -X POST "http://localhost:8000/api/v1/tasks" \
     -H "Content-Type: application/json" \
     -d '{"taskID": "V-102", "Impact": 30, "duration": 3}'
echo -e "\n"

echo "4. Generating Schedule..."
curl -s -X POST "http://localhost:8000/api/v1/schedule/DEPOT-001"
echo -e "\n"
