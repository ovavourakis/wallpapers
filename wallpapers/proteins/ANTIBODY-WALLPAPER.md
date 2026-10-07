# Antibody wallpaper

Branch: `antibody-sabdab2`.

Run `./run-antibody-wallpaper.sh` in this folder and leave it running. Plash can open the local `index.html` file or use http://127.0.0.1:8766/index.html. The Python 3 server listens only on this Mac and relays SAbDab2 requests, whose public API lacks browser CORS permissions.

Hover the small rhombus at bottom right to reveal controls. Keyboard focus also reveals them. The rhombus rotates into a square. The open menu has its own softly feathered light/dark veil.

- Source: **PROTEINS / ANTIBODIES**, drawing from SAbDab2 or PDB.
- Display: **DYNAMIC / STATIC**, also available with S / D. Fresh page loads start in antibodies, static, dark and auto-reload modes, with highlights enabled.
- Appearance: **LIGHT / DARK**, also available with M. Initially dark; subsequent London 06:00/18:00 boundaries update the appearance.
- **RELOAD NOW** selects a new random structure from the current source.
- **FIXED / AUTO-RELOAD**: automatic mode selects a new entry every five minutes; fixed mode pauses that timer indefinitely. Manual reload and entry selection still work. Fresh page loads restore automatic refresh.
- The loupe beside the entry ID opens a field accepting `1A14`, `pdb_00001a14`, or a search phrase (up to 200 characters). IDs load directly. Antibody searches first use SAbDab antigen names, then antibody-chain names, organism/gene metadata, structure titles, keywords and publication references. Abstracts are not exposed by SAbDab. Fallback metadata pages are cached in memory for one hour. Protein searches use the RCSB full-text API and load its first relevance-ranked experimental entry. Press Enter to load the first match from the current source. Manual entries bypass random-selection filters. The ID links to its SAbDab2 or RCSB page.

Antibody entries always reserve the lightest grey for heavy chains and the darkest grey for light chains. Other chains use intermediate shades. **ENABLE HIGHLIGHTS** in antibody mode colours annotated CDR1–3 red. The same control in protein mode colours non-polymer and branched molecular entities red while protein, peptide, DNA and RNA regions retain greys. Ligand classification uses mmCIF entity descriptors; antibody highlighting covers only CDRs. Water remains hidden. Clicking a chain in dynamic mode toggles a red user highlight.

Highlight changes recolour the existing dynamic viewer without resetting its camera or rotation. Static mode swaps matching in-memory images captured at identical pose and 300% zoom. Snapshot preparation is hidden; a previous-frame cover fades into the finished new view. Structure replacement and static/dynamic changes run within the page, preserving its light/dark choice and clock. Static/dynamic changes keep the same entry and reload deadline. Random snapshot variants are never saved to disk or long-term browser storage.

Random SAbDab2 selection samples accepted PDB entries, not antibody instances, and downloads `full_structure: true` from the `_sabdab.cif` endpoint. A qualifying entry must have an annotated antibody binding to a PROTEIN antigen, at least one protein chain longer than 30 residues, no nucleic-acid chains, and at most 20 protein chains. Protein-source random selection uses the corresponding length/nucleic-acid/chain filters. Antibody colours and CDRs use author chain and residue IDs from the unmodified file.

Offline: antibody mode uses bundled **1IGT** coordinates and annotations (an exception to the random antigen filter). Protein mode retains the **1PMA** proteasome and the two permanent axial PNG backups. Mol* assets and both coordinate fallbacks are local.

API specification: https://sabdab.opig.stats.ox.ac.uk/api/openapi.json
