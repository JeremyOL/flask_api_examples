from flask import Flask, url_for, request, render_template, abort, redirect
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Index Page</p>"

@app.route("/abort")
def abort401():
    abort(401)

@app.route("/login/")
def bad_login():
    return redirect(url_for('abort401'))

@app.route("/hello")
def hello_world():
    return "Hello World!"


@app.route("/hello/<name>")
def hello_name(name):
    return f"Hello, {escape(name)}!"


@app.route("/get_post", methods=["GET", "POST"])
def get_and_post():
    if request.method == "POST":
        return "IS A POST"
    else:
        return "IS A GET"


@app.get("/get_only")
def just_a_get():
    return request.method


@app.post("/post_only")
def just_a_post():
    return request.method


@app.route("/call_template")
@app.route("/call_template/<name>")
def calling_a_template(name=None):
    return render_template("im_a_template.j2", name=name)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return render_template("im_a_template.j2", name=request.form["username"])
    else:
        return render_template("im_a_template.j2", name=request.args.get("user", None))


@app.route("/form", methods=["POST", "GET"])
def call_form():
    if request.method == "GET":
        return render_template("im_a_form_template.j2", posted=False)
    else:
        files_route = "uploaded_files"
        request.files.get("file").save(files_route)
        return render_template("im_a_form_template.j2", posted=True)


with app.test_request_context():
    print(url_for("hello_world"))
    print(url_for("hello_world", next="/"))
    print(url_for("hello_name", name="Z"))
    print(url_for("get_and_post"))
    print(url_for("just_a_get"))
    print(url_for("just_a_post"))
    print(url_for("static", filename="style.css"))
    print(url_for("calling_a_template"))
    print(url_for("calling_a_template", name="Jeremy"))
    print(url_for("login"))
    print(url_for("call_form"))

with app.test_request_context("/call_template", method="GET"):
    assert request.path == "/call_template"
