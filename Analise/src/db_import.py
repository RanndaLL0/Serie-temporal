import sqlite3
import csv
import os


def create_database(db_path: str):
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS date(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER,
            month INTEGER,
            year INTEGER,
            UNIQUE(day, month, year)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flag(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mflag TEXT,
            qflag TEXT,
            sflag TEXT,
            UNIQUE(mflag, qflag, sflag)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS star(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            element TEXT,
            value REAL,
            flag_id INTEGER,
            date_id INTEGER,
            FOREIGN KEY (flag_id) REFERENCES flag(id),
            FOREIGN KEY (date_id) REFERENCES date(id)
        );
    """)

    conn.commit()
    return conn, cursor



def csv_to_sqlite(csv_path, db_path):
    conn, cursor = create_database(db_path)

    with open(csv_path, "r", newline="") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)

        for row in reader:
            year      = int(row[1])
            month     = int(row[2])
            day       = int(row[3])
            element   = row[4]
            value     = float(row[5])
            mflag     = row[6]
            qflag     = row[7]
            sflag     = row[8]

            cursor.execute("""
                INSERT OR IGNORE INTO date(day, month, year)
                VALUES (?, ?, ?)
            """, (day, month, year))

            cursor.execute("""
                SELECT id FROM date
                WHERE day = ? AND month = ? AND year = ?
            """, (day, month, year))
            date_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT OR IGNORE INTO flag(mflag, qflag, sflag)
                VALUES (?, ?, ?)
            """, (mflag, qflag, sflag))

            cursor.execute("""
                SELECT id FROM flag
                WHERE mflag = ? AND qflag = ? AND sflag = ?
            """, (mflag, qflag, sflag))
            flag_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO star (element, value, flag_id, date_id)
                VALUES (?, ?, ?, ?)
            """, (element, value, flag_id, date_id))


    conn.commit()
    conn.close()
    print(f"Banco criado com sucesso: {db_path}")



directory = os.fsencode("../data/csv")
db_path = "../data/db/dados_climaticos.db"    

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):

        src = f"../data/csv/{filename}"

        csv_to_sqlite(src, db_path)
        # print(os.path.join(directory, filename))
