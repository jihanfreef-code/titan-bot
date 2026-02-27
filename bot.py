from flask import Flask
import threading
import time
import os
import random

app = Flask(__name__)

# ডাটাবেজ এবং প্রেডিকশন ভেরিয়েবল
DATABASE = []
NEXT_PREDICTION = "WAITING..."

def ai_engine():
    global DATABASE, NEXT_PREDICTION
    print("TITAN AI: Logic Engine Started...")
    
    # টেস্ট ডাটা জেনারেটর (মামা, এখানে পরে আমরা আসল API লিঙ্ক বসাবো)
    while True:
        # গেম থেকে রেজাল্ট আসার সিমুলেশন
        new_result = random.choice(["B", "S"]) 
        DATABASE.append(new_result)
        
        # ডাটা যদি বেশি হয়ে যায়, তবে শেষ ২০টা রাখবে
        if len(DATABASE) > 20:
            DATABASE.pop(0)
        
        # সহজ এআই লজিক: যদি শেষ ৩টা Small হয়, তবে পরেরটা Big হওয়ার চান্স বেশি
        if len(DATABASE) >= 3:
            last_three = DATABASE[-3:]
            if last_three == ["S", "S", "S"]:
                NEXT_PREDICTION = "BIG (High Chance)"
            elif last_three == ["B", "B", "B"]:
                NEXT_PREDICTION = "SMALL (High Chance)"
            else:
                NEXT_PREDICTION = random.choice(["BIG", "SMALL"]) + " (Analysis)"
        
        time.sleep(30) # প্রতি ৩০ সেকেন্ডে ডাটা আপডেট হবে

@app.route('/')
def home():
    db_string = " - ".join(DATABASE) if DATABASE else "COLLECTING DATA..."
    color = "#ff0000" if "BIG" in NEXT_PREDICTION else "#00ff00"
    
    return f"""
    <html>
        <head>
            <title>TITAN AI PREDICTOR</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {{ background: #050505; color: white; font-family: sans-serif; text-align: center; padding-top: 50px; }}
                .box {{ border: 2px solid #333; display: inline-block; padding: 30px; border-radius: 20px; background: #111; box-shadow: 0 0 30px #00ffff66; }}
                .pred {{ font-size: 40px; font-weight: bold; color: {color}; margin: 20px 0; text-shadow: 0 0 10px {color}; }}
                .data {{ font-size: 18px; color: #888; letter-spacing: 2px; }}
            </style>
        </head>
        <body>
            <div class="box">
                <h1 style="color: #00ffff;">🚀 TITAN AI V1.0</h1>
                <p>SERVER STATUS: <span style="color: #00ff00;">● ONLINE</span></p>
                <hr style="border: 0.5px solid #333;">
                
                <h3>🔮 NEXT PREDICTION:</h3>
                <div class="pred">{NEXT_PREDICTION}</div>
                
                <h4>📊 RECENT TREND:</h4>
                <div class="data">{db_string}</div>
                
                <p style="margin-top: 20px; font-size: 14px; color: #555;">Total Points: {len(DATABASE)} | Updates every 30s</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    threading.Thread(target=ai_engine, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
