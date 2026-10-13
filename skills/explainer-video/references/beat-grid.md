# Beat Grid

Cuts land on downbeats, UI hits land on beats, zero dead time. The grid comes from the actual music file, not its nominal BPM.

## Bed selection
- CC-licensed with a **clear, steady pulse**, ~100-150 BPM (Wikimedia Commons API: `https://commons.wikimedia.org/w/api.php`). Keep the attribution for the outro.
- Reject ambient/droning beds: they have no grid to cut on (the helper will tell you).

## Analysis
```bash
python3 bin/beat_grid.py BED_FILE --duration 61 -o grid.json
```
Output: `bpm`, `beat_period_s`, `offset_s`, `beats[]`, `grid_energy_ratio`.

- `grid_energy_ratio >= 1.5` → usable grid. Below that → **pick another bed**, do not force it.
- Method: high-frequency-content spectral flux (numpy) → phase-fold into candidate periods. Percussive beds score > 2.0; ambient beds score ~1.0-1.4.
- Lock scene boundaries to downbeats (every N beats, e.g. 8-beat grid lines) and place every event (card pop, badge, stamp, cut) on a beat from `beats[]`.

## Timing the narration
Lay narration segments against the grid: a segment may start slightly off-grid, but scene boundaries and visual hits must sit on beats. If a narration line overruns its scene, trim the copy — never stretch the grid.
