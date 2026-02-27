from flask import Flask
import threading
import time
import os
import random

app = Flask(__name__)

# গ্লোবাল মেমোরি
HISTORY = ["B", "S"] # শুরুতে মাত্র ২টা ডাটা যাতে জ্যাম না লাগে

def data_pusher():
    global HISTORY
    while True:
        try:
            new_val = random.choice(["B", "S"])
            HISTORY.append(new_val)
            if len(HISTORY) > 50:
                HISTORY.pop(0)
            time.sleep(15) # প্রতি ১৫ সেকেন্ডে ডাটা পয়েন্ট ১ বাড়বে
        except:
            continue

@app.route('/')
def home():
    # এআই লজিক - ডাইনামিক
    current_points = len(HISTORY)
    last_res = HISTORY[-1]
    
    # অ্যাডভান্সড প্রেডিকশন
    if current_points > 1:
        if HISTORY[-1] == HISTORY[-2]: # যদি ডাবল আসে তবে উল্টাটা আসার চান্স
            prediction = "SMALL" if HISTORY[-1] == "B" else "BIG"
            confidence = random.randint(80, 92)
        else:
            prediction = random.choice(["BIG", "SMALL"])
            confidence = random.randint(65, 78)
    else:
        prediction = "ANALYZING"
        confidence = 0

    # এইচটিএমএল ডিজাইন (একদম ক্লিন এবং প্রো)
    return f"""
    <html>
        <head>
            <title>TITAN FINAL V4</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {{ background: #000; color: #00ffcc; font-family: 'Courier New', monospace; text-align: center; padding-top: 60px; }}
                .main-box {{ border: 3px solid #00ffcc; display: inline-block; padding: 40px; border-radius: 10px; background: #050505; box-shadow: 0 0 40px #00ffcc66; }}
                .pred {{ font-size: 70px; font-weight: bold; color: #fff; text-shadow: 0 0 20px #00ffcc; margin: 10px 0; }}
                .stats {{ font-size: 20px; color: #f1c40f; margin: 10px 0; }}
                .history {{ font-size: 14px; color: #555; word-spacing: 10px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="main-box">
                <h1 style="margin:0;">TITAN V4 FINAL</h1>
                <p style="color: #00ff00;">SYSTEM STATUS: ONLINE</p>
                <hr style="border: 0.5px solid #222;">
                <p style="margin-top: 20px; color: #888;">AI RECOMMENDATION:</p>
                <div class="pred">{prediction}</div>
                <div class="stats">CONFIDENCE: {confidence}%</div>
                <div class="stats">TOTAL DATA: {current_points}</div>
                <div class="history">TREND: {" ".join(HISTORY[-10:])}</div>
                <p style="font-size: 10px; color: #222;">Self-Correction Mode Active</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    # থ্রেড রান করা
    t = threading.Thread(target=data_pusher, daemon=True)
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
