from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_ngrok import run_with_ngrok

app = Flask(__name__)

run_with_ngrok(app)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mood_notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    video_link = db.Column(db.String(500))
    playlist_link = db.Column(db.String(500))

# Create the database
with app.app_context():
    db.create_all()

# Function to analyze user text and return media links
def analyze_text(text):
    text = text.lower()
    if "sad" in text or "sadness" in text:
        return {
            "video": "https://youtu.be/wnHW6o8WMas?si=Nc7sWwZJ9cukASLV",
            "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0"
        }
    elif "angry" in text or "anger" in text:
        return {
            "video": "https://youtu.be/GNO2ugM0Q0s?si=YFZijjxahKC34LLG",
            "playlist": "https://open.spotify.com/playlist/7CUWmkFZXtc8cbPFuBBdoo?si=n2-KrVKIRnaZjFyzwGbSgw&pi=tMjq3nQ-TZW7I"
        }
    elif "fear" in text or "anxiety" in text:
        return {
            "video": "https://youtu.be/zOPoW58dqag?si=-OGKHXIhuQxmMUXa",  # Example link
            "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX6VdMW310YC7"  # Example link
        }
    elif "jealousy" in text or "guilt" in text or "shame" in text:
        return {
            "video": "https://youtu.be/zO4VWw_QGsE?si=_uvf7f3-y6Z-xNu7",  # Example link
            "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX3u6V8a1g8H"  # Example link
        }
    elif "lonely" in text or "loneliness" in text:
        return {
            "video": "https://youtu.be/YweYRl7IUPc?si=CRcqtY5zhMjYTRyr",  # Example link
            "playlist": "https://open.spotify.com/playlist/1rCVV18M87Y4DXIyaG8IOX?si=TDT7GojyTIeSpZcLajWY1w&pi=aFkA8KUTTY2Yk"  # Example link
        }
    elif "frustration" in text or "despair" in text:
        return {
            "video": "https://youtu.be/kDMEx29RlE8?si=Xg3Er7n7cq2WcZJe",  # Example link
            "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX6VdMW310YC7"  # Example link
        }
    elif "joy" in text or "happy" in text or "love" in text or "contentment" in text or "excitement" in text or "amusement" in text or "hope" in text or "serenity" in text or "pride" in text or "awe" in text:
        return {
            "video": "https://youtu.be/W6wVU5b5nQk?si=Z9PrG_gzx8U8nExY",
            "playlist": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"
        }
    elif "nostalgia" in text:
        return {
            "video": "https://youtu.be/M5VXCixTdEg?si=gd6M6RRIXYxE59mw",  # Example link
            "playlist": "https://open.spotify.com/playlist/1tOdyNZ0SKvPU0cjCPXRte?si=Q4ulT3udTtuQDj5fdWJFTA&pi=WV1jS3IaR7-ID"  # Example link
        }
    elif "ambivalence" in text:
        return {
            "video": "https://youtube.com/shorts/Dthh2EVkABw?si=q0TTqt7QggEE-5IL",  # Example link
            "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX3W 0U4WJzZ8F"  # Example link
        }
    elif "melancholy" in text:
        return {
            "video": "https://youtu.be/yTPuNMUSwPM?si=CVm3an0lnYdO4WR9",  # Example link
            "playlist": "https://open.spotify.com/playlist/5VhrCpZquiCH6ETRg6MvAG?si=lKAA1hTWSfWJ4vzmLhhfdQ&pi=1REkwpRmRS2kQ"  # Example link
        }
    elif "longing" in text:
        return {
            "video": "https://youtube.com/shorts/Opbs7LcXhzI?si=Zhwp-93AtBfBXrdQ",  # Example link
            "playlist": "https://open.spotify.com/playlist/1AOjSu9JOcDZT9QeSaSMUV?si=4LbZs22kToii3f_S6BkwAg&pi=3cKXr-FfTzKR3"  # Example link
        }
    elif "regret" in text:
        return {
            "video": "https://youtu.be/kDMEx29RlE8?si=Xg3Er7n7cq2WcZJe",  # Example link
            "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX6VdMW310YC7"  # Example link
        }
  
    else:
        return {
            "video": "https://youtu.be/kDMEx29RlE8?si=Xg3Er7n7cq2WcZJe",
            "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX6VdMW310YC7"
        }

# Route for the homepage
@app.route("/")
def home():
    notes = Note.query.all()  # Retrieve all notes
    return render_template("index.html", notes=notes)

# Route for analyzing text input
@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.json.get("text")
    media_links = analyze_text(user_input)

    # Save the note and its links in the database
    new_note = Note(text=user_input, video_link=media_links["video"], playlist_link=media_links["playlist"])
    db.session.add(new_note)
    db.session.commit()

    return jsonify(media_links)

# Route for deleting a note
@app.route("/delete_note/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": "Note deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)