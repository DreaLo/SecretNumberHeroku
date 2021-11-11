import random
from datetime import datetime
from flask import Flask, render_template, request, make_response

webapp = Flask(__name__)


@webapp.route("/")
def index_date():
    return render_template("index.html", date=datetime.now())


@webapp.route("/", methods=["GET"])
def index():
    secret_number = request.cookies.get("secret_number")  # check if there is already a cookie named secret_number

    response = make_response(render_template("index.html"))
    if not secret_number:  # if not, create a new cookie
        new_secret = random.randint(1, 30)
        response.set_cookie("secret_number", str(new_secret))

    return response


@webapp.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    secret_number = int(request.cookies.get("secret_number"))

    if guess == secret_number:
        message = "Correct! The secret number is {0} !".format(str(secret_number))
        response = make_response(render_template("result-win.html", message=message))
        response.set_cookie("secret_number", str(random.randint(1, 30)))  # set the new secret number
        return response
    elif guess > secret_number:
        message = "Your guess is not correct... Let's try something smaller."
        return render_template("result.html", message=message)
    elif guess < secret_number:
        message = "Your guess is not correct...Ok,let's try something BIGGER."
        return render_template("result.html", message=message)


if __name__ == '__main__':
    webapp.run(use_reloader=True)