"""Non-destructive merge for the CSV rebuild scripts.

Why this exists: the rebuild scripts used to overwrite their CSVs wholesale from
the OWID snapshots. Anything curated by hand or appended from a later CDC pull —
diphtheria deaths 1900-1936, the NNDSS recent-year rows, partial-year rows, the
measles 2025 final count — was silently destroyed on the next run.

The rule now: a rebuild may only ADD. An existing non-empty cell is never
overwritten by a source value; divergences are reported so nothing hides. To let
a source value win, blank the cell (or delete the row) first.
"""
import csv
import os

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def load_existing(name, key="year"):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return [], {}
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return rows, {int(r[key]): r for r in rows}


def merge_rows(name, header, source_rows, key="year"):
    """source_rows: list of dicts. Returns merged list of dicts, sorted by year.

    Existing values win over source values; empty existing cells are filled from
    the source; years only in the source are appended.
    """
    _, existing = load_existing(name, key)
    merged = {y: dict(r) for y, r in existing.items()}
    kept, filled, added = [], 0, 0
    for src in source_rows:
        y = int(src[key])
        cur = merged.get(y)
        if cur is None:
            merged[y] = {h: str(src.get(h, "") or "") for h in header}
            added += 1
            continue
        for h in header:
            if h == key:
                continue
            new = str(src.get(h, "") or "").strip()
            old = (cur.get(h) or "").strip()
            if not new:
                continue
            if not old:
                cur[h] = new
                filled += 1
            elif old != new:
                kept.append((y, h, old, new))
    out = [merged[y] for y in sorted(merged)]
    print(f"  {name}: {len(out)} rows | +{added} new years, {filled} empty cells filled, "
          f"{len(kept)} curated values kept over source")
    for y, h, old, new in kept[:12]:
        print(f"    kept {name} {y}.{h} = {old!r} (source said {new!r})")
    if len(kept) > 12:
        print(f"    ... and {len(kept) - 12} more")
    return out


def write_rows(name, header, rows, key="year"):
    path = os.path.join(DATA, name)
    with open(path, "w", newline="") as f:
        # LF everywhere (see .gitattributes) — csv's default CRLF once left stray
        # CR bytes in otherwise-LF files, which shows up as whole-file churn.
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote data/{name} ({rows[0][key]}-{rows[-1][key]})")


def merge_and_write(name, header, source_rows, key="year"):
    write_rows(name, header, merge_rows(name, header, source_rows, key), key)
