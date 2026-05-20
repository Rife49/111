from flask import Flask, jsonify, request
import sqlite3


app = Flask(__name__) # Create a Flask instance

DB_NAME = "budget_manager.db"

def init_db():
    connection = sqlite3.connect(DB_NAME) # Open a connection to a D.B named "budget_manager.db"
    cursor = connection.cursor() # Creates a cursor/tool that lets you send commands (Select, Insert,, ...) to the D.B.
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    connection.commit() # Save changes to the D.B.
    connection.close() # Close the connection to the D.B.

# http://127.0.0.1:5000/api/health

@app.get("/api/health")
def health_check():
    return jsonify({
        "status": "OK"
    }), 200
    
# ------- USERS ---------
# http://127.0.0.1:5000/api/users

@app.post("/api/users")
def register():
    new_user = request.get_json()
    print(new_user)
    
    username= new_user["username"]
    password= new_user["password"]
    
    connection = sqlite3.connect(DB_NAME) # Open a connection to the D.B.
    cursor = connection.cursor() # Create a cursor/tool (Insert, Select, ....) to the D.B.
    cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
    connection.commit() # Save the connection
    connection.close() # Close the connection 
    
    return jsonify ({
        "success": True,
        "message": "User created successfully"
    }), 201 # created 
    
# GET http://127.0.0.1:5000/api/users
@app.get("/api/users")
def get_users():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row # Allows columns values to be retrieved by name, row["username"]
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print(rows)
    connection.close()
    
    users = []
    for row in rows:
        print(dict(row))
        users.append(dict(row))
    
    return jsonify ({
        "success": True,
        "message": "User created successfully",
        "data": users 
    })

    
if __name__ == "__main__":
    init_db()
    app.run(debug=True)