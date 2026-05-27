from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import date


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
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT NOT NULL,
            amount INTEGER NOT NULL,
            data TEXT NOT NULL,
            category TEXT OT NULL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
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
    
# Get http://127.0.0.1:5000/api/users/2
@app.get("/api/users/<int:user_id>")
def get_user_by_id(user_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row:
        return jsonify({
            "success": False,
            "message": "User not found"
        }),404
    
    print(f"row = {row}")
    user_information = dict(row)
    connection.close()
    
    return jsonify({
        "success": True,
        "message": "User retrieved successfully",
        "data": user_information
    }), 200
    
    
# PUT http://127.0.0.1:5000/api/users/2
@app.put("/api/users/<int:user_id>")
def update_user_by_id(user_id):
    updated_user = request.get_json()
    username = updated_user["username"]
    password = updated_user["password"]
    
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    
    # Validation
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row:
        return jsonify({
            "success": True,
            "message": "User not found"
        }), 404
    
    cursor.execute("UPDATE users SET username=?, password=? WHERE id=?", (username, password, user_id))
    connection.commit()
    connection.close()
    
    return jsonify({
        "success": True,
        "message": "USer updated Successfully"
    }), 200
    



# Delete 
@app.delete("/api/users/<int:user_id>")
def delete_user_by_id(user_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row:
        return jsonify({
            "success": False,
            "message": "User not found"
        }),404
        
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    connection.commit() # Save the connection
    connection.close() # Close the connection 
    
    
    
    return jsonify({
        "success": True,
        "message": "User deleted successfully",
    }), 200

# ---Expenses ---
# POST http://127.0.0.1:5000/api/expenses
@app.post("/api/expenses")
def create_expense():
    new_expense = request.get_json()
    print(new_expense)
    
    title = new_expense.get("title", "")
    description = new_expense.get("description", "")
    amount = new_expense.get("amount", 1)
    date_expense = new_expense.get("date", date.today()) #....
    category = new_expense.get("category", "") 
    user_id = new_expense.get("user_id", 2) 
    
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO expenses (title, description, amount, date, category, user_id)
        VALUES(?, ?, ?, ?, ?, ?)""", (title, description, amount, date_expense, category, user_id) )
    connection.commit()
    connection.close()
    
    return jsonify({
        "success": True,
        "message": "Expense created successfully",
    }), 201
    



# GET http://127.0.0.1:5000/api/expenses
@app.get ("/api/expenses")
def get_expenses():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    print(f"expenses {rows}")
    
    expenses = []
    for row in rows:
        print(f"row = {dict(row)}")
        expenses.append(dict(row))
    
    return jsonify({
        "success": True,
        "message": "Expenses retrieved successfully",
        "data": expenses
    }), 200
    
    
# GET http://127.0.0.1:5000/api/expenses/2
@app.get("/api/expenses/<int:expense_id>")
def get_expense_by_id(expense_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    row = cursor.fetchone()
    
    if not row:
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404
        
    print(f"row = {row}")
    expense = dict(row)
    connection.close()
    
    return jsonify({
        "success": True,
        "message": "Expenses retrieved successfully",
        "data": expense
    }), 200
    
# Update


# DELETE http://127.0.0.1:5000/api/expenses/2
@app.delete("/api/expenses/<int:expense_id>")
def delete_expense_by_id (expense_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    row = cursor.fetchone()
    
    if not row:
        return jsonify({
            "success": False,
            "message": "Expense not found"
        }), 404
    
    
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    connection.commit() 
    connection.close()
    
    
    return jsonify({
        "success": True,
        "message": "Expenses retrieved successfully",
    }), 200




# ---- Front end ----
@app.get("/")
@app.get("/home")
@app.get("/index")
def home():
    return render_template("home.html")

@app.get("/about")
def about():
    student_data = {
        "name": "Rife",
        "cohort": 66,
        "year": 2026
    }
    
    return render_template("about.html", student=student_data)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)