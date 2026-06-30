import os, sys, json, time, threading, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("BOT_TOKEN", "")
PORT  = int(os.getenv("PORT", "8080"))

def tg(text):
    try:
        data = json.dumps({"chat_id":"8725437154","text":text}).encode()
        req  = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                      data=data, headers={"Content-Type":"application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print("tg_send error:", e, flush=True)

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"OK PORT=" + str(PORT).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(body))); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

print(f"[STARTUP] PORT={PORT} TOKEN={'ok' if TOKEN else 'MISSING'}", flush=True)
tg(f"[MINIMAL BOT] iniciou! PORT={PORT} TOKEN={'ok' if TOKEN else 'MISSING'}")

try:
    srv = HTTPServer(("0.0.0.0", PORT), H)
    print(f"[HTTP] OK na porta {PORT}", flush=True)
    tg(f"[MINIMAL BOT] HTTP server OK na porta {PORT}")
    srv.serve_forever()
except Exception as e:
    print(f"[HTTP] FALHOU: {e}", flush=True)
    tg(f"[MINIMAL BOT] HTTP FALHOU: {e}")
    while True: time.sleep(60)
