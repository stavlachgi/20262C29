import sqlite3

def get_user_info(username: str) -> dict | None:
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    
    row = cursor.fetchone()
    connection.close()
    
    if row is None:
        return None
    
    columns = [description[0] for description in cursor.description]
    return dict(zip(columns, row))
