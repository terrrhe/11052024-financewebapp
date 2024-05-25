from flask import Flask, render_template, request
import google.generativeai as palm
import replicate
import os
import requests
from PIL import Image
import datetime
import sqlite3

app = Flask(__name__)

flag = 1
name = ""

makersuite_api = os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=makersuite_api)

@app.route("/main",  methods=["GET","POST"])
def main():
    global flag, name
    if flag == 1:
        name = request.form.get("q")
        flag = 0
        
    return render_template(
         "main.html", r= name )

@app.route("/generate_text",  methods=["GET","POST"])
def generate_text():
    return render_template(
         "generate_text.html")

@app.route("/text_result_makersuite",  methods=["GET","POST"])
def text_result_makersuite():
    
    model = { 'model': "models/chat-bison-001"}
    messages =  request.form.get("q")
    response = palm.chat(**model,messages=messages)
    
    return response.last

@app.route("/generate_image",  methods=["GET","POST"])
def generate_image():
    return render_template(
         "generate_image.html")

@app.route("/generate_result_image",  methods=["GET","POST"])
def generate_result_image():
    q = request.form.get("q")
    output = replicate.run("stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
      input = {"prompt":q})
    
    return render_template(
         "generate_image_result.html", r = output)


@app.route("/dbs_price",  methods=["GET","POST"])
def do_dbs_price():
    
    q = float(request.form.get("q"))
    return render_template("dbs_price.html", r=(q*-50.6)+90.2)

@app.route("/end",  methods=["GET","POST"])
def end():
    
    global flag
    global name
    
    flag = 1
    name = ""
    
    return render_template(
         "index.html"
    )


def do_prediction():
    
    return render_template(
         "prediction.html"
    )

@app.route("/prediction",  methods=["GET","POST"])
def prediction():
    
    
    return do_prediction()
    
@app.route("/user_logs",  methods=["GET","POST"])
def user_logs():
     return render_template(
         "logs.html"
    )

@app.route("/log_create",  methods=["GET","POST"])
def log_create():
    
    #q =  request.form.get("q")
    conn = sqlite3.connect('log.db', timeout = 10)
    c = conn.cursor()
    c.execute('CREATE TABLE user (name text, timestamp timestamp)')
    conn.commit()
    c.close()
    conn.close()
    
    return "log table is created successfully"

@app.route("/log_insert",  methods=["GET","POST"])
def log_insert():
    
    q =  request.form.get("q")
    if len(q) > 0:
        conn = sqlite3.connect('log.db', timeout = 10)
        c = conn.cursor()
        c.execute("insert into user(name, timestamp) values(?, ?)", (q, datetime.datetime.now()))
        conn.commit()
        c.close()
        conn.close()
    
        return q + " is inserted successfully"
    
    return "input is empty"

@app.route("/log_show",  methods=["GET","POST"])
def log_show():
    conn = sqlite3.connect('log.db', timeout = 10)
    c = conn.cursor()
    c = conn.execute("select * from user")

    r= "logs are"
    for row in c:
      r += str(row) + ","
        
    return r
    
@app.route("/",  methods=["GET","POST"])
def index():
     return render_template(
         "index.html"
    )

if __name__ == "__main__":
    app.run()
