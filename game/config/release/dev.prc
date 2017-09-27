# Distribution:
distribution dev

# Art assets:
model-path ../resources

# Server:
server-version rttim-v69.6
min-access-level 700
accountdb-type local
shard-low-pop 50
shard-mid-pop 100

# RPC:
want-rpc-server #f
rpc-server-endpoint http://localhost:7199/

# DClass files (in reverse order):
dc-file astron/dclass/toon.dc
dc-file astron/dclass/otp.dc

# Core features:
want-pets #f
want-parties #f
want-cogdominiums #f
want-achievements #f

# Chat:
want-whitelist #f

# Cashbot boss:
want-resistance-toonup #t
want-resistance-restock #t
want-resistance-dance #t

# Optional:
want-yin-yang #f

# Developer options:
show-population #t
force-skip-tutorial #f
want-instant-parties #t
