import requests
import time

# আগের সব BSBS মুছে একদম খালি করে দিলাম মামা
DATABASE = ""

def get_live_result():
    try:
        # DK Win 30S এর জন্য আপাতত ডামি রেজাল্ট
        return "S" 
    except:
        return None

def start_bot():
    global DATABASE
    print("TITAN AI: DK Win (30S) Started with Fresh Memory...")
    
    while True:
        new_res = get_live_result()
        if new_res:
            DATABASE += new_res
            print(f"New Data: {new_res} | Total DB: {DATABASE}")
        
        time.sleep(20)

if __name__ == "__main__":
    start_bot()
