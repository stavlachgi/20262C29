import sqlite3

def get_user_by_username(username):
    db_path = 'users.db'
    query = "SELECT id, username, email, joined_date FROM users WHERE username = ?"
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()
            
            if user_data:
                return {
                    "id": user_data[0],
                    "username": user_data[1],
                    "email": user_data[2],
                    "joined_date": user_data[3]
                }
            return None
            
    except sqlite3.Error:
        return None
