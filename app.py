from flask import Flask, render_template, request, jsonify, redirect, url_for
from openai import OpenAI
import sqlite3

# Initialize app and OpenAI client
app = Flask(__name__)
client = OpenAI(api_key="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")  # <-- your actual API key here

# ✅ Home (Chatbot)
@app.route("/")
def home():
    return render_template("chat.html")

# ✅ Handle chatbot responses
@app.route("/get", methods=["POST"])
def get_bot_response():
    try:
        user_message = request.json["message"]

        prompt = f"You are Jarvis, an intelligent financial advisor. Respond conversationally to: {user_message}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Jarvis, a friendly and knowledgeable AI investment advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        bot_reply = response.choices[0].message.content.strip()

        # 🪙 If user asks to invest, append [INVEST_NOW] trigger
        if any(word in user_message.lower() for word in ["invest", "start investment", "begin investing", "invest now"]):
            bot_reply += " Let's begin your first investment journey on Jarvis! [INVEST_NOW]"

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Sorry, there was an error connecting to Jarvis: {str(e)}"})

# ✅ Investment page
@app.route("/invest")
def invest_page():
    return render_template("invest.html")

# ✅ Handle investment form submission
@app.route("/submit_investment", methods=["POST"])
def submit_investment():
    try:
        name = request.form["name"]
        metal = request.form["metal"]
        amount = request.form["amount"]

        # Save investment in a simple SQLite DB
        conn = sqlite3.connect("investments.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                metal TEXT,
                amount REAL
            )
        """)
        cursor.execute("INSERT INTO investments (name, metal, amount) VALUES (?, ?, ?)", (name, metal, amount))
        conn.commit()
        conn.close()

        # Success message
        message = "🎉 Congratulations! Your investment has been recorded successfully."
        return render_template("success.html", message=message)

    except Exception as e:
        return render_template("success.html", message=f"⚠️ Error saving investment: {str(e)}")

# ✅ Success page
@app.route("/success")
def success_page():
    return render_template("success.html", message="🎉 Congratulations! Your investment has been recorded.")

# ✅ Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
