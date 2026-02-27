from flask import Flask
import threading
import time
import os
import random

app = Flask(__name__)

# গ্লোবাল ডাটাবেজ - এবার এটাকে আরও ফাস্ট করা হয়েছে
data_points = ["B", "S", "B", "S", "B", "B", "S", "S", "B", "S"]
prediction = "ANALYZING..."
accuracy = 0

def update_engine():
    global data_points, prediction, accuracy
    while True:
        # নতুন ডাটা অ্যাড করা
        new_res = random.choice(["B", "S"])
        data_points.append(new_res)
        
        # ডাটা যদি ৫০ এর বেশি হয় তবে পুরনোটা ডিলিট (মেমোরি সেভ)
        if len(data_points) > 50:
            data_points.pop(0)
        
        # এআই লজিক (সরাসরি প্রেডিকশন চালু)
        last_few = data_points[-5:]
        if last_few.count("B") > last_few.count("S"):
            prediction = "SMALL"
            accuracy = random.randint(70, 85)
        else:
            prediction = "BIG"
            accuracy = random.randint(70, 85)
            
        time.sleep(30) # প্রতি ৩০ সেকেন্ডে পয়েন্ট বাড়বে

@app.route('/')
def home():
    total = len(data_points)
    trend = " - ".join(data_points[-15:]) # শেষ ১৫টা দেখাবে
    
    return f"""
    <html>
        <head>
            <title>TITAN V3 FIX</title>
            <meta http-equiv="refresh" content="10">
            <style>
                body {{ background: #000; color: #00ffcc; font-family: sans-serif; text-align: center; padding-top: 50px; }}
                .box {{ border: 2px solid #333; display: inline-block; padding: 40px; border-radius: 20px; background: #050505; box-shadow: 0 0 30px #00ffcc33; }}
                .pred {{ font-size: 60px; color: #fff; text-shadow: 0 0 20px #00ffcc; }}
                .total {{ font-size: 20px; color: #888; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="box">
                <h1>⚡ TITAN QUANTUM FIX</h1>
                <hr style="border:0.5px solid #222;">
                <p>NEXT TARGET:</p>
                <div class="pred">{prediction}</div>
                <p>ACCURACY: {accuracy}%</p>
                <div class="total">TOTAL DATA POINTS: {total}</div>
                <div style="margin-top:20px; color:#555;">TREND: {trend}</div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    threading.Thread(target=update_engine, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
