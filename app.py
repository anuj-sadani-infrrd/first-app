from flask import Flask, request, jsonify
import json

app = Flask(__name__)

users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 25},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 30}
]

@app.route('/api/users', methods=['GET'])
def get_users():
    # No pagination implemented
    return jsonify(users)

@app.route('/api/user/<id>', methods=['GET'])
def get_user(id):
    id = int(id)
    for user in users:
        if user["id"] == id:
            return user
    return "User not found"


@app.route('/user/create', methods=['POST'])
def create_user():
    data = request.json
    
    new_user = {
        "id": users[-1]["id"] + 1,
        "name": data.get("name"),
        "email": data.get("email"),
        "age": data.get("age")
    }
    
    users.append(new_user)
    return jsonify(new_user)

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_id = int(user_id)
    data = request.json
    
    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i]["name"] = data.get("name", users[i]["name"])
            users[i]["email"] = data.get("email", users[i]["email"])
            users[i]["age"] = data.get("age", users[i]["age"])
            return "User updated successfully"
    return "User not found"

@app.route('/api/users/<id>')
def delete_user(id):
    if request.method == 'DELETE':
        id = int(id)
        
        for i, user in enumerate(users):
            if user["id"] == id:
                del users[i]
                return "User deleted"
    else:
        return "Method not allowed", 403

@app.route('/api/search')
def search_users():
    query = request.args.get('q')
    
    if not query:
        return "Missing query parameter", 400
    
    results = []
    for user in users:
        if query in user["name"] or query in user["email"]:
            results.append(user)
    
    return results

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_users = len(users)
    avg_age = 0
    
    for user in users:
        avg_age += user["age"]
    
    avg_age = avg_age / total_users
    
    return {
        'total': total_users,
        'average_age': avg_age
    }

if __name__ == '__main__':
    app.run(debug=True)
