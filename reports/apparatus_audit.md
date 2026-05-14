# Apparatus Propagation Audit

Run at: `2026-05-14T17:41:30Z`

This audit verifies that the deploy faithfully represents
the canonical archive's apparatus state. See
`APPARATUS_PROPAGATION_REPAIR_2026.md` for the constitutional rationale.

## Summary

- Canonical apparatus files: **1**
- Propagated correctly: **1**
- Propagation breaches: **0**
- Deploys with orphan `[*N]` markers (no canonical apparatus): **167**
- Canonical apparatus with anchor problems: **0**

## Propagated correctly

- `upanishads-muller-part2::muller-part2` — 42 apparatus entries, 1157 markers in passages

## Orphan markers (canonical apparatus not yet extracted)

Deploys whose passages carry `[*N]` markers verbatim from the raw witness
but whose canonical apparatus has not yet been recovered. These are not
propagation bugs; they are a long-term restoration backlog. The reader
surfaces an honest-gap diagnostic on click.

Total orphan markers across all deploys: **46630**.

| Deploy | Markers | Passages |
|---|---:|---:|
| `kojiki-chamberlain_chamberlain.json` | 2385 | 555 |
| `pagan-christs-robertson_robertson.json` | 2005 | 735 |
| `the-upanishads-max-muller-1879_anonymous.json` | 1582 | 1138 |
| `vishnu-purana_wilson.json` | 1574 | 694 |
| `thrice-greatest-hermes-vol1_mead.json` | 1501 | 1055 |
| `thrice-greatest-hermes-vol-1-grs-mead-1906_anonymous.json` | 1500 | 1054 |
| `lost-books-bible_platt.json` | 1427 | 990 |
| `vedic-hymns-part2_oldenberg.json` | 1426 | 793 |
| `mysticism-underhill_underhill.json` | 1420 | 635 |
| `history-of-utah-1540-1886-hubert-bancroft-1889_anonymous.json` | 1385 | 900 |
| `mishna-18-rabbinowicz_desola-raphall.json` | 1332 | 738 |
| `jaina-sutras-part2_jacobi.json` | 1259 | 974 |
| `thrice-greatest-hermes-vol2_mead.json` | 984 | 721 |
| `folklore-shakespeare-dyer_dyer.json` | 971 | 779 |
| `egypt-religious-development-petrie_petrie.json` | 911 | 419 |
| `religious-development-thought-in-ancient-egypt-james-breaste_anonymous.json` | 911 | 419 |
| `thrice-greatest-hermes-vol-3-grs-mead-1906_anonymous.json` | 795 | 555 |
| `thrice-greatest-hermes-vol3_mead.json` | 795 | 555 |
| `upanishads-muller-part1_muller-part1.json` | 746 | 592 |
| `evil-eye-elworthy_elworthy.json` | 696 | 517 |
| `jaina-sutras-part-2-hermann-jacobi-1884_anonymous.json` | 688 | 483 |
| `fairy-faith-evans-wentz_evans-wentz.json` | 684 | 436 |
| `vedic-hymns-part-1-max-muller-1891_anonymous.json` | 658 | 383 |
| `vedic-hymns-part1_muller-vedic.json` | 658 | 383 |
| `records-of-the-past-2nd-series-vol-ii-ah-sayce-1888_anonymous.json` | 584 | 363 |
| `records-past-vol2_sayce.json` | 584 | 363 |
| `myths-babylonia-mackenzie_mackenzie.json` | 570 | 463 |
| `tibetan-tantra-muses_muses.json` | 511 | 458 |
| `lloyd-creed-half-japan_lloyd.json` | 505 | 386 |
| `migration-symbols-d-alviella_d-alviella.json` | 490 | 358 |
| `interior-castle-teresa_peers.json` | 456 | 340 |
| `oracles-of-nostradamus-charles-ward-1891_anonymous.json` | 456 | 184 |
| `evolution-dragon-smith_smith.json` | 445 | 358 |
| `mesnavi-acts-adepts-redhouse_redhouse-acts.json` | 434 | 296 |
| `the-mesnavi-the-acts-of-the-adepts-james-redhouse-1881_anonymous.json` | 434 | 296 |
| `records-past-vol3_sayce.json` | 430 | 206 |
| `wisdom-talmud-bokser_bokser.json` | 414 | 401 |
| `the-jataka-vol-4-whd-rouse-1901_anonymous.json` | 412 | 336 |
| `jesus-essene-hartmann_hartmann.json` | 392 | 230 |
| `the-jataka-vol-2-whd-rouse-1895_anonymous.json` | 391 | 374 |
| _… and 127 more_ |  |  |

