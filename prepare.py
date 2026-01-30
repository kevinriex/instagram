import argparse
import os
import shutil
import zipfile

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "data")

DEFAULT_REL_PATH = os.path.join(
    "connections", "followers_and_following", "following.json"
)

def extract_zip(zip_path: str, outdir: str) -> str:
    os.makedirs(outdir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(outdir)
    return outdir

def find_following_json(root: str) -> str:
    """
    Sucht nach der Datei connections/followers_and_following/following.json
    innerhalb des entpackten Ordners. Manche Exporte haben noch einen
    Top-Level-Ordner (z.B. instagram-username/...), daher wird rekursiv gesucht.
    """
    # 1) Direkt versuchen (falls root genau der Export-Root ist)
    direct = os.path.join(root, DEFAULT_REL_PATH)
    if os.path.exists(direct):
        return direct

    # 2) Rekursiv suchen
    for dirpath, _, filenames in os.walk(root):
        if "following.json" in filenames:
            candidate = os.path.join(dirpath, "following.json")
            # Pfad-Ende prüfen, damit wir nicht irgendeine andere following.json erwischen
            normalized = os.path.normpath(candidate)
            if normalized.endswith(os.path.normpath(DEFAULT_REL_PATH)):
                return candidate

    raise FileNotFoundError(
        f"Konnte '{DEFAULT_REL_PATH}' im entpackten Export nicht finden."
    )

def main():
    ap = argparse.ArgumentParser(
        description="Extracts an Instagram export ZIP and copies out following.json."
    )
    ap.add_argument("zipfile", help="Pfad zur Instagram Export ZIP")
    ap.add_argument(
        "--outdir",
        default=os.path.join("data", "export"),
        help="Extraction directory (default: data/export)",
    )
    ap.add_argument(
        "--dest",
        default=os.path.join("data", "followings.json"),
        help="Destination path for the copied following.json (default: data/followings.json)",
    )

    args = ap.parse_args()

    if not os.path.exists(args.zipfile):
        raise FileNotFoundError(f"ZIP not found: {args.zipfile}")

    os.makedirs(DATA_DIR, exist_ok=True)

    extract_zip(args.zipfile, args.outdir)
    src = find_following_json(args.outdir)

    os.makedirs(os.path.dirname(args.dest) or ".", exist_ok=True)
    shutil.copy2(src, args.dest)

    print(f"OK: Extracted to: {args.outdir}")
    print(f"OK: Copied: {src} -> {args.dest}")

if __name__ == "__main__":
    main()
