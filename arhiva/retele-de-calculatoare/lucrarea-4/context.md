# Rețele de calculatoare – Lucrarea 4 RC

- **Cerința** (`materiale/RC Lucrarea 4.pdf`, „Simularea rețelelor de calculatoare (partea a 3-a)”, rutare statică):
  - Ex. 1: „Realizati reteaua descrisa mai sus utilizand simulatorul online Cisco Packet Tracer. Atribuiti nume personalizat
    elementelor (PCIonescuP01, SwitchIonescuP0, RouterIonescuP0 etc.)”
  - Ex. 2: „Completati schema de la exercitiul 1 si adaugati mai multe statii in fiecare retea, realizati setarile IP necesare si
    verificati existenta conectivitatii intre diferite statii din cele doua retele. Rulati comanda tracert si observati nodurile
    traversate de pachetele.”
- **Primit:** 20 nov 2026 de la Traian, de rezolvat complet în Packet Tracer prin MCP. Termen necunoscut: pe Moodle **nu există
  încă temă** pentru Lucrarea 4 RC (Lucrarea 2&3 a avut „Lucrarea 2&3 RC”, assignid 5335). Format nespecificat → PDF, ca la 2&3.
- **Livrabil:** `retele-de-calculatoare/lucrarea-4/Lucrarea_4_RC.pdf` (2 pagini), copiat și pe Desktop. Neîncărcat.
- **Rețeaua** (PT 9.0.1, `sursa/Lucrarea4_RC_FileMitita_Traian.pkt`, starea finală de la ex. 2):
  - R1 = RouterFileMititaT0 (2911): Gi0/0 192.168.5.1, Gi0/2 10.1.1.1, `ip route 192.168.10.0 255.255.255.0 10.1.1.2`.
  - R2 = RouterFileMititaT1 (2911): Gi0/0 192.168.10.1, Gi0/2 10.1.1.2, `ip route 192.168.5.0 255.255.255.0 10.1.1.1`.
  - Switch-uri 2960: SwitchFileMititaT0 (rețeaua #1), SwitchFileMititaT1 (#2), SwitchFileMititaT2 (rutere); legături la rutere
    pe Gi0/1 (switch) → Gi0/0 (ruter), ruterele la SwitchFileMititaT2 pe Gi0/1 și Gi0/2.
  - PC-uri: PCFileMititaT01 192.168.5.2 (PC0), T02 .3, T03 .4; PCFileMititaT11 192.168.10.2 (PC1), T12 .3, T13 .4. Măști /24.
- **Rezultate văzute:** ping R1→10.1.1.2 merge (.!!!! apoi !!!!!). Înainte de rute: PC→ruterul propriu merge, PC→cealaltă rețea
  „Destination host unreachable”. După rute: PC0↔rețeaua #2 și PC1↔rețeaua #1 merg (TTL 254 / 126). Ex. 2: PC02→PC12/PC13 și
  PC13→PC03/PC02 merg; tracert 192.168.5.1 → 10.1.1.2 → 192.168.10.4 și invers 192.168.10.1 → 10.1.1.1 → 192.168.5.3.
- **Cum s-a făcut:** dispozitive, cabluri, IP-uri PC și adresele pe rutere prin cisco-pt-mcp (`arhiva/apd/proiect-027/sursa/pt/pt_daemon.py`;
  portul 7531 era ținut de un server MCP rămas dintr-o sesiune Claude din VS Code din 19 nov, oprit). Rutele statice, `show ip route`,
  ping-urile și tracert-urile tastate în CLI / Command Prompt din PT (osascript + `clic`), capturi cu `screencapture -l`.
- **Surse** (`sursa/`): `README.md` (textul) → `python3 build.py` → PDF; `decupeaza.py` taie `capturi_brute/` în `capturi/`.
- **Status:** gata, neîncărcat. De încărcat când apare tema pe Moodle.
