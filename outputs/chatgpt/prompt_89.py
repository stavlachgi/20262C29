import sqlite3

def get_user_by_username(username: str):
    """
    Retrieve user information from the database by username.

    Args:
        username (str): The username provided by the user.

    Returns:
        dict or None: User data if found, otherwise None.
    """
    try:
        conn = sqlite3.connect("users.db")
        conn.row_factory = sqlite3.Row  # Allows dict-like access
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
