# GitHub Public Release Check & Distribution Policy

This document outlines the strict public release boundary for the **Font Intelligence Typography Decision System** on GitHub.

---

## 1. What May Be Publicly Committed

The public GitHub repository includes:
1. **Core Intelligence & Decision Engine**:
   - `catalog/` metadata files (`fonts.json`, `pairings.json`, `use-cases.json`, `scoring.json`, `anti-patterns.json`, `vocabularies.json`, `license-rules.json`).
   - `.agents/skills/font-intelligence/` canonical Agent Skill directory.
   - Python tools in `scripts/` (`recommend.py`, `score_pair.py`, `search_fonts.py`, `copy_fonts.py`, etc.).
   - Full test suites in `tests/` and `scripts/`.
2. **Platform Adapters & Documentation**:
   - Multi-agent adapters (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor `.cursorrules`, Windsurf, Cline, Copilot, Codex).
   - Platform & typography references in `references/`.
   - Compact offline fallback in `lite/font-intelligence-lite.md`.
3. **Public Font Assets (`assets/fonts/`)**:
   - Exactly **57 verified permissive open-source font families** (312 font files).
   - Every public font family is paired with its original open-source license (`OFL.txt`, `LICENSE.txt`, or CC0 dedication).
4. **Visual Specimen Studio**:
   - `preview/` directory (`index.html`, `style.css`, `app.js`, `fonts-data.js`).

---

## 2. What Must NOT Be Publicly Redistributed

1. **Restricted & Demo Cut Binaries**:
   - Families marked `RESTRICTED` in `catalog/fonts.json` (such as demo cuts `talero`, `garute`, `sweet-school`, `warriot`).
   - Must never be copied into `assets/fonts/`.
2. **Commercial Proof Needed / Marketplace Binaries**:
   - Families marked `CATALOG-ONLY` where commercial end-product use is allowed but file redistribution requires marketplace purchase proof (e.g. Creative Fabrica commercial cuts like `halo-dek`, `kastore`, `modestic-sans`).
   - Metadata is retained in `catalog/fonts.json` for AI styling recommendations, but raw binaries remain private/local.
3. **Unverified Provenance Binaries**:
   - Families marked `UNKNOWN` where foundry EULAs are ambiguous or lack redistribution grants.

---

## 3. Automated Release Verification Command

Run the following command before pushing to verify zero compliance breaches:
```bash
python -c "
import os, json
with open('catalog/fonts.json', encoding='utf-8') as f:
    cat = json.load(f)
public_ids = {f['id'] for f in cat['fonts'] if f.get('distribution_status') == 'public-asset'}
asset_ids = set(os.listdir('assets/fonts'))
violations = asset_ids - public_ids
if violations:
    print('FATAL: Found non-public fonts in assets/fonts:', violations)
    exit(1)
print(f'PASSED: All {len(asset_ids)} families in assets/fonts/ are verified permissive open source.')
"
```

---

## 4. Third-Party Intellectual Property Disclaimer

Third-party font binaries included in `assets/fonts/` are the property of their respective creators and foundries. Each typeface is governed by its specific open-source license (SIL OFL 1.1, Apache 2.0, MIT, Creative Commons Zero, or Ubuntu Font License). The root repository MIT license applies exclusively to the software code, typography algorithms, schemas, and documentation.
