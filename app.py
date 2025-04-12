from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create DB and table if not exists
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 address TEXT,
                 phone TEXT,
                 message TEXT,
                 service TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/request-form', methods=['GET', 'POST'])
def request_form():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        message = request.form['message']
        service = request.form['service']

        # Save to database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO requests (name, address, phone, message, service) VALUES (?, ?, ?, ?, ?)",
                  (name, address, phone, message, service))
        conn.commit()
        conn.close()

        return redirect(url_for('confirmation'))

    service = request.args.get('service', 'unknown')
    return render_template('request_form.html', service=service)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
