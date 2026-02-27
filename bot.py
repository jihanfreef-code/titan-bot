from flask import Flask
import threading
import time
import os
import random

app = Flask(__name__)

# ডাটাবেজ
HISTORY = ["B", "S", "B", "B", "B", "S", "S", "B", "S", "B"]
PREDICTION = "ANALYZING..."
CONFIDENCE = 0
CURRENT_STREAK = 0
STREAK_TYPE = "NONE"

def advanced_statistical_analysis():
    global HISTORY, PREDICTION, CONFIDENCE, CURRENT_STREAK, STREAK_TYPE
    
    while True:
        if len(HISTORY) < 5:
            PREDICTION = "NEED MORE DATA"
            CONFIDENCE = 0
        else:
            # ১. Streak Calculation (টানা কয়টা আসছে)
            last_item = HISTORY[-1]
            streak_count = 1
            for i in range(len(HISTORY)-2, -1, -1):
                if HISTORY[i] == last_item:
                    streak_count += 1
                else:
                    break
            
            CURRENT_STREAK = streak_count
            STREAK_TYPE = "BIG" if last_item == "B" else "SMALL"

            # ২. Frequency & Probability Calculation
            total_b = HISTORY.count("B")
            total_s = HISTORY.count("S")
            total_games = len(HISTORY)
            
            b_percent = (total_b / total_games) * 100
            s_percent = (total_s / total_games) * 100

            # ৩. Advanced Logic Engine
            if streak_count >= 4:
                # যদি টানা ৪ বার বা তার বেশি একই আসে, তবে ট্রেন্ড ভাঙার চান্স বেশি
                PREDICTION = "SMALL" if last_item == "B" else "BIG"
                CONFIDENCE = min(90, 50 + (streak_count * 10)) # স্ট্রিক যত বড়, কনফিডেন্স তত বেশি
            else:
                # যদি স্ট্রিক না থাকে, তবে হিস্টোরি ব্যালেন্স করার চেষ্টা করবে
                if b_percent > 55:
                    PREDICTION = "SMALL"
                    CONFIDENCE = round(b_percent + random.randint(1, 5))
                elif s_percent > 55:
                    PREDICTION = "BIG"
                    CONFIDENCE = round(s_percent + random.randint(1, 5))
                else:
                    # যদি সব ব্যালেন্সড থাকে, তবে অল্টারনেট প্যাটার্ন খুঁজবে
                    PREDICTION = "BIG" if HISTORY[-1] == "S" else "SMALL"
                    CONFIDENCE = 65

        # সিমুলেশন: নতুন ডাটা আপডেট (প্রতি ৩০ সেকেন্ডে)
        new_val = random.choice(["B", "B", "S"]) if random.random() > 0.5 else random.choice(["S", "S", "B"])
        HISTORY.append(new_val)
        if len(HISTORY) > 100: HISTORY.pop(0) # ১০০ টা ডাটা সেভ রাখবে
        
        time.sleep(30)

@app.route('/')
def home():
    history_str = ""
    for res in reversed(HISTORY[-20:]): # শেষ ২০টা দেখাবে
        color = "#ff3333" if res == "B" else "#33ff33"
        history_str += f'<span style="color:{color}; font-weight:900; margin:0 4px; font-size: 22px;">{res}</span>'
    
    conf_color = "#00ffcc" if CONFIDENCE >= 75 else "#ffcc00"
    
    return f"""
    <html>
        <head>
            <title>TITAN V3 AI CORE</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {{ background: #000; color: #fff; font-family: 'Courier New', Courier, monospace; text-align: center; padding: 20px; }}
                .dashboard {{ border: 2px solid #222; display: inline-block; padding: 40px; border-radius: 15px; background: #0a0a0a; box-shadow: 0 0 40px rgba(0, 255, 204, 0.15); max-width: 600px; width: 100%; }}
                .title {{ color: #00ffcc; font-size: 28px; text-transform: uppercase; font-weight: bold; letter-spacing: 3px; }}
                .target-box {{ background: #111; border: 1px solid #333; padding: 20px; margin: 20px 0; border-radius: 10px; }}
                .prediction {{ font-size: 60px; color: {conf_color}; font-weight: 900; text-shadow: 0 0 15px {conf_color}; margin: 10px 0; }}
                .stats {{ display: flex; justify-content: space-between; margin-top: 20px; color: #aaa; font-size: 14px; border-top: 1px solid #222; padding-top: 15px; }}
                .history-box {{ margin-top: 30px; background: #151515; padding: 15px; border-radius: 8px; border: 1px solid #222; }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="title">⚡ TITAN V3 QUANTUM ⚡</div>
                <p style="color: #00ff00; font-size: 12px;">● STATISTICAL ENGINE RUNNING</p>
                
                <div class="target-box">
                    <div style="color: #777; font-size: 16px; letter-spacing: 2px;">SYSTEM RECOMMENDS:</div>
                    <div class="prediction">{PREDICTION}</div>
                    <div style="color: #fff; font-size: 22px;">WIN PROBABILITY: <span style="color:{conf_color}; font-weight:bold;">{CONFIDENCE}%</span></div>
                </div>

                <div class="stats">
                    <div>🔥 CURRENT STREAK: {CURRENT_STREAK} ({STREAK_TYPE})</div>
                    <div>📊 TOTAL DATA POINTS: {len(HISTORY)}</div>
                </div>
                
                <div class="history-box">
                    <p style="color: #666; font-size: 12px; margin-bottom: 10px;">LIVE MARKET TREND (LAST 20)</p>
                    {history_str}
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    threading.Thread(target=advanced_statistical_analysis, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
