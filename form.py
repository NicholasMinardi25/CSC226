from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

form_html = """
<!DOCTYPE html>
<html>
  <body>
    <h2>Submit a Message</h2>
    <form method="POST" action="/submit">
      Name: <input type="email" name="name"><br><br>
      Message: <input type="text" name="message"><br><br>
      <input type="submit" value="Submit">
    </form>
    <p>See all messages at <a href="/messages">/messages</a></p>
  </body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(form_html)

@app.route("/submit", methods=["POST"])
def submit():
    # TODO: Get form data from request.form
    name = request.form.get("name")
    message = request.form.get("message")

    # TODO: Save it to a file (append mode - make sure you are appending to the file, not overwriting the whole thing)
    with open("messages.txt", "a") as file:
        file.write(f"{name}: {message}\n")

    return redirect("/messages")

@app.route("/messages", methods=["GET"])
def messages():
    # TODO: Read file content and return as plain text or HTML
    try:
        with open("messages.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    display_html = "<h2>All Submitted Messages</h2><ul>"
    for line in lines:
        display_html += f"<li>{line.strip()}</li>"
    display_html += "</ul><p><a href='/'>Go back</a></p>"

    return display_html

if __name__ == "__main__":
    app.run(debug=True)
