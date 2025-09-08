CREATE TABLE IF NOT EXISTS blocks (
  height INTEGER PRIMARY KEY,
  hash TEXT UNIQUE NOT NULL,
  previous_hash TEXT,
  merkle_root TEXT,
  timestamp BIGINT,
  difficulty TEXT,
  nonce BIGINT,
  tx_count INTEGER
);

CREATE TABLE IF NOT EXISTS transactions (
  txid TEXT PRIMARY KEY,
  block_height INTEGER,
  raw JSONB
);

CREATE TABLE IF NOT EXISTS utxos (
  txid TEXT,
  idx INTEGER,
  address TEXT,
  value NUMERIC,
  PRIMARY KEY (txid, idx)
);

CREATE INDEX IF NOT EXISTS idx_utxos_address ON utxos(address);
CREATE INDEX IF NOT EXISTS idx_blocks_hash ON blocks(hash);
CREATE INDEX IF NOT EXISTS idx_tx_block ON transactions(block_height);
