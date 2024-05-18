from flask import Flask, render_template, request

app = Flask(__name__)

flag = 1
name = ""

@app.route("/main",  methods=["GET","POST"])
def main():
    global flag, name
    if flag == 1:
        name = request.form.get("q")
        flag = 0
        
    return render_template(
         "main.html", r= name )

@app.route("/dbs_price",  methods=["GET","POST"])
def do_dbs_price():
    
    q = float(request.form.get("q"))
    return render_template("dbs_price.html", r=(q*-50.6)+90.2)

def do_prediction():
    
    return render_template(
         "prediction.html"
    )

@app.route("/prediction",  methods=["GET","POST"])
def prediction():
    
    
    return do_prediction()

@app.route("/",  methods=["GET","POST"])
def index():
     return render_template(
         "index.html"
    )
    
if __name__ == "__main__":
    app.run()
