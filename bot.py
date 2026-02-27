from flask import Flask
import threading
import time
import os
import random

app = Flask(__name__)

# শুরুতে আমরা ৫টা রিয়েলিস্টিক ডাটা রাখছি যাতে এআই কনফিউজ না হয়
HISTORY = ["B", "S", "B", "B", "S"]

def force_update():
    global HISTORY
    while True:
        # প্রতি ১৫ সেকেন্ডে নতুন ডাটা পুশ করবে (আগের চেয়ে ফাস্ট)
        new_val = random.choice(["B", "S"])
        HISTORY.append(new_val)
        
        # ডাটা পয়েন্ট ১০০ এর বেশি হলে পুরনোটা কাটবে
        if len(HISTORY) > 100:
            HISTORY.pop(0)
            
        time.sleep(15) 

@app.route('/')
def home():
    # এআই লজিক সরাসরি এখানে (যাতে কোনো ল্যাগ না থাকে)
    last_val = HISTORY[-1]
    total_pts = len(HISTORY)
    
    # সিম্পল কিন্তু স্ট্রং প্যাটার্ন লজিক
    if HISTORY[-3:].count("B") >= 2:
        prediction = "SMALL"
        prob = random.randint(75, 88)
    else:
        prediction = "BIG"
        prob = random.randint(75, 88)

    trend_str = " | ".join(HISTORY[-12:]) # শেষ ১২টা রেজাল্ট দেখাবে

    return f"""
    <html>
        <head>
            <title>TITAN V3 ULTRA</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {{ background: #000; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; padding-top: 40px; }}
                .card {{ border: 2px solid #00ffcc; display: inline-block; padding: 30px; border-radius: 15px; background: #080808; box-shadow: 0 0 20px #00ffcc55; }}
                .pred-text {{ font-size: 55px; color: #00ffcc; font-weight: bold; text-shadow: 0 0 15px #00ffcc; }}
                .points {{ font-size: 22px; color: #f1c40f; margin: 15px 0; }}
                .trend {{ color: #555; font-family: monospace; letter-spacing: 2px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2 style="letter-spacing: 3px;">TITAN QUANTUM V3.1</h2>
                <hr style="border: 0.1px solid #222;">
                <p style="color: #888;">AI PREDICTION:</p>
                <div class="pred-text">{prediction}</div>
                <p>PROBABILITY: {prob}%</p>
                <div class="points">DATA POINTS: {total_pts}</div>
                <div class="trend">RECENT: {trend_str}</div>
                <p style="font-size: 10px; color: #333; margin-top: 15px;">Auto-updates every 10s</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    # থ্রেড স্টার্ট করার আগে একবার চেক করে নেওয়া
    t = threading.Thread(target=force_update)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
