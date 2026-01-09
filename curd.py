import mysql.connector

# connecting pyhton <-> mysql workbench
try:
    conn= mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Saif@321',
    database='flights'
    )

    myCursor= conn.cursor(buffered=True)
    print("connection established")
except Exception as e:
    print(f"connection error:{e}")

#performing queries using myCursor object

# myCursor.execute("CREATE DATABASE flights")
#conn.commit()

# myCursor.execute("""
# CREATE TABLE planes(
# airportID INT NOT NULL,
# code INT NOT NULL,
# city VARCHAR(10) NOT NULL,
# name VARCHAR(10) NOT NULL
# )
# """)
# conn.commit()

# insertion
# myCursor.execute("""
# INSERT INTO planes VALUES
#     (1,234,854301,'DEL'),
#     (2,235,854331,'MUM'),
#     (3,236,89765,'CHIC')
# """)
# conn.commit()

#retrive
