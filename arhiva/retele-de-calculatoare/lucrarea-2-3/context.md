# Rețele de calculatoare – Lucrarea 2&3 RC

- **Task (Moodle, assignment "Lucrarea 2&3 RC"):** upload one PDF with the solved exercises from lucrările 2 and 3
  (for students with RC labs in the weeks 19–30.10.2026). Opened 26 Oct, **due Sun 1 Nov 2026, 23:59**; work started
  on 2 Nov, after the deadline (the Moodle page still allowed a submission). One file, PDF/DOC/DOCX/ODT/RTF/EPUB.
- **Handouts:** `materiale/RC Lucrarea 2.pdf` (IP addresses, subnetting, Packet Tracer basics; ex. 1–6) and
  `materiale/RC Lucrarea 3.pdf` (hierarchical networks, subnets, VLANs; ex. 1–3). Lucrarea 1 is still in
  `retele-de-calculatoare/` (not part of this assignment).
- **Hand-in:** `retele-de-calculatoare/lucrarea-2-3/Lucrarea_2_3_RC.pdf`, built from `sursa/README.md` with
  `python3 sursa/build.py` (marked.js + headless Chrome). Screenshots go in `sursa/capturi/`; a missing one shows
  as a dashed placeholder.
- **Answers in short:**
  - L2 ex1: /28 → mask .240, net .96, bcast .111, 14 hosts (.97–.110); /27 gives 30 → +16.
  - L2 ex2: four /17 (255.255.128.0), 32766 hosts each. Ex3: /16 + /17, last /17 unused. Ex4: 192.168.0.0/28
    split into four /30.
  - L2 ex5: /30 → only 2 stations. Ex6: 4-port switches → min 4 switches (2k+2 ≥ 9), max 9 (one PC each).
  - L3 ex1: 45 PCs don't fit on 3×16 ports (44 free) → 4 switches: one per floor + central on floor 2; all in /16.
    Ex2: same wiring, /27 per floor (.0, .32, .64), no gateway so inter-floor ping fails. Ex3: VLAN 2 purchase
    (Fa0/1–2), VLAN 3 sales (Fa0/3–4).
- **Names used:** switch `FileMititaT441A` (from the handout's `IonescuA441A` example), switches for ex6
  `FileMititaT441A01`–`04`, stations `FT01`… (initials File Traian).
- **Packet Tracer:** the online version linked in the handout (packettracernetwork.com/ptanywhere) didn't respond on
  2 Nov 2026. Cisco Packet Tracer for Mac is free from netacad.com (needs a NetAcad login). Claude can't click inside
  desktop apps, so Traian builds the networks and takes the screenshots following the steps below.

## Steps in Packet Tracer (5 screenshots)

General:
- Switch: *Network Devices → Switches → 2960*. PC: *End Devices → PC*.
- Cables: *Connections* (lightning icon). PC → switch: **Copper Straight-Through**, choose FastEthernet0 on the PC
  and the switch port listed below. Switch → switch: **Copper Cross-Over**.
- Name: click the device → *Config* → *Display Name*.
- IP: PC → *Desktop → IP Configuration* → IP Address and Subnet Mask (leave the gateway empty).
- Links turn green after ~30 s (or click *Fast Forward Time* at the bottom).
- Ping: PC → *Desktop → Command Prompt* → `ping <ip>`.
- Screenshot: leave the Command Prompt window open over the topology, then **Cmd+Shift+4, Space, click the Packet
  Tracer window**. It lands on the Desktop. Take them in this order:

1. **L2 ex5** → `capturi/l2-ex5.png`: 1 switch `FileMititaT441A`, `FT01` 192.168.0.1 and `FT02` 192.168.0.2, mask
   255.255.255.252. From FT01: `ping 192.168.0.2`.
2. **L2 ex6** → `capturi/l2-ex6.png`: switches `FileMititaT441A01` (central) cross-over to `…02`, `…03`, `…04`.
   FT01–FT03 on 02, FT04–FT06 on 03, FT07–FT09 on 04. FTn = 192.168.0.n, mask 255.255.255.0. From FT01:
   `ping 192.168.0.9`.
3. **L3 ex1** → `capturi/l3-ex1.png` (new file): switches `Central`, `Etaj1`, `Etaj2`, `Etaj3`, each floor switch
   cross-over to Central. PCs `E1-PC1..3` = 192.168.1.1–3, `E2-PC1..3` = 192.168.2.1–3, `E3-PC1..3` = 192.168.3.1–3,
   all mask 255.255.0.0. From E1-PC1: `ping 192.168.2.1` and `ping 192.168.3.1`.
4. **L3 ex2** → `capturi/l3-ex2.png` (same file, only change IPs): E1 = 192.168.0.1–3, E2 = 192.168.0.33–35,
   E3 = 192.168.0.65–67, all mask 255.255.255.224. From E1-PC1: `ping 192.168.0.2` (works) and
   `ping 192.168.0.33` (fails).
5. **L3 ex3** → `capturi/l3-ex3.png` (new file): 1 switch; P1 on Fa0/1 = 192.168.10.1, P2 on Fa0/2 = .2, S1 on
   Fa0/3 = .3, S2 on Fa0/4 = .4, mask 255.255.255.0. Switch → *CLI* tab (answer `no` to the setup dialog), paste the
   commands from exercise 3 in the PDF. From P1: `ping 192.168.10.2` (works) and `ping 192.168.10.3` (timeout).

- **Status (2 Nov 2026):** calculations done, PDF draft built with placeholders; waiting for the 5 screenshots.
  Not uploaded yet.
