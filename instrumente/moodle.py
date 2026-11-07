#!/usr/bin/env python3
"""Mic client pentru Moodle-ul UPB (curs.upb.ro/2026), prin API-ul aplicatiei mobile.

Tokenul nu sta in repo: e in Keychain (serviciul "moodle-upb-token"). Fara biblioteci externe.

  python3 instrumente/moodle.py whoami
  python3 instrumente/moodle.py due [--days 21]            # teme de predat / intarziate
  python3 instrumente/moodle.py show <assignid>            # enunt, atasamente, ce fisiere accepta
  python3 instrumente/moodle.py files <courseid> [--grep text]   # fisierele din curs (laboratoare etc.)
  python3 instrumente/moodle.py download <assignid> <folder>     # atasamentele temei
  python3 instrumente/moodle.py get <fileurl> <fisier>           # un fisier din `files`
  python3 instrumente/moodle.py submit <assignid> <fisier>... [--yes]   # fara --yes doar arata ce ar face
"""
import argparse, html, json, mimetypes, re, subprocess, sys, time, uuid
import urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

BASE = "https://curs.upb.ro/2026"


def token():
    try:
        return subprocess.run(["security", "find-generic-password", "-s", "moodle-upb-token", "-w"],
                              check=True, capture_output=True, text=True).stdout.strip()
    except subprocess.CalledProcessError:
        sys.exit("Nu gasesc tokenul in Keychain (serviciul moodle-upb-token).")


def flatten(params, prefix=""):
    out = {}
    for k, v in params.items():
        key = f"{prefix}[{k}]" if prefix else str(k)
        if isinstance(v, dict):
            out.update(flatten(v, key))
        elif isinstance(v, (list, tuple)):
            out.update(flatten(dict(enumerate(v)), key))
        elif isinstance(v, bool):
            out[key] = int(v)
        else:
            out[key] = v
    return out


def call(fn, **params):
    data = {"wstoken": token(), "wsfunction": fn, "moodlewsrestformat": "json", **flatten(params)}
    req = urllib.request.Request(f"{BASE}/webservice/rest/server.php",
                                 data=urllib.parse.urlencode(data).encode())
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.load(r)
    if isinstance(res, dict) and res.get("exception"):
        sys.exit(f"{fn}: {res.get('errorcode')}: {res.get('message')}")
    return res


def text(h):
    h = re.sub(r"<(br|/p|/li|/div)[^>]*>", "\n", h or "", flags=re.I)
    return re.sub(r"\n{3,}", "\n\n", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def when(ts):
    return datetime.fromtimestamp(ts).strftime("%a %d %b %Y %H:%M") if ts else "fara termen"


def me():
    return call("core_webservice_get_site_info")


def courses():
    return call("core_enrol_get_users_courses", userid=me()["userid"])


def assignments():
    cs = courses()
    res = call("mod_assign_get_assignments", courseids=[c["id"] for c in cs])
    names = {c["id"]: c["fullname"] for c in cs}
    for c in res["courses"]:
        for a in c["assignments"]:
            a["coursename"] = names.get(c["id"], c["fullname"])
            yield a


def status(assignid):
    s = call("mod_assign_get_submission_status", assignid=assignid)
    la = s.get("lastattempt") or {}
    sub = la.get("submission") or la.get("teamsubmission") or {}
    files = [f["filename"] for p in sub.get("plugins", []) for fa in p.get("fileareas", [])
             for f in fa.get("files", [])]
    return sub.get("status", "new"), files, s


def download(url, dest):
    sep = "&" if "?" in url else "?"
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(f"{url}{sep}token={token()}", timeout=120) as r:
        dest.write_bytes(r.read())
    print(f"  {dest} ({dest.stat().st_size} B)")


def cmd_whoami(a):
    i = me()
    print(f"{i['fullname']} ({i['username']}), userid {i['userid']}, {i['sitename']}")
    for c in courses():
        print(f"  [{c['id']}] {c['fullname']}")


def cmd_due(a):
    now = time.time()
    rows = []
    for x in assignments():
        due = x.get("duedate") or 0
        if due and due > now + a.days * 86400:
            continue
        if due and due < now - a.past * 86400:
            continue
        st, files, _ = status(x["id"])
        if st == "submitted" and not a.all:
            continue
        rows.append((due or 9e12, x, st, files))
    for due, x, st, files in sorted(rows, key=lambda r: r[0]):
        late = " INTARZIAT" if x.get("duedate") and x["duedate"] < now and st != "submitted" else ""
        print(f"{when(x.get('duedate'))}{late} | {x['coursename']}\n"
              f"   {x['name']}  (assignid {x['id']}, cmid {x['cmid']}, status: {st}"
              f"{', fisiere: ' + ', '.join(files) if files else ''})")
    if not rows:
        print("Nimic de predat in intervalul ales.")
    # alte termene (teste, chestionare etc.) din calendar
    ev = call("core_calendar_get_action_events_by_timesort", timesortfrom=int(now - a.past * 86400),
              timesortto=int(now + a.days * 86400), limitnum=50).get("events", [])
    other = [e for e in ev if e.get("modulename") != "assign"]
    if other:
        print("\nAlte termene din calendar:")
    for e in other:
        print(f"{when(e['timesort'])} | {e.get('course', {}).get('fullname', '')}\n"
              f"   {e['name']} ({e.get('modulename')}) {e.get('url', '')}")


def cmd_show(a):
    x = next((x for x in assignments() if x["id"] == a.assignid), None)
    if not x:
        sys.exit("Nu gasesc tema.")
    st, files, _ = status(x["id"])
    cfg = {(c["plugin"], c["name"]): c["value"] for c in x.get("configs", [])}
    print(f"{x['name']} | {x['coursename']}\nTermen: {when(x.get('duedate'))}, "
          f"limita: {when(x.get('cutoffdate'))}, status: {st} {files or ''}")
    print(f"Fisiere acceptate: {cfg.get(('file', 'filetypeslist')) or 'orice'}, "
          f"max {cfg.get(('file', 'maxfilesubmissions'), '?')} fisiere; text online: "
          f"{'da' if cfg.get(('onlinetext', 'enabled')) == '1' else 'nu'}; "
          f"buton 'submit for grading': {'da' if x.get('submissiondrafts') else 'nu'}")
    print(f"Link: {BASE}/mod/assign/view.php?id={x['cmid']}\n\n{text(x.get('intro'))}")
    for f in x.get("introattachments", []):
        print(f"\nAtasament: {f['filename']}  {f['fileurl']}")


def cmd_files(a):
    for sec in call("core_course_get_contents", courseid=a.courseid):
        for m in sec.get("modules", []):
            for f in m.get("contents", []) or []:
                if f.get("type") != "file":
                    continue
                line = f"{sec['name']} / {m['name']} / {f['filename']}"
                if a.grep and a.grep.lower() not in line.lower():
                    continue
                print(f"{line}\n   {when(f.get('timemodified'))}  {f['fileurl']}")


def cmd_download(a):
    x = next((x for x in assignments() if x["id"] == a.assignid), None)
    if not x:
        sys.exit("Nu gasesc tema.")
    att = x.get("introattachments", [])
    if not att:
        print("Tema nu are atasamente (enuntul e probabil o resursa separata in curs: vezi `files`).")
    for f in att:
        download(f["fileurl"], Path(a.folder) / f["filename"])


def cmd_get(a):
    download(a.fileurl, a.dest)


def upload(paths):
    """Urca fisierele in zona draft a utilizatorului; intoarce itemid-ul."""
    itemid = 0
    for p in paths:
        p = Path(p)
        b = uuid.uuid4().hex
        fields = {"token": token(), "filearea": "draft", "itemid": itemid}
        body = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
                        for k, v in fields.items())
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        body += (f'--{b}\r\nContent-Disposition: form-data; name="file_1"; filename="{p.name}"\r\n'
                 f"Content-Type: {ctype}\r\n\r\n").encode() + p.read_bytes() + f"\r\n--{b}--\r\n".encode()
        req = urllib.request.Request(f"{BASE}/webservice/upload.php", data=body,
                                     headers={"Content-Type": f"multipart/form-data; boundary={b}"})
        with urllib.request.urlopen(req, timeout=300) as r:
            res = json.load(r)
        if isinstance(res, dict) and res.get("error"):
            sys.exit(f"upload: {res['error']}")
        itemid = res[0]["itemid"]
        print(f"  urcat {p.name} -> draft {itemid}")
    return itemid


def cmd_submit(a):
    x = next((x for x in assignments() if x["id"] == a.assignid), None)
    if not x:
        sys.exit("Nu gasesc tema.")
    for p in a.files:
        if not Path(p).is_file():
            sys.exit(f"Lipseste {p}")
    st, files, _ = status(x["id"])
    print(f"Tema: {x['name']} | {x['coursename']} | termen {when(x.get('duedate'))}\n"
          f"Status acum: {st} {files or ''}\nFisiere noi (inlocuiesc ce e acolo): "
          f"{', '.join(Path(p).name for p in a.files)}")
    if not a.yes:
        print("\nNu am trimis nimic (ruleaza cu --yes ca sa trimiti).")
        return
    itemid = upload(a.files)
    call("mod_assign_save_submission", assignmentid=x["id"],
         plugindata={"files_filemanager": itemid})
    if x.get("submissiondrafts"):
        call("mod_assign_submit_for_grading", assignmentid=x["id"], acceptsubmissionstatement=1)
    st, files, _ = status(x["id"])
    print(f"Gata. Status: {st}, fisiere: {', '.join(files)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("whoami").set_defaults(f=cmd_whoami)
    p = sp.add_parser("due")
    p.add_argument("--days", type=int, default=21, help="cate zile in fata (implicit 21)")
    p.add_argument("--past", type=int, default=60, help="cat de vechi pot fi intarzierile (implicit 60)")
    p.add_argument("--all", action="store_true", help="arata si temele deja trimise")
    p.set_defaults(f=cmd_due)
    p = sp.add_parser("show"); p.add_argument("assignid", type=int); p.set_defaults(f=cmd_show)
    p = sp.add_parser("files"); p.add_argument("courseid", type=int); p.add_argument("--grep")
    p.set_defaults(f=cmd_files)
    p = sp.add_parser("download"); p.add_argument("assignid", type=int); p.add_argument("folder")
    p.set_defaults(f=cmd_download)
    p = sp.add_parser("get"); p.add_argument("fileurl"); p.add_argument("dest"); p.set_defaults(f=cmd_get)
    p = sp.add_parser("submit"); p.add_argument("assignid", type=int); p.add_argument("files", nargs="+")
    p.add_argument("--yes", action="store_true"); p.set_defaults(f=cmd_submit)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
