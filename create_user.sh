curl -X POST http://localhost:8000/users/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "manager",
           "password": "manager",
           "full_name": "New User",
           "role": "admin"
         }'
