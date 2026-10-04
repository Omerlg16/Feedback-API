from Config.database import get_connection

def insert_review(name, rating, comment):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO reviews (name, rating, comment) VALUES (%s, %s, %s)",
            (name, rating, comment)
        )
        connection.commit()
    finally:
        connection.close()

def count_by_rating():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT rating, COUNT(*) FROM reviews GROUP BY rating")
        return cursor.fetchall()
    finally:
        connection.close()

def count_by_month():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT TO_CHAR(DATE_TRUNC('month', created_at), 'YYYY-MM') AS month, COUNT(*) "
            "FROM reviews GROUP BY month ORDER BY month"
        )
        return cursor.fetchall()
    finally:
        connection.close()
