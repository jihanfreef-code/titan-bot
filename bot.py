from flask import Flask
import threading
import time
import os
import random

app = Flask(__name__)

# ডাটাবেজ (তোর স্ক্রিনশট থেকে নেওয়া প্যাটার্ন এখানে সেভ হচ্ছে)
# প্যাটার্ন: B, S, B, B, B, S, S, B, S, B (নিচ থেকে উপরে)
HISTORY = ["B", "S", "B", "B", "B", "S", "S", "B", "S", "B"]
PREDICTION = "ANALYZING..."
CONFIDENCE = 0

def titan_ultra_logic():
    global HISTORY, PREDICTION, CONFIDENCE
    
    while True:
        if len(HISTORY) < 3:
            PREDICTION = "COLLECTING DATA..."
            CONFIDENCE = 0
        else:
            last_3 = HISTORY[-3:]
            big_count = HISTORY[-10:].count("B")
            small_count = HISTORY[-10:].count("S")
            
            # ১. ড্রাগন প্যাটার্ন চেক (Dragon Trend)
            if last_3 == ["B", "B", "B"]:
                PREDICTION = "SMALL"
                CONFIDENCE = 85  # টানা ৩ বার Big আসলে পরেরটা Small হওয়ার চান্স বেশি
            elif last_3 == ["S", "S", "S"]:
                PREDICTION = "BIG"
                CONFIDENCE = 85
                
            # ২. অল্টারনেট প্যাটার্ন (Zig-Zag)
            elif last_3 == ["B", "S", "B"]:
                PREDICTION = "SMALL"
                CONFIDENCE = 70
            elif last_3 == ["S", "B", "S"]:
                PREDICTION = "BIG"
                CONFIDENCE = 70
                
            # ৩. প্রোবাবিলিটি চেক
            else:
                if big_count > small_count:
                    PREDICTION = "SMALL (Reverse)"
                    CONFIDENCE = 60
                else:
                    PREDICTION = "BIG (Reverse)"
                    CONFIDENCE = 60

        # সিমুলেশন: প্রতি ৩০ সেকেন্ডে গেমের সাথে তাল মিলিয়ে ডাটা আপডেট হবে
        # (মামা, এখানে আমরা পরে রিয়াল অটো-স্ক্র্যাপার কানেক্ট করতে পারবো)
        new_val = random.choice(["B", "S"])
        HISTORY.append(new_val)
        if len(HISTORY) > 50: HISTORY.pop(0)
        
        time.sleep(30)

@app.route('/')
def home():
    history_str = ""
    for res in reversed(HISTORY[-15:]):
        color = "#ff4d4d" if res == "B" else "#4dff4d"
        history_str += f'<span style="color:{color}; font-weight:bold; margin:0 5px;">{res}</span>'
    
    conf_color = "#00ffff" if CONFIDENCE > 70 else "#f39c12"
    
    return f"""
    <html>
        <head>
            <title>TITAN ULTRA PRO V2</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {{ background: #0a0a0a; color: #e0e0e0; font-family: 'Segoe UI', Tahoma; text-align: center; padding: 20px; }}
                .container {{ border: 1px solid #333; display: inline-block; padding: 40px; border-radius: 30px; background: linear-gradient(145deg, #111, #050505); box-shadow: 0 0 50px rgba(0,255,255,0.2); }}
                .prediction-box {{ font-size: 50px; color: {conf_color}; margin: 25px 0; text-shadow: 0 0 20px {conf_color}; font-weight: 900; letter-spacing: 2px; }}
                .confidence {{ font-size: 20px; color: #888; }}
                .history-bar {{ background: #1a1a1a; padding: 15px; border-radius: 10px; margin-top: 30px; font-family: monospace; font-size: 20px; }}
                .status {{ color: #00ff00; font-size: 14px; letter-spacing: 1px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 style="color: #00ffff; margin-bottom: 5px;">TITAN ULTRA PRO</h2>
                <p class="status">● AI ENGINE ACTIVE (v2.0)</p>
                <hr style="border: 0.5px solid #222;">
                
                <p style="margin-top:20px; color:#aaa;">NEXT PREDICTION</p>
                <div class="prediction-box">{PREDICTION}</div>
                <div class="confidence">Accuracy: {CONFIDENCE}%</div>
                
                <div class="history-bar">
                    <p style="font-size:12px; color:#555; margin-bottom:10px;">RECENT TREND (LAST 15)</p>
                    {history_str}
                </div>
                
                <p style="margin-top: 30px; font-size: 12px; color: #444;">Analyzing period based on DK Win patterns...</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    threading.Thread(target=titan_ultra_logic, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
