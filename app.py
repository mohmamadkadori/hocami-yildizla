import os
import helpers
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['DEBUG'] = True
app.config['TESTING'] = True

# ---------- ROUTES ----------

@app.route('/')
def index():
    try:
        conn = helpers.get_db()
        cursor = conn.cursor()
        # Ensure tables exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hocalar (
                id SERIAL PRIMARY KEY, 
                name TEXT, 
                rating FLOAT, 
                submissions INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                profId INTEGER REFERENCES hocalar(id), 
                comment TEXT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('index.html')
    except Exception as e:
        return f"Error in index route: {e}", 500


@app.route('/search')
def search():
    try:
        name = request.args.get("hoca_adi", "").strip().lower()
        conn = helpers.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hocalar WHERE LOWER(name) LIKE %s", (f"%{name}%",))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("search.html", results=results)
    except Exception as e:
        return f"Error in search route: {e}", 500


@app.route('/result')
def result():
    try:
        profId = int(request.args.get("id"))
        conn = helpers.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hocalar WHERE id = %s", (profId,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            flash("Hoca bulunamadı. Lütfen geçerli bir ID girin.", "danger")
            return redirect("/search")
        cursor.execute("SELECT * FROM comments WHERE profId = %s", (profId,))
        comments = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("result.html", result=result, comments=comments)
    except Exception as e:
        return f"Error in result route: {e}", 500


@app.route('/rate', methods=["POST"])
def rate():
    try:
        profId = int(request.form.get("profId"))
        rating = request.form.get("rating")
        if not rating:
            flash("Geçersiz puan değeri. Lütfen 1 ile 5 arasında bir sayı girin.", "danger")
            return redirect(f"/result?id={profId}")
        rating = float(rating)
        if rating < 1 or rating > 5:
            flash("Invalid rating value. Please enter a number between 1 and 5.", "danger")
            return redirect(f"/result?id={profId}")

        conn = helpers.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT submissions, rating FROM hocalar WHERE id = %s", (profId,))
        row = cursor.fetchone()
        submissions = row[0] if row and row[0] is not None else 0
        avgRating = row[1] if row and row[1] is not None else 0
        newRating = (avgRating * submissions + rating) / (submissions + 1)

        cursor.execute(
            "UPDATE hocalar SET rating = %s, submissions = %s WHERE id = %s",
            (newRating, submissions + 1, profId)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Puanınız başarıyla kaydedildi. Teşekkür ederiz!", "success")
        return redirect(f"/result?id={profId}")
    except Exception as e:
        return f"Error in rate route: {e}", 500


@app.route('/comment', methods=["POST"])
def comment():
    try:
        profId = int(request.form.get("profId"))
        comment_text = request.form.get("comment")
        if not comment_text:
            flash("Yorum boş olamaz. Lütfen geçerli bir yorum girin.", "danger")
            return redirect(f"/result?id={profId}")

        conn = helpers.get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comments (profId, comment) VALUES (%s, %s)",
            (profId, comment_text)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Yorumunuz başarıyla kaydedildi. Teşekkür ederiz!", "success")
        return redirect(f"/result?id={profId}")
    except Exception as e:
        return f"Error in comment route: {e}", 500


@app.route('/add', methods=["POST"])
def add():
    try:
        name = request.form.get('name', '').strip().lower()
        if not name:
            flash("Hoca adı boş olamaz. Lütfen geçerli bir isim girin.", "danger")
            return redirect("/")

        conn = helpers.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hocalar WHERE LOWER(name) = %s", (name,))
        data = cursor.fetchone()
        if not data:
            cursor.execute(
                "INSERT INTO hocalar (name) VALUES (%s) RETURNING id", (name,)
            )
            id = cursor.fetchone()[0]
            message = f"Hoca '{name}' başarıyla eklendi!"
        else:
            id = data[0]
            message = f"Hoca '{name}' zaten mevcut!"
        conn.commit()
        cursor.close()
        conn.close()
        flash(message, "success")
        return redirect(f'/result?id={id}')
    except Exception as e:
        return f"Error in add route: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)