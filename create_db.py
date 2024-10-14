import sqlite3
import uuid
import datetime

#current datatime
current_datetime = datetime.datetime.now()
#unique id


def save_to_database(result, filename):
    unique_id = uuid.uuid4()
    id = int(unique_id.int)
    id = str(id % 1000000).zfill(6)
    # Open a connection to the SQLite database
    conn = sqlite3.connect('invoice.db')
    cursor = conn.cursor()

    query = """CREATE TABLE IF NOT EXISTS
    INVOICE_DATA(invoice_id INTEGER PRIMERY KEY,invoice_type TEXT,filename TEXT,key TEXT,value TEXT,date DATETIME)"""

    cursor.execute(query)
    # Begin a transaction
    conn.execute('BEGIN')
    for i in result:
        if 'supplier_name' in i[0]:
            invoice_type = i[1]
            break
    try:
        for i in result:
            data = (id, invoice_type, filename, i[0], i[1], current_datetime)
            query = "INSERT INTO INVOICE_DATA (invoice_id, invoice_type, filename, key, value, date) VALUES (?, ?, ?, ?, ?, ?)"
            # cursor.execute(f"INSERT INTO INVOICE_DATA (invoice_id, invoice_type, filename, key, value, date) VALUES ({id}, {invoice_type}, {filename}, {i[0]}, {i[1]}, {current_datetime})")
            cursor.execute(query, data)
            conn.commit()
        conn.close()
        return id
    except Exception as e:
        # Rollback the transaction if there's an exception
        conn.rollback()
        print("Error:", str(e))
        return None


    

def save_feedback(name, comments):
    # Open a connection to the SQLite database
    conn = sqlite3.connect('invoice.db')
    cursor = conn.cursor()

    query = """CREATE TABLE IF NOT EXISTS
    feedback(name TEXT,comments TEXT,date DATETIME)"""

    cursor.execute(query)
    # Begin a transaction
    conn.execute('BEGIN')

    try:
        data = (name, comments, current_datetime)
        query = "INSERT INTO feedback (name, comments, date) VALUES (?, ?, ?)"
        cursor.execute(query, data)
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        # Rollback the transaction if there's an exception
        conn.rollback()
        print("Error:", str(e))
        return False


    
def save_contact(name, email, message):
    # Open a connection to the SQLite database
    conn = sqlite3.connect('invoice.db')
    cursor = conn.cursor()

    query = """CREATE TABLE IF NOT EXISTS
    contact(name TEXT,email TEXT,message TEXT,date DATETIME)"""

    cursor.execute(query)
    # Begin a transaction
    conn.execute('BEGIN')

    try:
        data = (name, email, message, current_datetime)
        query = "INSERT INTO contact (name, email, message, date) VALUES (?, ?, ?, ?)"
        cursor.execute(query, data)
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        # Rollback the transaction if there's an exception
        conn.rollback()
        print("Error:", str(e))
        return False



def retrive_data(invoiceid):
    # Open a connection to the SQLite database
    conn = sqlite3.connect('invoice.db')
    cursor = conn.cursor()

    try:
        query = f"select * from INVOICE_DATA where invoice_id={invoiceid}"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        print("Error:", str(e))
        return False
