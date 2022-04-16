# from crypt import methods
from flask import Flask , render_template , request
app = Flask(__name__)

import movie as mv
import pandas as pd 


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/sub",methods = ['POST'])
def submit():
    if request.method == "POST":
        a = request.form["a"]
    num = mv.recommend(a)


    return render_template("sub.html" , n=num , df=a)


if __name__ == "__main__":
    app.run(debug=True)