from datetime import datetime
from flask import Flask, render_template, request, redirect

import psycopg2

app = Flask(__name__)

# Connect to an existing database
conn = psycopg2.connect(user="postgres", password="Danso2015", host="localhost", port="5432", database="mydukasite")
# a connection creates a session.
# a session is the period in which you’re  connected or logged in into your db.

# Open a cursor to perform database operations
cur = conn.cursor()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/about_us", methods=["GET"])
def about_us():
    return render_template("about_us.html")


@app.route("/contact_us", methods=["GET"])
def icontact_us():
    return render_template("contact_us.html")


# admin route
@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("/admin.html")

# admin dashboard route


@app.route("/admin/dashboard", methods=["GET"])
def dashboard():
    return render_template("/admin/dashboard.html")

# admin inventories route


@app.route("/admin/inventories", methods=["GET", "POST"])
def inventories():
    if request.method == "POST":
        # To capture data from the form
        name = request.form["name"]
        quantity = request.form["quantity"]
        bp = request.form["bp"]
        sp = request.form["sp"]
        # Inserting data to database
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO inventories (name,quantity, bp, sp) VALUES (%s, %s, %s, %s)", (name, quantity, bp, sp))
        conn.commit()
# redirecting is a get request
        return redirect("/admin/inventories")
    else:
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventories")
        rows = cur.fetchall()
        print()
        return render_template("admin/inventories.html", rows=rows)

# sales route


@app.route("/admin/sales", methods=["GET", "POST"])
def sales():
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales;")
    rows = cur.fetchall()
    print(rows)
    return render_template("/admin/sales.html", rows=rows)


@app.route('/make_sale', methods=['GET', 'POST'])
def make_sale():
    if request.method == "POST":
        pid = request.form['pid']
        quantity = request.form['qty']
        # from datetime import datetime
        created_at = datetime.now()
    # time when the sale is made
        cur= conn.cursor()
        cur.execute("INSERT INTO Sales (pid, quantity, created_at) VALUES (%s, %s, %s)",(pid, quantity, created_at))
    # commit changes you make to the database
        conn.commit()
        return redirect("admin/sales")
    else:
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales;")
        rows = cur.fetchall()
        print(rows)
        return render_template("/admin/sales.html", rows=rows)

#a new route for viewing sales per product
@app.route('/view_sales/<int:pid>',methods=['GET', 'POST'])
def view_sales(pid):
    if request.method == "POST":
        # query the sales for that product_id
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales WHERE product_id=%s;",[pid])
        rows = cur.fetchall()
        return render_template("sales.html", rows = rows)
    else:
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales;")
        rows = cur.fetchall()
        print(rows)
        return render_template("/admin/sales.html", rows=rows)


