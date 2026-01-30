import json
import csv
import os
from datetime import datetime

APP_TITLE = "Instagram Following Review"


def _print_entry(pos: int, total: int, row_id: int, username: str, url: str, date_str: str, status: str) -> None:
    print("=" * 50)
    print(f"Entry {pos}/{total}")
    print(f"ID:        {row_id}")
    print(f"Username:  {username}")
    print(f"URL:       {url}")
    print(f"Date:      {date_str}")
    print(f"Status:    {status}")
    print("\nEnter = done | r = change status | q = quit")

def export_followings_to_csv(base_name: str) -> str:
    """
    Reads {base_name}.json (Instagram export) and writes {base_name}.csv
    with: id, username, url, timestamp
    """
    json_path = f"{base_name}.json"
    csv_path = f"{base_name}.csv"

    with open(json_path, "r", encoding="utf-8") as f:
        followings = json.load(f)["relationships_following"]

    structured = []
    for item in followings:
        title = item.get("title", "")
        sld = (item.get("string_list_data") or [{}])[0] or {}
        href = sld.get("href", "")
        ts = sld.get("timestamp")
        try:
            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            date_str = ""

        structured.append((title, href, date_str))

    structured = structured[::-1]  # oldest first

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(("id", "username", "url", "timestamp"))
        for idx, data in enumerate(structured):
            writer.writerow((idx,) + data)

    return csv_path


def _load_done_ids(edited_csv_path: str) -> set[int]:
    """
    Reads the edited CSV and collects all already-processed IDs,
    so the script can resume cleanly after a restart.
    """
    if not os.path.exists(edited_csv_path):
        return set()

    done = set()
    with open(edited_csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                done.add(int(row["id"]))
            except Exception:
                continue
    return done


def interactive_review_followings(base_name: str) -> str:
    """
    Reads {base_name}.csv and writes/appends edited_{base_name}.csv.
    For each not-yet-reviewed row, you can toggle the status (keep/delete)
    and confirm with Enter. Writes immediately after each confirmed entry.
    """
    source_csv = f"{base_name}.csv"
    edited_csv = f"edited_{base_name}.csv"

    done_ids = _load_done_ids(edited_csv)

    # If edited file does not exist yet: write header
    file_exists = os.path.exists(edited_csv)
    out = open(edited_csv, "a", newline="", encoding="utf-8")
    writer = csv.writer(out)
    if not file_exists:
        writer.writerow(("id", "username", "url", "timestamp", "status"))  # status: keep/delete

    with open(source_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        rows = list(reader)

    open_rows = []
    for row in rows:
        try:
            row_id = int(row.get("id", ""))
        except Exception:
            continue
        if row_id in done_ids:
            continue
        open_rows.append((row_id, row))

    print(f"{APP_TITLE}\n")
    if not open_rows:
        print("Nothing left to review.")
        out.close()
        return edited_csv

    for pos, (row_id, row) in enumerate(open_rows, start=1):
        username = row.get("username", "")
        url = row.get("url", "")
        ts = row.get("timestamp", "")

        status = "keep"
        while True:
            _print_entry(pos, len(open_rows), row_id, username, url, ts, status)
            ans = input("> ").strip().lower()

            if ans == "":
                break

            if ans == "r":
                status = "delete" if status == "keep" else "keep"
                continue

            if ans in ("y", "yes", "j", "ja", "k", "keep"):
                status = "keep"
                break

            if ans in ("n", "no", "d", "delete", "del"):
                status = "delete"
                break

            if ans in ("q", "quit", "exit"):
                print("\nQuitting without losing progress.")
                out.close()
                return edited_csv

            print("Please use Enter, 'r', or 'q'.")

        # Write immediately + flush (so resume is safe)
        writer.writerow((row_id, username, url, ts, status))
        out.flush()
        done_ids.add(row_id)

    out.close()
    return edited_csv


if __name__ == "__main__":
    base = "followings"
    export_followings_to_csv(base)
    result = interactive_review_followings(base)
    print(f"\nDone. Output: {result}")
