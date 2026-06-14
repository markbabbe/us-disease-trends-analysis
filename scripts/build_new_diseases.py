#!/usr/bin/env python3
"""Build diphtheria/mumps/rubella CSVs from the saved OWID raw files.

Source: Our World in Data U.S. series (underlying: U.S. Public Health Reports +
CDC). Raw files: data/owid_diphtheria.csv, owid_mumps.csv, owid_rubella.csv.
Output: data/diphtheria.csv, data/mumps.csv, data/rubella.csv
(Tetanus and Hep B are hand-built from CDC MMWR — see those CSVs.)
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def read(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def write(name, rows):
    with open(os.path.join(DATA, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "cases", "deaths", "notes"])
        w.writerows(rows)
    print(f"wrote data/{name}: {len(rows)} rows ({rows[0][0]}-{rows[-1][0]})")


def col(r, key):
    v = (r.get(key) or "").strip()
    return v if v else ""


def main():
    # Diphtheria — cases + deaths, 1937-2022 (pre-1937 not in OWID; note it)
    out = []
    for r in read("owid_diphtheria.csv"):
        y = int(r["Year"])
        note = "Toxoid (1920s); into DTP ~1948" if y == 1937 else ""
        out.append([y, col(r, "Diphtheria cases"), col(r, "Diphtheria deaths"), note])
    out[0][3] = "OWID series starts 1937; pre-1937 had >100k cases/yr in the 1920s"
    write("diphtheria.csv", out)

    # Mumps — cases + deaths; cases reportable from 1968, vaccine 1967
    out = []
    for r in read("owid_mumps.csv"):
        y = int(r["Year"])
        note = ""
        if y == 1967:
            note = "Mumps vaccine licensed"
        elif y == 1968:
            note = "Nationally notifiable; into MMR 1971"
        out.append([y, col(r, "Mumps cases"), col(r, "Mumps deaths"), note])
    write("mumps.csv", out)

    # Rubella — cases only (deaths minimal; harm is congenital rubella syndrome)
    out = []
    for r in read("owid_rubella.csv"):
        y = int(r["Year"])
        note = ""
        if y == 1966:
            note = "Notifiable from 1966; main harm is CRS, not deaths"
        elif y == 1969:
            note = "Rubella vaccine licensed; into MMR 1971"
        out.append([y, col(r, "Rubella cases"), "", note])
    write("rubella.csv", out)


if __name__ == "__main__":
    main()
