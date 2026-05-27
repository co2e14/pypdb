![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg) <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/co2e14/pypdb"> <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/co2e14/pypdb">

# pypdb

A collection of Python scripts for mining the [Protein Data Bank](https://www.rcsb.org/) for X-ray crystallography experimental metadata and producing summary plots. The focus is on **long-wavelength macromolecular crystallography** (in particular the Diamond Light Source **I23** beamline) and on assessing the feasibility of native sulphur SAD (**S-SAD**) phasing across the PDB.

The scripts query the RCSB / PDBe APIs (via [`pypdb`](https://pypi.org/project/pypdb/), [`rcsbsearchapi`](https://pypi.org/project/rcsbsearchapi/), and direct REST calls), extract per-entry fields such as diffraction wavelength, synchrotron beamline, unit-cell dimensions, number of unique reflections and sequence-derived sulphur content, then save the results as CSV files and plot histograms with `matplotlib` / `seaborn`.

## What's in here

### PDB harvesting

| Script | Purpose |
| --- | --- |
| [rcsbAPI.py](rcsbAPI.py) | Queries all X-ray entries via `rcsbsearchapi`, pulls wavelength / beamline per entry from the RCSB REST API, and writes `wl_bl_id.csv`. |
| [longWavelengthExperiments.py](longWavelengthExperiments.py) / [longWavelengthExperimentsV2.py](longWavelengthExperimentsV2.py) | Earlier `pypdb`-based and PDBe Solr-based harvesters of wavelength / beamline metadata. V2 uses the EBI PDBe `select` endpoint. |
| [pdb_wavelength_list.py](pdb_wavelength_list.py) | Multiprocessed wavelength extraction for X-ray, I23-only and neutron-diffraction subsets. |
| [longWavelengthPDBIDs.py](longWavelengthPDBIDs.py) / [longwavelength_pdbids.py](longwavelength_pdbids.py) | Filter PDB IDs to long-wavelength synchrotron entries (excluding I23 and neutron) above a wavelength threshold. |
| [entries.py](entries.py) / [query.py](query.py) | Helper Solr queries against the PDBe API. |
| [unitcell.py](unitcell.py) / [unitcell_threaded.py](unitcell_threaded.py) | Pull the longest unit-cell axis for every X-ray entry. |
| [S_content.py](S_content.py) | Compute the percentage of sulphur-containing residues (Cys + Met) from each entry's FASTA sequence. |
| [S_content_UNIPROTKB.py](S_content_UNIPROTKB.py) | Bulk-download eukaryote / archaea / bacteria FASTA sequences from UniProtKB. |
| [reflection_scatterer_ratio.py](reflection_scatterer_ratio.py) | Compute `num_miller_indices / sulphur_count` per entry — the reflections-per-scatterer ratio used as a proxy for S-SAD solvability. |

### Post-processing & plotting

| Script | Purpose |
| --- | --- |
| [convertcsv.py](convertcsv.py) | Parse the raw harvester output (tuple-formatted lines) into a clean `WAVELENGTH, BEAMLINE, PDBID` table. |
| [removeI23Duplicates.py](removeI23Duplicates.py) | Deduplicate I23 entries from the combined wavelength list. |
| [pdb_wavelength_hist.py](pdb_wavelength_hist.py) | Stacked log-histogram of all PDB wavelengths with I23 entries highlighted. |
| [ratio_hist.py](ratio_hist.py) | Histogram of reflections-per-scatterer ratio (XKCD-styled) with the proposed S-SAD-feasible threshold drawn at 1000. |
| [XKCDhistogram.py](XKCDhistogram.py) | KDE plot of the reflections-per-scatterer ratio across all X-ray PDB structures. |

### Data files

The repository ships with the cached CSV / TXT outputs of previous runs (e.g. `wl_bl_id*.csv`, `wavelengthlistvalues*.csv`, `longcellvalues.csv`, `refScatRatio*.csv`, `pdb_lambda_beamline.txt`) plus the rendered plots (`out.png`, `refscatrat.png`, `refperscat_xkcd.png`) so the figures can be reproduced without re-querying the PDB.

## Requirements

- Python 3
- `pypdb`, `rcsbsearchapi`, `solrq`, `requests`
- `pandas`, `numpy`, `tqdm`
- `matplotlib`, `seaborn`

## Usage

Each script is standalone and run directly, e.g.:

```bash
python rcsbAPI.py              # harvest wavelength + beamline for all X-ray entries
python reflection_scatterer_ratio.py
python pdb_wavelength_hist.py  # plot histogram from the cached CSV
```

The harvesters use `multiprocessing.Pool` over `os.cpu_count()` and can take several hours against the full PDB — the included CSVs let you skip straight to the plotting scripts.

## License

See [LICENSE](LICENSE).
