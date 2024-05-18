from flask import Flask, render_template, request
import google.generativeai as palm
import replicate
import osx
import requests
from PIL import Image

app = Flask(__name__)

flag = 1
name = ""
palm.configure(api_key="AIzaSyDV1E5CltzYfoXoUFMgh8ziYxnFypEO9yc")

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
    apiKey =  "r8_cMMTBEmGy233e5okqviDaJ0nJrbpIGT04ncEg"
    os.environ["REPLICATE_API_TOKEN"] = apiKey
    output = replicate.run(
    "zsxkib/pulid:43d309c37ab4e62361e5e29b8e9e867fb2dcbcec77ae91206a8d95ac5dd451a0",
    input={
        "prompt": "portrait, impressionist painting, loose brushwork, vibrant color, light and shadow play",
        "cfg_scale": 1.2,
        "num_steps": 4,
        "image_width": 768,
        "num_samples": 4,
        "image_height": 1024,
        "output_format": "webp",
        "identity_scale": 0.8,
        "mix_identities": False,
        "output_quality": 80,
        "generation_mode": "fidelity",
        "main_face_image": "https://www.billboard.com/wp-content/uploads/2023/12/taylor-swift-eras-foxborough-2023-billboard-1548.jpg?w=942&h=623&crop=1",
        "negative_prompt": "fire in the eyes, flaws in the face, flaws, lowres, non-HDRi, low quality, worst quality,artifacts noise, text, watermark, glitch, deformed, mutated, ugly, disfigured, hands, low resolution, partially rendered objects,  deformed or partially rendered eyes, deformed, deformed eyeballs, cross-eyed,blurry"
    }
    )
    
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

@app.route("/",  methods=["GET","POST"])
def index():
     return render_template(
         "index.html"
    )

if __name__ == "__main__":
    app.run()
