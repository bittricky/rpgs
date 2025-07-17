import os
import time
import pandas as pd
import requests
from tqdm import tqdm

API_KEY = os.getenv("RAWG_KEY")  # set env var RAWG_KEY=your_key
if not API_KEY:
    raise SystemExit("[!] Set your RAWG_KEY environment variable first.")

SOURCE_CSV = "rpgs.csv"
DEST_CSV = "rpgs.csv"

def get_release_year(title: str) -> str:
    """Return the release year for *title* using RAWG search."""
    url = "https://api.rawg.io/api/games"
    params = {"search": title, "page_size": 1, "key": API_KEY}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    results = r.json().get("results", [])
    if results and results[0].get("released"):
        return results[0]["released"][:4]  # YYYY-MM-DD → YYYY
    return ""  # couldn't find it

def main():
    df = pd.read_csv(SOURCE_CSV)
    if "release year" not in df.columns:
        df.insert(len(df.columns), "release year", "")
    for idx, title in tqdm(enumerate(df["title"]), total=len(df)):
        if not df.at[idx, "release year"]:
            try:
                df.at[idx, "release year"] = get_release_year(title)
            except Exception as e:
                print(f"[warn] {title}: {e}")
            time.sleep(3)
    df.to_csv(DEST_CSV, index=False)
    print(f"[✓] Saved updated CSV → {DEST_CSV}")

if __name__ == "__main__":
    main()
