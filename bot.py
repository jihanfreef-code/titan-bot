from flask import Flask
import threading
import time
import os

app = Flask(__name__)

# তোর ডাটাবেজ (নতুন করে শুরু হবে)
DATABASE = ""

def fetch_dkwin_result():
    global DATABASE
    print("TITAN AI: Data tracking started...")
    while True:
        # আপাতত টেস্ট ডাটা হিসেবে 'S' যোগ হচ্ছে
        # মামা, এটা সেট হয়ে গেলে আমি তোকে DK Win এর আসল ডাটা কানেক্ট করার কোড দেব
        new_res = "S" 
        DATABASE += new_res
        print(f"Added: {new_res} | Current DB Length: {len(DATABASE)}")
        time.sleep(30) # ৩০ সেকেন্ড পরপর ডাটা চেক করবে

@app.route('/')
def home():
    # এইটাই তোর ওয়েবসাইটের মূল চেহারা
    return f"""
    <html>
        <head>
            <title>TITAN AI DASHBOARD</title>
            <meta http-equiv="refresh" content="10"> </head>
        <body style="background-color: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding: 50px;">
            <div style="border: 2px solid #00ff00; display: inline-block; padding: 20px; border-radius: 15px; box-shadow: 0 0 20px #00ff00;">
                <h1 style="text-shadow: 2px 2px #ff0000;">🚀 TITAN AI LIVE TRACKER</h1>
                <p style="color: white;">Status: <span style="color: #00ff00;">● ACTIVE</span></p>
                <hr style="border: 1px solid #333;">
                
                <h3 style="color: #ffcc00;">📡 CURRENT DATABASE (LIVE):</h3>
                <div style="background: #111; padding: 20px; border-radius: 10px; word-wrap: break-word; font-size: 24px; color: #00ffff; margin: 20px; min-width: 300px; max-width: 80vw;">
                    {DATABASE if DATABASE else "INITIALIZING... PLEASE WAIT"}
                </div>
                
                <p style="font-size: 18px;">Total Data Points: <span style="color: #ff00ff;">{len(DATABASE)}</span></p>
                <p style="color: #888; font-size: 12px;">(The page refreshes every 10 seconds to show new data)</p>
            </div>
            <br><br>
            <p style="color: #555;">&copy; 2026 TITAN AI SYSTEM BY JIHAN</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে ডাটা কালেকশন শুরু করার থ্রেড
    threading.Thread(target=fetch_dkwin_result, daemon=True).start()
    
    # রেন্ডার পোর্টের জন্য সেটিংস
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
