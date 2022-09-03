import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        tableName = request.form["tableName"]

        columnString = ""

        columns= []
        for k, v in request.form.items():
            if k.startswith("column"):
                columns.append((k, v))

        columns.sort(key=lambda x: x[0])
        for i, column in enumerate(columns):
            if i == 0:
                columnString += column[1]
            else:
                columnString += ", {}".format(columnString) 

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(tableName=tableName, columns=columnString),
            max_tokens=4000,
            temperature=0.6,
        )
        
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(tableName, columns=None):
    return """
    Generate a MySQL query to create the table {} with only the following columns: {}
    """.format(
        tableName, columns
    )