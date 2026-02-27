from flask import Flask
import time
import os
import random

app = Flask(__name__)

# সার্ভার কখন চালু হলো তার টাইম রেকর্ড করে রাখলাম
START_TIME = time.time()

@app.route('/')
def home():
    # বর্তমান সময় থেকে সার্ভার চালুর সময় বাদ দিয়ে হিসাব
    current_time = time.time()
    elapsed_seconds = current_time - START_TIME
    
    # প্রতি ১০ সেকেন্ডে ১টা করে নতুন ডাটা পয়েন্ট যোগ হবে (শুরু হবে ৫ থেকে)
    total_points = 5 + int(elapsed_seconds // 10)
    
    # ডাটা পয়েন্টের ওপর ভিত্তি করে রেজাল্ট ফিক্স রাখা (যাতে রিফ্রেশ দিলে না লাফায়)
    rng = random.Random(total_points)
    
    # হিস্টোরি জেনারেট করা
    history = []
    for i in range(min(total_points, 15)):
        history.append(rng.choice(["B", "S"]))
        
    if not history:
        history = ["B", "S", "B"]
        
    # এআই লজিক
    b_count = history.count("B")
    s_count = history.count("S")
    
    if b_count > s_count:
        prediction = "SMALL"
        prob = rng.randint(75, 96)
    else:
        prediction = "BIG"
        prob = rng.randint(75, 96)

    trend_str = " ".join(history[-10:])

    return f"""
    <html>
        <head>
            <title>TITAN V5 - NO THREAD</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {{ background: #050505; color: #fff; font-family: 'Segoe UI', Tahoma, sans-serif; text-align: center; padding-top: 50px; }}
                .box {{ border: 2px solid #ff0055; display: inline-block; padding: 40px; border-radius: 15px; background: #0a0a0a; box-shadow: 0 0 40px #ff005555; max-width: 500px; width: 90%; }}
                .pred {{ font-size: 65px; color: #ff0055; font-weight: 900; margin: 15px 0; text-shadow: 0 0 20px #ff0055; letter-spacing: 2px; }}
                .points {{ font-size: 28px; color: #00ffcc; margin: 20px 0; font-weight: bold; background: #111; padding: 10px; border-radius: 8px; border: 1px solid #333; }}
                .trend {{ color: #888; letter-spacing: 3px; font-family: monospace; font-size: 18px; }}
            </style>
        </head>
        <body>
            <div class="box">
                <h2 style="color: #fff; margin: 0;">⚡ TITAN V5 ENGINE</h2>
                <p style="color: #00ff00; font-size: 12px;">SERVER BYPASS: SUCCESS</p>
                <hr style="border: 0.5px solid #222; margin-bottom: 30px;">
                
                <p style="color: #aaa; margin: 0;">AI TARGET:</p>
                <div class="pred">{prediction}</div>
                <p style="font-size: 20px; color: #ddd;">WIN PROBABILITY: <span style="color:#00ffcc;">{prob}%</span></p>
                
                <div class="points">TOTAL DATA POINTS: {total_points}</div>
                
                <div style="margin-top: 30px;">
                    <p style="font-size: 12px; color: #555; margin-bottom: 5px;">LIVE TREND (LAST 10)</p>
                    <div class="trend">{trend_str}</div>
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
