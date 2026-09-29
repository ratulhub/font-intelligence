/**
 * Font Intelligence Specimen & Visual Inspection System
 * Dynamic Catalog Rendering, Real-Time Filtering, and Visual Inspection Engine
 */

(function () {
  'use strict';

  // State Management
  const state = {
    fonts: [],
    filteredFonts: [],
    activeFont: null,
    searchQuery: '',
    selectedCategory: '',
    selectedStyle: '',
    selectedScript: '',
    selectedRole: '',
    selectedLicense: '',
    variableOnly: false,
    minReadability: 1,
    previewText: 'Sphinx of black quartz, judge my vow.',
    fontSize: 28,
    viewMode: 'grid' // 'grid' | 'stream'
  };

  // DOM Elements
  const elements = {
    fontGrid: document.getElementById('font-grid'),
    emptyState: document.getElementById('empty-state'),
    searchInput: document.getElementById('search-input'),
    filterCategory: document.getElementById('filter-category'),
    filterStyle: document.getElementById('filter-style'),
    filterScript: document.getElementById('filter-script'),
    filterRole: document.getElementById('filter-role'),
    filterLicense: document.getElementById('filter-license'),
    filterVariable: document.getElementById('filter-variable'),
    filterReadability: document.getElementById('filter-readability'),
    readabilityVal: document.getElementById('readability-val'),
    customTextInput: document.getElementById('custom-text-input'),
    fontSizeSlider: document.getElementById('font-size-slider'),
    fontSizeVal: document.getElementById('font-size-val'),
    presetPills: document.querySelectorAll('.preset-pill'),
    viewGridBtn: document.getElementById('view-grid'),
    viewStreamBtn: document.getElementById('view-stream'),
    resultsCount: document.getElementById('results-count'),
    activeChips: document.getElementById('active-filters-chips'),
    btnResetFilters: document.getElementById('btn-reset-filters'),
    btnClearEmpty: document.getElementById('btn-clear-empty'),
    dynamicStyle: document.getElementById('dynamic-font-faces'),
    
    // Stats
    statTotal: document.getElementById('stat-total-fonts'),
    statOpenSource: document.getElementById('stat-open-source'),
    statVariable: document.getElementById('stat-variable-fonts'),
    statFiles: document.getElementById('stat-total-files'),

    // Modal
    modal: document.getElementById('inspector-modal'),
    modalCloseBtn: document.getElementById('modal-close-btn'),
    modalFontName: document.getElementById('modal-font-name'),
    modalFontCat: document.getElementById('modal-font-category'),
    modalFontId: document.getElementById('modal-font-id'),
    modalTabs: document.querySelectorAll('.modal-tab'),
    tabPanes: document.querySelectorAll('.tab-pane'),
    waterfallList: document.getElementById('modal-waterfall-list'),
    glyphsLetters: document.getElementById('modal-glyphs-letters'),
    glyphsNumbers: document.getElementById('modal-glyphs-numbers'),
    glyphsSymbols: document.getElementById('modal-glyphs-symbols'),
    licensingContent: document.getElementById('modal-licensing-content'),
    codeCss: document.getElementById('modal-code-css'),
    codeFlutter: document.getElementById('modal-code-flutter'),
    btnCopyCss: document.getElementById('btn-copy-css'),
    btnCopyFlutter: document.getElementById('btn-copy-flutter'),
    toast: document.getElementById('toast'),
    toastMsg: document.getElementById('toast-message')
  };

  /**
   * Initialize Catalog Application
   */
  async function init() {
    setupEventListeners();
    await loadCatalogData();
    injectFontFaces();
    updateMetrics();
    applyFilters();
  }

  /**
   * Load Catalog Data (Supports offline window.CATALOG_DATA and HTTP fetch)
   */
  async function loadCatalogData() {
    if (window.CATALOG_DATA && window.CATALOG_DATA.fonts) {
      state.fonts = window.CATALOG_DATA.fonts;
      return;
    }

    try {
      const response = await fetch('../catalog/fonts.json');
      if (!response.ok) throw new Error(`HTTP error ${response.status}`);
      const data = await response.json();
      state.fonts = data.fonts || [];
    } catch (err) {
      console.warn('Could not fetch ../catalog/fonts.json. Checking fallback window.CATALOG_DATA...', err);
      if (window.CATALOG_DATA && window.CATALOG_DATA.fonts) {
        state.fonts = window.CATALOG_DATA.fonts;
      } else {
        elements.fontGrid.innerHTML = `
          <div class="empty-state">
            <h3>Unable to load font catalog</h3>
            <p>Please run preview via an HTTP server or ensure preview/fonts-data.js is present.</p>
          </div>
        `;
      }
    }
  }

  /**
   * Dynamically Inject @font-face Rules
   */
  function injectFontFaces() {
    let rules = '';
    for (const font of state.fonts) {
      const files = font.files || [];
      // Prefer woff2, then ttf, then otf
      const best = files.find(f => f.format === 'woff2') ||
                   files.find(f => f.format === 'ttf') ||
                   files[0];
      if (best) {
        const url = `../${best.path}`;
        const fmt = best.format === 'woff2' ? 'woff2' : (best.format === 'otf' ? 'opentype' : 'truetype');
        rules += `
          @font-face {
            font-family: '${font.id}-preview';
            src: url('${encodeURI(url)}') format('${fmt}');
            font-display: swap;
          }
        `;
      }
    }
    elements.dynamicStyle.innerHTML = rules;
  }

  /**
   * Update Header Metric Counters
   */
  function updateMetrics() {
    if (!state.fonts.length) return;
    elements.statTotal.textContent = state.fonts.length;
    const verifiedOS = state.fonts.filter(f => f.license?.tracking?.verification_status === 'verified').length;
    elements.statOpenSource.textContent = verifiedOS;
    const variableCount = state.fonts.filter(f => f.technical?.variable).length;
    elements.statVariable.textContent = variableCount;
    const totalFiles = state.fonts.reduce((acc, f) => acc + (f.files ? f.files.length : 0), 0);
    elements.statFiles.textContent = totalFiles;
  }

  /**
   * Filter & Search Evaluation
   */
  function applyFilters() {
    const q = state.searchQuery.toLowerCase().trim();
    const cat = state.selectedCategory.toLowerCase();
    const st = state.selectedStyle.toLowerCase();
    const sc = state.selectedScript.toLowerCase();
    const ro = state.selectedRole.toLowerCase();
    const lic = state.selectedLicense.toLowerCase();

    state.filteredFonts = state.fonts.filter(f => {
      const cur = f.curated || {};
      const tech = f.technical || {};
      const licInfo = f.license || {};
      const track = licInfo.tracking || {};

      // Free-text query
      if (q) {
        const textCorpus = `${f.id} ${f.name} ${cur.category} ${(cur.styles || []).join(' ')} ${(cur.roles || []).join(' ')} ${cur.notes || ''}`.toLowerCase();
        if (!textCorpus.includes(q)) return false;
      }

      // Category
      if (cat && cur.category?.toLowerCase() !== cat) return false;

      // Style
      if (st && !(cur.styles || []).some(s => s.toLowerCase() === st)) return false;

      // Script
      if (sc) {
        const scripts = [...(tech.scripts || []), ...(tech.unicode_blocks || [])].map(s => s.toLowerCase());
        if (!scripts.some(s => s.includes(sc))) return false;
      }

      // Role
      if (ro && !(cur.roles || []).some(r => r.toLowerCase() === ro)) return false;

      // License status
      if (lic && track.verification_status?.toLowerCase() !== lic) return false;

      // Variable
      if (state.variableOnly && !tech.variable) return false;

      // Readability threshold
      if (state.minReadability > 1) {
        const read = cur.readability || {};
        const maxScore = Math.max(read.body || 0, read.ui || 0, read.long_form || 0);
        if (maxScore < state.minReadability) return false;
      }

      return true;
    });

    renderGrid();
    renderActiveFilterChips();
  }

  /**
   * Render Filter Chips
   */
  function renderActiveFilterChips() {
    const chips = [];
    if (state.selectedCategory) chips.push({ label: `Category: ${state.selectedCategory}`, clear: () => { state.selectedCategory = ''; elements.filterCategory.value = ''; } });
    if (state.selectedStyle) chips.push({ label: `Style: ${state.selectedStyle}`, clear: () => { state.selectedStyle = ''; elements.filterStyle.value = ''; } });
    if (state.selectedScript) chips.push({ label: `Script: ${state.selectedScript}`, clear: () => { state.selectedScript = ''; elements.filterScript.value = ''; } });
    if (state.selectedRole) chips.push({ label: `Role: ${state.selectedRole}`, clear: () => { state.selectedRole = ''; elements.filterRole.value = ''; } });
    if (state.selectedLicense) chips.push({ label: `Status: ${state.selectedLicense}`, clear: () => { state.selectedLicense = ''; elements.filterLicense.value = ''; } });
    if (state.variableOnly) chips.push({ label: 'Variable Only', clear: () => { state.variableOnly = false; elements.filterVariable.checked = false; } });
    if (state.minReadability > 1) chips.push({ label: `Min Readability: ≥${state.minReadability}`, clear: () => { state.minReadability = 1; elements.filterReadability.value = 1; elements.readabilityVal.textContent = '≥ 1/10'; } });

    elements.activeChips.innerHTML = chips.map((c, i) => `
      <span class="filter-chip" data-idx="${i}">
        ${c.label} ×
      </span>
    `).join('');

    elements.activeChips.querySelectorAll('.filter-chip').forEach(el => {
      el.addEventListener('click', () => {
        const idx = parseInt(el.getAttribute('data-idx'), 10);
        chips[idx].clear();
        applyFilters();
      });
    });

    elements.resultsCount.textContent = `Showing ${state.filteredFonts.length} of ${state.fonts.length} font families`;
  }

  /**
   * Render Specimen Grid Cards
   */
  function renderGrid() {
    if (!state.filteredFonts.length) {
      elements.fontGrid.innerHTML = '';
      elements.emptyState.classList.remove('hidden');
      return;
    }

    elements.emptyState.classList.add('hidden');
    
    const html = state.filteredFonts.map(font => {
      const cur = font.curated || {};
      const tech = font.technical || {};
      const lic = font.license || {};
      const track = lic.tracking || {};
      const read = cur.readability || {};

      // Status badge styling
      const status = track.verification_status || 'unknown';
      let statusClass = 'tag-review';
      let statusLabel = 'Needs Review';
      if (status === 'verified') { statusClass = 'tag-verified'; statusLabel = 'Verified Open Source'; }
      else if (status === 'restricted') { statusClass = 'tag-restricted'; statusLabel = 'Restricted / Demo'; }

      // Weight chips
      const weights = tech.weights || [400];
      const weightBadges = weights.slice(0, 7).map(w => `<span class="weight-chip">${w}</span>`).join('');
      const moreWeights = weights.length > 7 ? `<span class="weight-chip">+${weights.length - 7}</span>` : '';

      // Bangla support check
      const scripts = [...(tech.scripts || []), ...(tech.unicode_blocks || [])].map(s => s.toLowerCase());
      const hasBangla = scripts.some(s => s.includes('bangla') || s.includes('bengali'));

      // Readability tier badges
      const getMeterClass = v => v >= 8 ? 'read-high' : (v >= 6 ? 'read-med' : 'read-low');

      // Fallback family stack
      const fallbackStack = (cur.fallback || ['sans-serif']).join(', ');

      return `
        <article class="font-card" data-id="${font.id}">
          <header class="card-header">
            <div class="card-title-group">
              <h2>${font.name}</h2>
              <span class="card-subtype">${cur.subtype || 'Typography Family'}</span>
            </div>
            <div class="card-badges">
              <span class="tag-pill tag-category">${cur.category || 'sans-serif'}</span>
              <span class="tag-pill ${statusClass}" title="${track.redistribution_notes || ''}">${statusLabel}</span>
              ${tech.variable ? '<span class="tag-pill tag-variable">Variable</span>' : ''}
            </div>
          </header>

          <div class="card-weights">
            ${weightBadges}
            ${moreWeights}
            ${tech.italic ? '<span class="weight-chip is-var">Italic</span>' : ''}
          </div>

          <div class="card-readability">
            <div class="read-meter" title="Continuous long-form reading comfort">
              <span class="read-lbl">Body</span>
              <span class="read-val ${getMeterClass(read.body || 0)}">${read.body || '-'}/10</span>
            </div>
            <div class="read-meter" title="Interface microcopy & button clarity">
              <span class="read-lbl">UI</span>
              <span class="read-val ${getMeterClass(read.ui || 0)}">${read.ui || '-'}/10</span>
            </div>
            <div class="read-meter" title="Tabular figures & numeral clarity">
              <span class="read-lbl">Num</span>
              <span class="read-val ${getMeterClass(read.numbers || 0)}">${read.numbers || '-'}/10</span>
            </div>
          </div>

          <!-- Live Editable English Specimen -->
          <div class="specimen-canvas">
            <div class="specimen-text" style="font-family: '${font.id}-preview', ${fallbackStack}; font-size: ${state.fontSize}px; font-weight: ${weights[0] || 400};">
              ${escapeHtml(state.previewText)}
            </div>
          </div>

          <!-- Secondary Samples: Numbers & Mini UI -->
          <div class="samples-row">
            <div class="sample-box">
              <span class="sample-label">Numerals & Currency</span>
              <div class="sample-content" style="font-family: '${font.id}-preview', ${fallbackStack};">
                0123456789 $1,284.50 €98
              </div>
            </div>
            <div class="sample-box">
              <span class="sample-label">UI Interface Preview</span>
              <div class="ui-preview-box">
                <button class="mini-btn" style="font-family: '${font.id}-preview', ${fallbackStack};">Button CTA</button>
                <span class="mini-badge" style="font-family: '${font.id}-preview', ${fallbackStack};">PRO PLAN</span>
              </div>
            </div>
          </div>

          <!-- Bangla Sample (Strict verification audit) -->
          <div class="bangla-box">
            <span class="sample-label">Bangla Script Support</span>
            ${hasBangla ? `
              <div class="bangla-supported" style="font-family: '${font.id}-preview', ${fallbackStack};">
                আমাদের সুন্দর বাংলা বর্ণমালা এবং সংখ্যা ১২৩৪৫৬৭৮৯০
              </div>
            ` : `
              <div class="bangla-unsupported">
                <span>Not in Latin binary (Tofu risk)</span>
                <span class="tofu-badge">Pair: Hind Siliguri</span>
              </div>
            `}
          </div>

          <footer class="card-footer">
            <div class="footer-meta">
              <span>${tech.scripts ? tech.scripts.slice(0, 3).join(', ') : 'Latin'}</span>
              • <span>${tech.embedding_permission?.includes('Installable') ? 'Installable TTF' : 'Permissive'}</span>
            </div>
            <div class="card-actions">
              <button class="btn btn-sm btn-outline btn-inspect" data-id="${font.id}">Inspect</button>
              <button class="btn btn-sm btn-secondary btn-copy" data-id="${font.id}">Copy CSS</button>
            </div>
          </footer>
        </article>
      `;
    }).join('');

    elements.fontGrid.innerHTML = html;

    // Attach card action listeners
    elements.fontGrid.querySelectorAll('.btn-inspect').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        openInspector(btn.getAttribute('data-id'));
      });
    });

    elements.fontGrid.querySelectorAll('.btn-copy').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const fid = btn.getAttribute('data-id');
        const font = state.fonts.find(f => f.id === fid);
        if (font) copyFontCss(font);
      });
    });

    elements.fontGrid.querySelectorAll('.font-card').forEach(card => {
      card.addEventListener('click', () => {
        openInspector(card.getAttribute('data-id'));
      });
    });
  }

  /**
   * Inspector Modal
   */
  function openInspector(fontId) {
    const font = state.fonts.find(f => f.id === fontId);
    if (!font) return;
    state.activeFont = font;

    const cur = font.curated || {};
    const tech = font.technical || {};
    const lic = font.license || {};
    const track = lic.tracking || {};
    const fallbackStack = (cur.fallback || ['sans-serif']).join(', ');

    elements.modalFontName.textContent = font.name;
    elements.modalFontCat.textContent = cur.category || 'sans-serif';
    elements.modalFontId.textContent = font.id;

    // 1. Waterfall
    const weights = tech.weights || [400];
    const waterfallHtml = weights.map(w => `
      <div class="waterfall-item">
        <div class="waterfall-meta">Weight ${w} — Size 24px</div>
        <div class="waterfall-specimen" style="font-family: '${font.id}-preview', ${fallbackStack}; font-weight: ${w};">
          ${escapeHtml(state.previewText)}
        </div>
      </div>
    `).join('');
    elements.waterfallList.innerHTML = waterfallHtml;

    // 2. Glyphs
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    elements.glyphsLetters.innerHTML = letters.split('').map(char => `
      <div class="glyph-cell" style="font-family: '${font.id}-preview', ${fallbackStack};">${char}</div>
    `).join('');

    const nums = '0123456789+-=/%$€£¥₹';
    elements.glyphsNumbers.innerHTML = nums.split('').map(char => `
      <div class="glyph-cell" style="font-family: '${font.id}-preview', ${fallbackStack};">${char}</div>
    `).join('');

    const symbols = '!@#^&*()_[]{}|;:,.<>?~`"\'\\';
    elements.glyphsSymbols.innerHTML = symbols.split('').map(char => `
      <div class="glyph-cell" style="font-family: '${font.id}-preview', ${fallbackStack};">${char}</div>
    `).join('');

    // 3. Licensing Details
    elements.licensingContent.innerHTML = `
      <div class="lic-card">
        <span class="lic-key">License Name:</span>
        <span class="lic-val"><strong>${track.license_name || lic.type}</strong></span>
        <span class="lic-key">SPDX Identifier:</span>
        <span class="lic-val"><code>${track.spdx_id || 'N/A'}</code></span>
        <span class="lic-key">Commercial Use:</span>
        <span class="lic-val">${track.commercial_use ? '✓ Allowed for commercial designs & web applications' : '✗ Personal / Demo only (Commercial purchase required)'}</span>
        <span class="lic-key">Redistribution:</span>
        <span class="lic-val">${track.redistribution ? '✓ Permitted to redistribute / bundle in open-source repos' : '✗ Do NOT commit or redistribute raw font files on public GitHub repositories'}</span>
        <span class="lic-key">Modification:</span>
        <span class="lic-val">${track.modification ? '✓ Derivatives permitted' : '✗ Modifications prohibited'}</span>
        <span class="lic-key">Verification Status:</span>
        <span class="lic-val"><strong>${track.verification_status?.toUpperCase()}</strong> (${track.verification_date || '2026-09-29'})</span>
        <span class="lic-key">Source & Foundry:</span>
        <span class="lic-val">${track.source || 'N/A'}</span>
        <span class="lic-key">License File:</span>
        <span class="lic-val"><code>${track.license_file || 'Metadata record'}</code></span>
        <span class="lic-key">Terms & Notes:</span>
        <span class="lic-val">${track.redistribution_notes || 'Standard terms apply.'}</span>
      </div>
    `;

    // 4. Code Tokens
    const bestFile = (font.files || []).find(f => f.format === 'woff2') || (font.files || [])[0];
    const cssCode = `/* CSS @font-face and Design Tokens for ${font.name} */
@font-face {
  font-family: '${font.name}';
  src: url('${bestFile ? bestFile.path : font.id + ".woff2"}') format('${bestFile ? bestFile.format : "woff2"}');
  font-weight: ${weights[0] || 400};
  font-style: ${tech.italic ? 'italic' : 'normal'};
  font-display: swap;
}

:root {
  --font-family-custom: '${font.name}', ${fallbackStack};
  --font-weight-regular: ${weights[0] || 400};
  --font-weight-bold: ${weights[weights.length - 1] || 700};
}

.heading-sample {
  font-family: var(--font-family-custom);
  font-weight: var(--font-weight-bold);
  letter-spacing: -0.02em;
}`;

    const flutterCode = `# Flutter pubspec.yaml declaration
flutter:
  fonts:
    - family: ${font.name}
      fonts:
        - asset: fonts/${font.id}-regular.ttf
          weight: ${weights[0] || 400}

// Dart TextStyle
final customStyle = TextStyle(
  fontFamily: '${font.name}',
  fontWeight: FontWeight.w${weights[0] || 400},
  fontSize: 16.0,
);`;

    elements.codeCss.textContent = cssCode;
    elements.codeFlutter.textContent = flutterCode;

    elements.modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    elements.modal.classList.add('hidden');
    document.body.style.overflow = '';
  }

  /**
   * Copy Helpers & Toast
   */
  function copyFontCss(font) {
    const cur = font.curated || {};
    const best = (font.files || []).find(f => f.format === 'woff2') || (font.files || [])[0];
    const css = `@font-face {
  font-family: '${font.name}';
  src: url('${best ? best.path : font.id + ".woff2"}') format('${best ? best.format : "woff2"}');
  font-display: swap;
}`;
    copyToClipboard(css, `Copied @font-face CSS for ${font.name}!`);
  }

  function copyToClipboard(text, msg) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => showToast(msg));
    } else {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast(msg);
    }
  }

  function showToast(msg) {
    elements.toastMsg.textContent = msg;
    elements.toast.classList.remove('hidden');
    setTimeout(() => {
      elements.toast.classList.add('hidden');
    }, 2500);
  }

  function escapeHtml(str) {
    return (str || '').replace(/[&<>"']/g, m => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[m]);
  }

  /**
   * Setup Event Listeners
   */
  function setupEventListeners() {
    // Search
    elements.searchInput.addEventListener('input', e => {
      state.searchQuery = e.target.value;
      applyFilters();
    });

    // Keyboard shortcut '/' to search
    window.addEventListener('keydown', e => {
      if (e.key === '/' && document.activeElement !== elements.searchInput && document.activeElement !== elements.customTextInput) {
        e.preventDefault();
        elements.searchInput.focus();
      }
      if (e.key === 'Escape' && !elements.modal.classList.contains('hidden')) {
        closeModal();
      }
    });

    // Filters
    elements.filterCategory.addEventListener('change', e => { state.selectedCategory = e.target.value; applyFilters(); });
    elements.filterStyle.addEventListener('change', e => { state.selectedStyle = e.target.value; applyFilters(); });
    elements.filterScript.addEventListener('change', e => { state.selectedScript = e.target.value; applyFilters(); });
    elements.filterRole.addEventListener('change', e => { state.selectedRole = e.target.value; applyFilters(); });
    elements.filterLicense.addEventListener('change', e => { state.selectedLicense = e.target.value; applyFilters(); });
    elements.filterVariable.addEventListener('change', e => { state.variableOnly = e.target.checked; applyFilters(); });

    elements.filterReadability.addEventListener('input', e => {
      state.minReadability = parseInt(e.target.value, 10);
      elements.readabilityVal.textContent = `≥ ${state.minReadability}/10`;
      applyFilters();
    });

    // Custom text
    elements.customTextInput.addEventListener('input', e => {
      state.previewText = e.target.value || 'Sphinx of black quartz, judge my vow.';
      renderGrid();
    });

    // Preset pills
    elements.presetPills.forEach(pill => {
      pill.addEventListener('click', () => {
        elements.presetPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const text = pill.getAttribute('data-preset');
        state.previewText = text;
        elements.customTextInput.value = text;
        renderGrid();
      });
    });

    // Font size slider
    elements.fontSizeSlider.addEventListener('input', e => {
      state.fontSize = parseInt(e.target.value, 10);
      elements.fontSizeVal.textContent = `${state.fontSize}px`;
      renderGrid();
    });

    // View toggles
    elements.viewGridBtn.addEventListener('click', () => {
      state.viewMode = 'grid';
      elements.viewGridBtn.classList.add('active');
      elements.viewStreamBtn.classList.remove('active');
      elements.fontGrid.classList.remove('stream-layout');
    });

    elements.viewStreamBtn.addEventListener('click', () => {
      state.viewMode = 'stream';
      elements.viewStreamBtn.classList.add('active');
      elements.viewGridBtn.classList.remove('active');
      elements.fontGrid.classList.add('stream-layout');
    });

    // Reset filters
    const resetAll = () => {
      state.searchQuery = '';
      state.selectedCategory = '';
      state.selectedStyle = '';
      state.selectedScript = '';
      state.selectedRole = '';
      state.selectedLicense = '';
      state.variableOnly = false;
      state.minReadability = 1;
      state.previewText = 'Sphinx of black quartz, judge my vow.';
      state.fontSize = 28;

      elements.searchInput.value = '';
      elements.filterCategory.value = '';
      elements.filterStyle.value = '';
      elements.filterScript.value = '';
      elements.filterRole.value = '';
      elements.filterLicense.value = '';
      elements.filterVariable.checked = false;
      elements.filterReadability.value = 1;
      elements.readabilityVal.textContent = '≥ 1/10';
      elements.customTextInput.value = state.previewText;
      elements.fontSizeSlider.value = 28;
      elements.fontSizeVal.textContent = '28px';

      elements.presetPills.forEach((p, idx) => p.classList.toggle('active', idx === 0));

      applyFilters();
    };

    elements.btnResetFilters.addEventListener('click', resetAll);
    elements.btnClearEmpty.addEventListener('click', resetAll);

    // Modal tabs & close
    elements.modalCloseBtn.addEventListener('click', closeModal);
    elements.modal.addEventListener('click', e => {
      if (e.target === elements.modal) closeModal();
    });

    elements.modalTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        elements.modalTabs.forEach(t => t.classList.remove('active'));
        elements.tabPanes.forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        const target = tab.getAttribute('data-tab');
        document.getElementById(`tab-${target}`).classList.add('active');
      });
    });

    elements.btnCopyCss.addEventListener('click', () => {
      copyToClipboard(elements.codeCss.textContent, 'Copied CSS tokens to clipboard!');
    });

    elements.btnCopyFlutter.addEventListener('click', () => {
      copyToClipboard(elements.codeFlutter.textContent, 'Copied Flutter tokens to clipboard!');
    });
  }

  // Launch on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
