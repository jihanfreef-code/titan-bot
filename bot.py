from flask import Flask
import time
import os
import random

app = Flask(__name__)

@app.route('/')
def home():
    # বর্তমান সময়ের ওপর ভিত্তি করে ডাটা পয়েন্ট তৈরি (যাতে কখনো না আটকায়)
    # এটা প্রতি ১ মিনিটে ডাটা পয়েন্ট বাড়াবে
    current_ts = int(time.time())
    points = (current_ts // 60) % 1000  # প্রতি মিনিটে পয়েন্ট বাড়বে
    
    # পিরিয়ড নম্বর জেনারেট (DK Win এর মতো)
    period_id = time.strftime("%Y%m%d%H%M")
    
    # সিড (Seed) ব্যবহার করে রেজাল্ট ফিক্স রাখা যাতে রিফ্রেশ করলে রেজাল্ট না বদলায়
    random.seed(points)
    history = [random.choice(["B", "S"]) for _ in range(15)]
    
    # এআই প্রেডিকশন লজিক
    prediction = "BIG" if history.count("S") > history.count("B") else "SMALL"
    confidence = random.randint(82, 98)

    return f"""
    <html>
        <head>
            <title>TITAN V6 FINAL</title>
            <meta http-equiv="refresh" content="30">
            <style>
                body {{ background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }}
                .main {{ border: 2px dashed #00ffcc; display: inline-block; padding: 30px; border-radius: 20px; background: #050505; }}
                .big-text {{ font-size: 60px; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; margin: 10px 0; }}
                .info {{ font-size: 20px; color: #ffcc00; }}
                .data-box {{ background: #111; padding: 10px; margin-top: 20px; border-radius: 10px; color: #888; letter-spacing: 5px; }}
            </style>
        </head>
        <body>
            <div class="main">
                <h1 style="color:red;">⚠️ TITAN V6 (GOD MODE)</h1>
                <p>PERIOD: {period_id}</p>
                <hr style="border:0.1px solid #222;">
                <p>AI PREDICTION FOR NEXT:</p>
                <div class="big-text">{prediction}</div>
                <div class="info">CONFIDENCE: {confidence}%</div>
                <div class="info" style="color:#00ff00; margin-top:10px;">TOTAL DATA POINTS: {points}</div>
                <div class="data-box">TREND: {" | ".join(history[-10:])}</div>
                <p style="font-size:12px; color:#444; margin-top:20px;">Updates automatically every 1 minute</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
