# indexer.py
import time, json, requests
import db

NODE = "http://127.0.0.1:5000"

while True:
    try:
        blocks = requests.get(f"{NODE}/blocks").json()
        for b in blocks:
            h = b["height"]
            block = requests.get(f"{NODE}/block/{h}").json()
            db.insert_block(block)
            for txid in block["txs"]:
                tx = requests.get(f"{NODE}/tx/{txid}").json()
                db.insert_tx(txid, tx, h)
    except Exception as e:
        print("Indexer error:", e)
    time.sleep(5)
