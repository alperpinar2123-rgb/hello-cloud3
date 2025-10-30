from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://hello_kloud2_db_user:UxLdeEE4UxcNel2MieU1ZPlQ3NcexdXf@dpg-d3tjheggjchc73fan2ng-a.oregon-postgres.render.com/hello_kloud2_db"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Ensure the table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ziyaretciler (
                id SERIAL PRIMARY KEY,
                isim TEXT
            )
        """)

        # Handle POST request: insert new visitor
        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            isim = data.get("isim")

            if isim:
                cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
                conn.commit()

        # Always return the 10 most recent visitors
        cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
        isimler = [row[0] for row in cur.fetchall()]

        return jsonify(isimler)

    except psycopg2.Error as e:
        print("Veritabanı hatası:", e)
        return jsonify({"error": "Database connection failed"}), 500

    except Exception as e:
        print("Genel hata:", e)
        return jsonify({"error": "Internal server error"}), 500

    finally:
        # Close connections safely
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
