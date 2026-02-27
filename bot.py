from flask import Flask
import threading
import time
import os

app = Flask(__name__)

# তোর ফ্রেশ ডাটাবেজ
DATABASE = ""

def fetch_dkwin_result():
    global DATABASE
    while True:
        # এখানে আমরা DK Win এর ডাটা কানেক্ট করবো
        # আপাতত টেস্ট করার জন্য ১টা করে 'S' যোগ হচ্ছে
        new_res = "S" 
        DATABASE += new_res
        print(f"Added: {new_res}")
        time.sleep(30) # ৩০ সেকেন্ডের গেমের জন্য

@app.route('/')
def home():
    # এইটাই তোর ওয়েবসাইটের চেহারা
    return f"""
    <html>
        <head><title>TITAN AI DASHBOARD</title></head>
        <body style="background-color: #121212; color: white; font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1 style="color: #00ff00;">🚀 TITAN AI LIVE TRACKER</h1>
            <hr style="width: 50%; border: 1px solid #333;">
            <h3>Current Memory (DATABASE):</h3>
            <div style="background: #222; padding: 20px; border-radius: 10px; word-wrap: break-word; font-size: 20px; color: #ffcc00; margin: 20px;">
                {DATABASE if DATABASE else "Waiting for data..."}
            </div>
            <p>Total Signals Tracked: {len(DATABASE)}</p>
            <button onclick="location.reload()" style="padding: 10px 20px; background: #00ff00; border: none; border-radius: 5px; cursor: pointer;">REFRESH DATA</button>
        </body>
    </html>
    """

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে ডাটা কালেকশন শুরু হবে
    threading.Thread(target=fetch_dkwin_result, daemon=True).start()
    # ওয়েবসাইট পোর্ট সেট করা
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
