import secrets, time, datetime, signal, sys

token = secrets.token_hex(16)  # 32-char hex string

def stop(_sig, _f):
    print("Shutting down", flush=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, stop)

while True:
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"{ts}: {token}", flush=True)
    time.sleep(5)
