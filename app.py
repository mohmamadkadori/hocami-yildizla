import os
import helpers

from flask import Flask, render_template, request, redirect, flash
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))




@app.route('/')
def index():
    conn = helpers.get_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS hocalar (
                id SERIAL PRIMARY KEY, name TEXT, rating FLOAT, submissions INTEGER DEFAULT 0)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS comments (
                profid INTEGER REFERENCES hocalar(id), comment TEXT)""")
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('index.html')


@app.route('/search')
def search():
    name = request.args.get("hoca_adi", "").strip().lower()
    conn = helpers.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hocalar WHERE name LIKE %s", (f"%{name}%",))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("search.html", results=results)


@app.route('/result')
def result():
    profid = request.args.get("id")
    conn = helpers.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hocalar WHERE id = %s", (profid,))
    result = cursor.fetchone()
    if not result:
        flash("Hoca bulunamadı. Lütfen geçerli bir ID girin.", "danger")
        cursor.close()
        conn.close()
        return redirect("/search")
    cursor.execute("SELECT * FROM comments WHERE profid = %s", (profid,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("result.html", result=result, comments=comments)
    


@app.route('/rate', methods=["POST"])
def rate():
    profid = int(request.form.get("profid"))
    rating = request.form.get("rating")
    if rating:
        rating = float(rating)
        if rating >= 1 and rating <=5:
            conn = helpers.get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT submissions FROM hocalar WHERE id = %s", (profid,))
            submissions_row = cursor.fetchone()
            submissions = submissions_row['submissions'] if submissions_row else 0
            print(f"Submissions: {submissions}")
            cursor.execute("SELECT rating FROM hocalar WHERE id = %s", (profid,))
            rating_row = cursor.fetchone()
            if rating_row and rating_row['rating'] is not None:
                avgRating = rating_row['rating']
            else:
                avgRating = 0
            print(f"Avg Rating: {avgRating}")
            newRating = (avgRating * submissions + rating) / (submissions + 1)
            cursor.execute("UPDATE hocalar SET rating = %s, submissions = %s WHERE id = %s", (newRating, submissions+1, profid,))
            conn.commit()
            cursor.close()
            conn.close()
            message = "Puanınız başarıyla kaydedildi. Teşekkür ederiz!"
            flash(message, "success")
            return redirect(f"/result?id={profid}")
        else:
            message = "Geçersiz puan değeri. Lütfen 1 ile 5 arasında bir sayı girin."
            flash(message, "danger")
            return redirect(f"/result?id={profid}")
    else:
            message = "Geçersiz puan değeri. Lütfen 1 ile 5 arasında bir sayı girin."
            flash(message, "danger")
            return redirect(f"/result?id={profid}")
        
    


@app.route('/comment', methods=["POST"])
def comment():
    profid = int(request.form.get("profid"))
    comment = request.form.get("comment")
    if comment:    
        conn = helpers.get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comments (profid, comment) VALUES (%s, %s)", (profid, comment))
        conn.commit()
        cursor.close()
        conn.close()
        message = "Yorumunuz başarıyla kaydedildi. Teşekkür ederiz!"
        flash(message, "success")
        return redirect(f"/result?id={profid}")
    else:
        message = "Yorum boş olamaz. Lütfen geçerli bir yorum girin."
        flash(message, "danger")
        return redirect(f"/result?id={profid}")
        



@app.route('/add', methods=["POST"])
def add():
    name = request.form.get('name', '').strip().lower()
    if name:
        conn = helpers.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hocalar WHERE name = %s", (name,))
        data = cursor.fetchone()
        if not data:
            cursor.execute("INSERT INTO hocalar (name) VALUES (%s) RETURNING id", (name,))
            id = cursor.fetchone()['id']
            message = f"Hoca '{name}' başarıyla eklendi!"
        else:
            id = data['id']  # First column is id
            message = f"Hoca '{name}' zaten mevcut!"
        flash(message, "success")
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(f'/result?id={id}')
    else:
        flash("Hoca adı boş olamaz. Lütfen geçerli bir isim girin.", "danger")
        return redirect("/")
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port, debug=True)
