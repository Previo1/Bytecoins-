# db.py
import psycopg2, psycopg2.extras
from contextlib import contextmanager

DSN = "dbname=bytecoin user=postgres password=password host=127.0.0.1"

@contextmanager
def get_conn():
    conn = psycopg2.connect(DSN)
    try:
        yield conn
    finally:
        conn.close()

def init_schema():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(open("schema.sql").read())
        conn.commit()

def insert_block(block):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO blocks (height, hash, previous_hash, merkle_root, timestamp, difficulty, nonce, tx_count) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (height) DO NOTHING",
            (block["height"], block["hash"], block["previous"], block.get("merkle_root",""),
             block["timestamp"], "0000", block.get("nonce",0), len(block.get("txs",[])))
        )
        conn.commit()

def insert_tx(txid, raw, block_height=None):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO transactions (txid, block_height, raw) VALUES (%s,%s,%s) "
                    "ON CONFLICT (txid) DO NOTHING", (txid, block_height, psycopg2.extras.Json(raw)))
        conn.commit()
