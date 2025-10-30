from flask import Flask, request, jsonify

from flask_cors import CORS

import psycopg2, os


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

conn = connect_db()

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")


if request.method == "POST":

isim = request.json.get("isim")

if isim:

cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))

conn.commit()


cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")

isimler = [row[0] for row in cur.fetchall()]


cur.close()

conn.close()


return jsonify(isimler)


if __name__ == "__main__":

app.run(host="0.0.0.0", port=5001)
