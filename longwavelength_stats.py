"""Summarise long-wavelength X-ray PDB entries and the I23 share.

Reads wl_bl_id.csv (output of rcsbAPI.py) and prints, for each wavelength
cutoff, the total number of unique PDB entries collected at >= cutoff and
the number / percentage of those collected on Diamond's I23 beamline.
"""

import sys
import pandas as pd

CSV_PATH = "wl_bl_id.csv"
CUTOFFS = (2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)


def load(path: str) -> pd.DataFrame:
    cols = ["WAVELENGTH", "BEAMLINE", "PDBID"]
    # The cached CSV is headerless; a freshly harvested one has a header.
    # Sniff the first line and read accordingly.
    with open(path) as f:
        first = f.readline().strip()
    has_header = first.upper().startswith("WAVELENGTH")
    df = pd.read_csv(
        path,
        names=None if has_header else cols,
        header=0 if has_header else None,
    )
    df["WAVELENGTH"] = pd.to_numeric(df["WAVELENGTH"], errors="coerce")
    df["BEAMLINE"] = df["BEAMLINE"].astype(str).str.strip().str.upper()
    df["PDBID"] = df["PDBID"].astype(str).str.strip().str.upper()
    return df.dropna(subset=["WAVELENGTH"])


def main() -> None:
    df = load(CSV_PATH)

    unique_entries = df["PDBID"].nunique()
    print(f"X-ray PDB entries with wavelength metadata: {unique_entries}")
    print()

    for cutoff in CUTOFFS:
        long_wl = df[df["WAVELENGTH"] >= cutoff]
        total_pdbs = long_wl["PDBID"].nunique()
        i23_pdbs = long_wl.loc[long_wl["BEAMLINE"] == "I23", "PDBID"].nunique()
        pct = (i23_pdbs / total_pdbs * 100) if total_pdbs else 0.0
        print(
            f"  lambda >= {cutoff} A: {total_pdbs} PDB entries, "
            f"{i23_pdbs} on I23 ({pct:.1f}%)"
        )


if __name__ == "__main__":
    sys.exit(main())
