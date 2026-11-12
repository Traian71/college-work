import threading, time as rt, types, sys, math, random, re
RC = sys.argv[1]; SCALE = 10.0
lock = threading.RLock(); sockets = {}; T0 = rt.time(); out = {}
def mk(ipself, name):
    m_udp = types.ModuleType("udp"); m_time = types.ModuleType("time")
    class UDPSocket:
        def onReceive(self, cb): self.cb = cb
        def begin(self, port): sockets[ipself] = self
        def send(self, ip, port, data):
            s = sockets.get(ip)
            if s:
                def d(): 
                    rt.sleep(random.uniform(0.001,0.004))
                    with lock: s.cb(ipself, port, data)
                threading.Thread(target=d, daemon=True).start()
            return True
    m_udp.UDPSocket = UDPSocket
    m_time.uptime = lambda: (rt.time()-T0)*SCALE
    m_time.sleep = lambda s: rt.sleep(max(0,s)/SCALE)
    out[name] = []
    def pr(*a): out[name].append(" ".join(str(x) for x in a))
    return m_udp, m_time, pr
def run(name, ip, src):
    u, t, pr = mk(ip, name)
    sys.modules["udp"] = u; sys.modules["time"] = t
    g = {"__name__": "__main__", "print": pr}
    code = compile(src, name, "exec")
    # run with modules injected via a custom import
    import builtins
    real_import = builtins.__import__
    def imp(n, *a, **k):
        if n == "udp": return u
        if n == "time": return t
        return real_import(n, *a, **k)
    g["__builtins__"] = dict(vars(builtins), __import__=imp, print=pr)
    # wrap sleep in loops under lock-free; callbacks take lock
    threading.Thread(target=lambda: exec(code, g), daemon=True).start()
A = open(f"{RC}/sursa_A.py").read(); M = open(f"{RC}/membru.py").read()
def membru(j, l): return re.sub(r"LEAVE_DUPA = -1", f"LEAVE_DUPA = {l}", re.sub(r"JOIN_DUPA = 0", f"JOIN_DUPA = {j}", M))
run("A", "192.168.1.1", A); rt.sleep(0.05)
for n, ip, j, l in [("B","192.168.1.2",0,-1),("C","192.168.1.3",0,25),("D","192.168.1.4",0,-1),("E","192.168.1.5",15,-1)]:
    run(n, ip, membru(j, l)); rt.sleep(0.02)
rt.sleep(4.6)
for n in "ABCDE":
    L = out[n]
    keep = [x for x in L if not x.startswith("n = ") or n=="A" and ("trimiteri: 4" in x or "trimiteri: 2" in x)]
    print("-----", n, len(L)); print("\n".join(keep[:14] + (["..."] + keep[-8:] if len(keep) > 22 else keep[14:])))
