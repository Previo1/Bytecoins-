# bytecoin_node_persistent.py
# Persistent Bytecoin Node + Miner + Explorer
import time, json, hashlib, threading
from flask import Flask, request, jsonify
from ecdsa import SigningKey, SECP256k1
import base58
import db

app = Flask(__name__)
mempool = []
mining = False

def sha256d(x): return hashlib.sha256(hashlib.sha256(x).digest()).hexdigest()

def new_keypair():
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    priv = sk.to_string().hex()
    pub = vk.to_string().hex()
    addr = base58.b58encode_check(b'\x00'+hashlib.new('ripemd160', hashlib.sha256(vk.to_string()).digest()).digest()).decode()
    return priv, pub, addr

@app.route("/wallet/new")
def wallet_new():
    priv, pub, addr = new_keypair()
    return jsonify({"priv": priv, "pub": pub, "address": addr})

@app.route("/tx/create", methods=["POST"])
def tx_create():
    data = request.json
    tx = {
        "from": data["from"],
        "to": data["to"],
        "amount": data["amount"],
        "timestamp": int(time.time())
    }
    txid = sha256d(json.dumps(tx).encode())
    tx["txid"] = txid
    mempool.append(tx)
    db.insert_tx(txid, tx, None)
    return jsonify(tx)

def mine_loop(miner_addr):
    global mining
    while mining:
        block = {
            "height": int(time.time()), # demo only
            "previous": "0"*64,
            "txs": [tx["txid"] for tx in mempool],
            "timestamp": int(time.time()),
            "nonce": 0
        }
        while mining:
            block["nonce"] += 1
            h = sha256d(json.dumps(block).encode())
            if h.startswith("0000"):
                block["hash"] = h
                db.insert_block(block)
                for tx in mempool:
                    db.insert_tx(tx["txid"], tx, block["height"])
                mempool.clear()
                break

@app.route("/mine/start", methods=["POST"])
def mine_start():
    global mining
    if mining: return jsonify({"status": "already mining"})
    mining = True
    addr = request.json["miner_address"]
    threading.Thread(target=mine_loop, args=(addr,), daemon=True).start()
    return jsonify({"status": "started"})

@app.route("/mine/stop", methods=["POST"])
def mine_stop():
    global mining
    mining = False
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    db.init_schema()
    app.run(port=5000)
