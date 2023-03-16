from flask import Flask, render_template, Response, stream_with_context
import io
import base64
import sqlite3
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import json

from matplotlib.animation import FuncAnimation
from datetime import datetime

# Create Flask App
app = Flask(__name__)

# Connect to SQL database
def connect_sqlite():
    path = "C:/Users/hangp/.vscode/web-data-gui/livetest.db"
    conn = sqlite3.connect(path)
    print("Database successfully connected")
    return conn

#Query entire table
def grab_entire_table(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM data")
    data = cur.fetchall()
    return data

# Query most recent row
def query_row(conn, value):
    cur = conn.cursor()
    if(value == 0):
        cur.execute("SELECT * FROM XDATA ORDER by time DESC LIMIT 1")
    elif(value == 1):
        cur.execute("SELECT * FROM YDATA ORDER by time DESC LIMIT 1")
    row = cur.fetchone()
    return row

# Plot entire SQL table up to this point with Matplotlib
def plot(data):
    fig = Figure()
    ax = fig.subplots()
    y_values = []
    x_values = []

    for row in data:
        y_values.append(row[1])
        x_values.append(row[2])
    
    ax.plot(x_values, y_values)
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')

    image = base64.b64encode(buffer.getbuffer()).decode("ascii")
    plot_url = f"<img src='data:image/png;base64,{image}'/>"
    return plot_url

# Grab row and convert to JSON 
def grab_x_row(conn):
    value = 0
    while True:
        row = query_row(conn, value)
        json_data = json.dumps(
            {"name": row[0], 'value': row[1], 'time': row[2]})
        yield f"data:{json_data}\n\n"
        time.sleep(0.1)
        
    
# Grab row and convert to JSON 
def grab_y_row(conn):
    value = 1
    while True:
        row = query_row(conn, value)
        json_data = json.dumps(
            {"name": row[0], 'value': row[1], 'time': row[2]})
        yield f"data:{json_data}\n\n"
        time.sleep(50/1000)
        

#localhost:5000/chart page - Plot chart Not live
@app.route("/chart")
def chart():
    conn = connect_sqlite()
    data = grab_entire_table(conn)
    plot_url = plot(data)
    return plot_url
    

#localhost:5000/livexdata - View JSON data taken from SQL
@app.route("/livexdata", methods=['GET', 'POST'])
def livexdata():
    conn = connect_sqlite()
    response = Response(stream_with_context(grab_x_row(conn)), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = 'no'

    return response

@app.route("/liveydata", methods=['GET', 'POST'])
def liveydata():
    conn = connect_sqlite()
    response = Response(stream_with_context(grab_y_row(conn)), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = 'no'

    return response


# Home page - Render main.html page
@app.route("/")
def home():
    return render_template('main.html')

if __name__ == "__main__":
    app.run()       