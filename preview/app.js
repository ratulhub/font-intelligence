(function () {
  'use strict';

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
    minReadability: 1,
    previewText: 'Sphinx of black quartz, judge my vow.',
    fontSize: 32,
    viewMode: 'stream',
    pairingHeadingId: 'chillax',
    pairingBodyId: 'general-sans',
    pairingArchetype: 'luxury'
  };

  const elements = {
    fontGrid: document.getElementById('font-grid'),
    emptyState: document.getElementById('empty-state'),
    searchInput: document.getElementById('search-input'),
    filterCategory: document.getElementById('filter-category'),
    filterStyle: document.getElementById('filter-style'),
    filterScript: document.getElementById('filter-script'),
    filterRole: document.getElementById('filter-role'),
    filterLicense: document.getElementById('filter-license'),
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
    
    // Pairing Workbench Elements
    pairingWorkbench: document.getElementById('pairing-workbench'),
    pairingToggleBtn: document.getElementById('pairing-toggle-btn'),
    pairingHeadingSelect: document.getElementById('pairing-heading-select'),
    pairingBodySelect: document.getElementById('pairing-body-select'),
    pairingUsecaseSelect: document.getElementById('pairing-usecase-select'),
    pairingScoreVal: document.getElementById('pairing-score-val'),
    pairingScoreRating: document.getElementById('pairing-score-rating'),
    pairingScoreDesc: document.getElementById('pairing-score-desc'),
    pairingEyebrowText: document.getElementById('pairing-eyebrow-text'),
    pairingHeadlineText: document.getElementById('pairing-headline-text'),
    pairingLeadText: document.getElementById('pairing-lead-text'),
    pairingQuoteText: document.getElementById('pairing-quote-text'),
    pairingBtnDemo: document.getElementById('pairing-btn-demo'),

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

  async function init() {
    setupEventListeners();
    await loadCatalogData();
    injectFontFaces();
    updateMetrics();
    initPairingWorkbench();
    applyFilters();
  }

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
      if (window.CATALOG_DATA && window.CATALOG_DATA.fonts) {
        state.fonts = window.CATALOG_DATA.fonts;
      } else {
        elements.fontGrid.innerHTML = `
          <div class="empty-state">
            <h3>Unable to load font catalog</h3>
            <p>Please ensure preview/fonts-data.js is present or serve this folder over HTTP.</p>
          </div>
        `;
      }
    }
  }

  function injectFontFaces() {
    let cssRules = [];
    state.fonts.forEach(font => {
      const files = font.files || [];
      const best = files.find(f => f.format === 'woff2') || files.find(f => f.format === 'ttf') || files[0];
      if (best && best.path) {
        const webPath = '../' + best.path;
        const fmt = best.format === 'woff2' ? 'woff2' : (best.format === 'otf' ? 'opentype' : 'truetype');
        cssRules.push(`
          @font-face {
            font-family: '${font.id}-preview';
            src: url('${webPath}') format('${fmt}');
            font-weight: 100 900;
            font-style: normal;
            font-display: swap;
          }
        `);
      }
    });

    elements.dynamicStyle.textContent = cssRules.join('\n');
  }

  function updateMetrics() {
    if (elements.statTotal) elements.statTotal.textContent = state.fonts.length;
    if (elements.statOpenSource) {
      const pubCount = state.fonts.filter(f => f.distribution_status === 'public-asset').length;
      elements.statOpenSource.textContent = pubCount;
    }
    if (elements.statVariable) {
      const varCount = state.fonts.filter(f => f.technical && f.technical.variable).length;
      elements.statVariable.textContent = varCount;
    }
    if (elements.statFiles) {
      const totalFiles = state.fonts.reduce((acc, f) => acc + (f.files ? f.files.length : 0), 0);
      elements.statFiles.textContent = totalFiles;
    }
  }

  function initPairingWorkbench() {
    if (!elements.pairingHeadingSelect || !elements.pairingBodySelect) return;

    elements.pairingHeadingSelect.innerHTML = '';
    elements.pairingBodySelect.innerHTML = '';

    const sortedFonts = [...state.fonts].sort((a, b) => a.name.localeCompare(b.name));

    sortedFonts.forEach(font => {
      const optH = document.createElement('option');
      optH.value = font.id;
      optH.textContent = `${font.name} (${font.curated?.category || 'sans'})`;
      if (font.id === 'chillax') optH.selected = true;
      elements.pairingHeadingSelect.appendChild(optH);

      const optB = document.createElement('option');
      optB.value = font.id;
      optB.textContent = `${font.name} (${font.curated?.category || 'sans'})`;
      if (font.id === 'general-sans') optB.selected = true;
      elements.pairingBodySelect.appendChild(optB);
    });

    updatePairingStage();
  }

  function updatePairingStage() {
    const headId = elements.pairingHeadingSelect.value;
    const bodyId = elements.pairingBodySelect.value;
    const headFont = state.fonts.find(f => f.id === headId);
    const bodyFont = state.fonts.find(f => f.id === bodyId);

    if (!headFont || !bodyFont) return;

    const headFallback = (headFont.curated?.fallback || ['sans-serif']).join(', ');
    const bodyFallback = (bodyFont.curated?.fallback || ['sans-serif']).join(', ');

    elements.pairingHeadlineText.style.fontFamily = `'${headId}-preview', ${headFallback}`;
    elements.pairingHeadlineText.style.fontWeight = headFont.technical?.weights?.slice(-1)[0] || 700;

    elements.pairingEyebrowText.style.fontFamily = `'${bodyId}-preview', ${bodyFallback}`;
    elements.pairingLeadText.style.fontFamily = `'${bodyId}-preview', ${bodyFallback}`;
    elements.pairingQuoteText.style.fontFamily = `'${headId}-preview', ${headFallback}`;
    elements.pairingBtnDemo.style.fontFamily = `'${bodyId}-preview', ${bodyFallback}`;

    // Scoring heuristic
    let score = 88;
    const headCat = headFont.curated?.category;
    const bodyCat = bodyFont.curated?.category;

    if (headCat !== bodyCat) score += 6;
    if (headFont.curated?.readability?.heading >= 8) score += 2;
    if (bodyFont.curated?.readability?.body >= 8) score += 3;
    if (headId === bodyId) score -= 15;

    score = Math.min(99, Math.max(70, score));

    elements.pairingScoreVal.textContent = score;
    elements.pairingScoreRating.textContent = score >= 94 ? 'Masterclass' : (score >= 88 ? 'Exceptional' : 'Harmonious');
    elements.pairingScoreDesc.textContent = `${headFont.name} + ${bodyFont.name} (${headCat} / ${bodyCat})`;
  }

  function setupEventListeners() {
    if (elements.searchInput) {
      elements.searchInput.addEventListener('input', e => {
        state.searchQuery = e.target.value.toLowerCase().trim();
        applyFilters();
      });

      window.addEventListener('keydown', e => {
        if (e.key === '/' && document.activeElement !== elements.searchInput) {
          e.preventDefault();
          elements.searchInput.focus();
        }
      });
    }

    if (elements.filterCategory) {
      elements.filterCategory.addEventListener('change', e => {
        state.selectedCategory = e.target.value;
        applyFilters();
      });
    }

    if (elements.filterStyle) {
      elements.filterStyle.addEventListener('change', e => {
        state.selectedStyle = e.target.value;
        applyFilters();
      });
    }

    if (elements.filterScript) {
      elements.filterScript.addEventListener('change', e => {
        state.selectedScript = e.target.value;
        applyFilters();
      });
    }

    if (elements.filterRole) {
      elements.filterRole.addEventListener('change', e => {
        state.selectedRole = e.target.value;
        applyFilters();
      });
    }

    if (elements.filterLicense) {
      elements.filterLicense.addEventListener('change', e => {
        state.selectedLicense = e.target.value;
        applyFilters();
      });
    }

    if (elements.filterReadability) {
      elements.filterReadability.addEventListener('input', e => {
        state.minReadability = parseInt(e.target.value, 10);
        elements.readabilityVal.textContent = `≥ ${state.minReadability} / 10`;
        applyFilters();
      });
    }

    if (elements.customTextInput) {
      elements.customTextInput.addEventListener('input', e => {
        state.previewText = e.target.value || 'Sphinx of black quartz, judge my vow.';
        updateSpecimenTexts();
      });
    }

    if (elements.fontSizeSlider) {
      elements.fontSizeSlider.addEventListener('input', e => {
        state.fontSize = parseInt(e.target.value, 10);
        elements.fontSizeVal.textContent = `${state.fontSize}px`;
        updateSpecimenFontSizes();
      });
    }

    elements.presetPills.forEach(pill => {
      pill.addEventListener('click', () => {
        elements.presetPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.previewText = pill.dataset.preset;
        elements.customTextInput.value = state.previewText;
        updateSpecimenTexts();
      });
    });

    if (elements.viewStreamBtn && elements.viewGridBtn) {
      elements.viewStreamBtn.addEventListener('click', () => {
        state.viewMode = 'stream';
        elements.viewStreamBtn.classList.add('active');
        elements.viewGridBtn.classList.remove('active');
        elements.fontGrid.className = 'specimen-stream';
        renderCards();
      });

      elements.viewGridBtn.addEventListener('click', () => {
        state.viewMode = 'grid';
        elements.viewGridBtn.classList.add('active');
        elements.viewStreamBtn.classList.remove('active');
        elements.fontGrid.className = 'specimen-grid';
        renderCards();
      });
    }

    if (elements.pairingToggleBtn) {
      elements.pairingToggleBtn.addEventListener('click', () => {
        elements.pairingWorkbench.classList.toggle('collapsed');
      });
    }

    if (elements.pairingHeadingSelect) {
      elements.pairingHeadingSelect.addEventListener('change', updatePairingStage);
    }
    if (elements.pairingBodySelect) {
      elements.pairingBodySelect.addEventListener('change', updatePairingStage);
    }
    if (elements.pairingUsecaseSelect) {
      elements.pairingUsecaseSelect.addEventListener('change', updatePairingStage);
    }

    if (elements.btnResetFilters) {
      elements.btnResetFilters.addEventListener('click', resetFilters);
    }
    if (elements.btnClearEmpty) {
      elements.btnClearEmpty.addEventListener('click', resetFilters);
    }

    if (elements.modalCloseBtn) {
      elements.modalCloseBtn.addEventListener('click', closeModal);
    }
    if (elements.modal) {
      elements.modal.addEventListener('click', e => {
        if (e.target === elements.modal) closeModal();
      });
    }

    elements.modalTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        elements.modalTabs.forEach(t => t.classList.remove('active'));
        elements.tabPanes.forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        const targetPane = document.getElementById(`tab-${tab.dataset.tab}`);
        if (targetPane) targetPane.classList.add('active');
      });
    });

    if (elements.btnCopyCss) {
      elements.btnCopyCss.addEventListener('click', () => {
        copyToClipboard(elements.codeCss.textContent, 'CSS copied to clipboard');
      });
    }

    if (elements.btnCopyFlutter) {
      elements.btnCopyFlutter.addEventListener('click', () => {
        copyToClipboard(elements.codeFlutter.textContent, 'Flutter code copied to clipboard');
      });
    }
  }

  function applyFilters() {
    state.filteredFonts = state.fonts.filter(font => {
      const cur = font.curated || {};
      const tech = font.technical || {};
      const dist = font.distribution_status || 'unknown';
      const read = cur.readability || {};

      if (state.searchQuery) {
        const q = state.searchQuery;
        const matchesName = font.name.toLowerCase().includes(q) || font.id.toLowerCase().includes(q);
        const matchesCat = (cur.category || '').toLowerCase().includes(q);
        const matchesStyle = (cur.styles || []).some(s => s.toLowerCase().includes(q));
        if (!matchesName && !matchesCat && !matchesStyle) return false;
      }

      if (state.selectedCategory && cur.category !== state.selectedCategory) return false;
      if (state.selectedStyle && !(cur.styles || []).includes(state.selectedStyle)) return false;
      if (state.selectedRole && !(cur.roles || []).includes(state.selectedRole)) return false;

      if (state.selectedLicense) {
        if (dist !== state.selectedLicense) return false;
      }

      if (state.selectedScript) {
        const scripts = (tech.scripts || []).map(s => s.toLowerCase());
        const blocks = (tech.unicode_blocks || []).map(b => b.toLowerCase());
        const target = state.selectedScript.toLowerCase();
        const matchesScript = scripts.some(s => s.includes(target)) || blocks.some(b => b.includes(target));
        if (!matchesScript) return false;
      }

      if (state.minReadability > 1) {
        const bodyScore = read.body || 0;
        const uiScore = read.ui || 0;
        if (Math.max(bodyScore, uiScore) < state.minReadability) return false;
      }

      return true;
    });

    updateResultsMeta();
    renderCards();
  }

  function updateResultsMeta() {
    if (elements.resultsCount) {
      elements.resultsCount.textContent = `Showing ${state.filteredFonts.length} of ${state.fonts.length} families`;
    }

    if (!elements.activeChips) return;
    elements.activeChips.innerHTML = '';

    const addChip = (label, onRemove) => {
      const chip = document.createElement('span');
      chip.className = 'active-chip';
      chip.innerHTML = `${label} <span class="chip-remove" aria-label="Remove filter">&times;</span>`;
      chip.querySelector('.chip-remove').addEventListener('click', onRemove);
      elements.activeChips.appendChild(chip);
    };

    if (state.selectedCategory) {
      addChip(`Category: ${state.selectedCategory}`, () => {
        state.selectedCategory = '';
        elements.filterCategory.value = '';
        applyFilters();
      });
    }

    if (state.selectedStyle) {
      addChip(`Style: ${state.selectedStyle}`, () => {
        state.selectedStyle = '';
        elements.filterStyle.value = '';
        applyFilters();
      });
    }

    if (state.selectedScript) {
      addChip(`Script: ${state.selectedScript}`, () => {
        state.selectedScript = '';
        elements.filterScript.value = '';
        applyFilters();
      });
    }

    if (state.selectedRole) {
      addChip(`Role: ${state.selectedRole}`, () => {
        state.selectedRole = '';
        elements.filterRole.value = '';
        applyFilters();
      });
    }

    if (state.selectedLicense) {
      addChip(`Status: ${state.selectedLicense}`, () => {
        state.selectedLicense = '';
        elements.filterLicense.value = '';
        applyFilters();
      });
    }

    if (state.minReadability > 1) {
      addChip(`Readability: ≥ ${state.minReadability}`, () => {
        state.minReadability = 1;
        elements.filterReadability.value = 1;
        elements.readabilityVal.textContent = '≥ 1 / 10';
        applyFilters();
      });
    }
  }

  function resetFilters() {
    state.searchQuery = '';
    state.selectedCategory = '';
    state.selectedStyle = '';
    state.selectedScript = '';
    state.selectedRole = '';
    state.selectedLicense = '';
    state.minReadability = 1;

    if (elements.searchInput) elements.searchInput.value = '';
    if (elements.filterCategory) elements.filterCategory.value = '';
    if (elements.filterStyle) elements.filterStyle.value = '';
    if (elements.filterScript) elements.filterScript.value = '';
    if (elements.filterRole) elements.filterRole.value = '';
    if (elements.filterLicense) elements.filterLicense.value = '';
    if (elements.filterReadability) {
      elements.filterReadability.value = 1;
      elements.readabilityVal.textContent = '≥ 1 / 10';
    }

    applyFilters();
  }

  function renderCards() {
    if (!state.filteredFonts.length) {
      elements.fontGrid.innerHTML = '';
      elements.emptyState.classList.remove('hidden');
      return;
    }

    elements.emptyState.classList.add('hidden');

    if (state.viewMode === 'stream') {
      renderStream();
    } else {
      renderGrid();
    }
  }

  function renderStream() {
    const html = state.filteredFonts.map(font => {
      const cur = font.curated || {};
      const tech = font.technical || {};
      const dist = font.distribution_status || 'unknown';
      const weights = tech.weights || [400];
      const fallbackStack = (cur.fallback || ['sans-serif']).join(', ');

      let statusBadge = '<span class="tag-pill tag-verified">Public Open-Source</span>';
      if (dist === 'catalog-only') {
        statusBadge = '<span class="tag-pill tag-review">Catalog Only</span>';
      } else if (dist === 'restricted') {
        statusBadge = '<span class="tag-pill tag-restricted">Restricted</span>';
      }

      const weightChips = weights.map((w, i) => `
        <button class="weight-selector-chip ${i === 0 ? 'active' : ''}" data-weight="${w}">${w}</button>
      `).join('');

      return `
        <article class="specimen-entry" data-id="${font.id}">
          <div class="entry-meta-row">
            <div class="entry-title-wrap">
              <span class="entry-name" data-action="open-modal">${font.name}</span>
              <span class="entry-subtype">${cur.subtype || 'Digital Typeface'}</span>
            </div>

            <div class="entry-badges">
              <span class="tag-pill tag-category">${cur.category || 'sans-serif'}</span>
              ${statusBadge}
              ${tech.variable ? '<span class="tag-pill tag-variable">Variable</span>' : ''}
              ${tech.italic ? '<span class="tag-pill tag-category">Italic</span>' : ''}
            </div>

            <div class="entry-weights-row">
              ${weightChips}
            </div>
          </div>

          <div class="entry-canvas">
            <div class="entry-specimen-text" style="font-family: '${font.id}-preview', ${fallbackStack}; font-size: ${state.fontSize}px; font-weight: ${weights[0] || 400};">
              ${escapeHtml(state.previewText)}
            </div>
          </div>

          <div class="entry-substrip">
            <div class="glyph-strip" style="font-family: '${font.id}-preview', ${fallbackStack};">
              Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz • 0123456789
            </div>

            <div class="entry-actions">
              <button class="btn btn-outline btn-sm" data-action="pair">Test Pairing</button>
              <button class="btn btn-primary btn-sm" data-action="open-modal">Specimen Sheet</button>
            </div>
          </div>
        </article>
      `;
    }).join('');

    elements.fontGrid.innerHTML = html;
    attachCardListeners();
  }

  function renderGrid() {
    const html = state.filteredFonts.map(font => {
      const cur = font.curated || {};
      const tech = font.technical || {};
      const dist = font.distribution_status || 'unknown';
      const weights = tech.weights || [400];
      const fallbackStack = (cur.fallback || ['sans-serif']).join(', ');

      let statusBadge = '<span class="tag-pill tag-verified">Public</span>';
      if (dist === 'catalog-only') statusBadge = '<span class="tag-pill tag-review">Catalog Only</span>';
      else if (dist === 'restricted') statusBadge = '<span class="tag-pill tag-restricted">Restricted</span>';

      return `
        <article class="specimen-entry" data-id="${font.id}" style="padding: 18px 20px;">
          <div class="entry-meta-row" style="margin-bottom: 8px;">
            <div class="entry-title-wrap">
              <span class="entry-name" style="font-size: 20px;" data-action="open-modal">${font.name}</span>
            </div>
            <div class="entry-badges">
              <span class="tag-pill tag-category">${cur.category || 'sans'}</span>
              ${statusBadge}
            </div>
          </div>

          <div class="entry-canvas" style="padding: 8px 0;">
            <div class="entry-specimen-text" style="font-family: '${font.id}-preview', ${fallbackStack}; font-size: ${Math.min(state.fontSize, 36)}px; font-weight: ${weights[0] || 400};">
              ${escapeHtml(state.previewText)}
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-hairline); padding-top: 10px; margin-top: 4px;">
            <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">${weights.length} weights</span>
            <button class="btn btn-outline btn-sm" data-action="open-modal" style="padding: 4px 8px; font-size: 11px;">Inspect</button>
          </div>
        </article>
      `;
    }).join('');

    elements.fontGrid.innerHTML = html;
    attachCardListeners();
  }

  function attachCardListeners() {
    document.querySelectorAll('.specimen-entry').forEach(card => {
      const fontId = card.dataset.id;
      const font = state.fonts.find(f => f.id === fontId);
      if (!font) return;

      const specimenEl = card.querySelector('.entry-specimen-text');

      card.querySelectorAll('.weight-selector-chip').forEach(chip => {
        chip.addEventListener('click', e => {
          e.stopPropagation();
          card.querySelectorAll('.weight-selector-chip').forEach(c => c.classList.remove('active'));
          chip.classList.add('active');
          if (specimenEl) {
            specimenEl.style.fontWeight = chip.dataset.weight;
          }
        });
      });

      card.querySelectorAll('[data-action="open-modal"]').forEach(btn => {
        btn.addEventListener('click', e => {
          e.stopPropagation();
          openModal(font);
        });
      });

      card.querySelectorAll('[data-action="pair"]').forEach(btn => {
        btn.addEventListener('click', e => {
          e.stopPropagation();
          if (elements.pairingHeadingSelect) {
            elements.pairingHeadingSelect.value = font.id;
            updatePairingStage();
            elements.pairingWorkbench.classList.remove('collapsed');
            elements.pairingWorkbench.scrollIntoView({ behavior: 'smooth' });
          }
        });
      });
    });
  }

  function updateSpecimenTexts() {
    document.querySelectorAll('.entry-specimen-text').forEach(el => {
      el.textContent = state.previewText;
    });
  }

  function updateSpecimenFontSizes() {
    document.querySelectorAll('.entry-specimen-text').forEach(el => {
      el.style.fontSize = `${state.fontSize}px`;
    });
  }

  function openModal(font) {
    state.activeFont = font;
    const cur = font.curated || {};
    const tech = font.technical || {};
    const lic = font.license || {};
    const track = lic.tracking || {};
    const weights = tech.weights || [400];
    const fallbackStack = (cur.fallback || ['sans-serif']).join(', ');

    elements.modalFontName.textContent = font.name;
    elements.modalFontCat.textContent = cur.category || 'Family';
    elements.modalFontId.textContent = font.id;

    // 1. Waterfall
    const waterfallSizes = [64, 48, 36, 24, 18, 14];
    elements.waterfallList.innerHTML = waterfallSizes.map(size => `
      <div class="waterfall-item">
        <div class="waterfall-meta">
          <span>${size}px</span>
          <span>Weight: ${weights[0] || 400}</span>
        </div>
        <div style="font-family: '${font.id}-preview', ${fallbackStack}; font-size: ${size}px; font-weight: ${weights[0] || 400}; line-height: 1.2;">
          ${escapeHtml(state.previewText)}
        </div>
      </div>
    `).join('');

    // 2. Glyphs
    const latinUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const latinLower = 'abcdefghijklmnopqrstuvwxyz';
    elements.glyphsLetters.innerHTML = (latinUpper + latinLower).split('').map(char => `
      <div class="glyph-cell" style="font-family: '${font.id}-preview', ${fallbackStack};">${char}</div>
    `).join('');

    const numerals = '0123456789$€£¥%+-=';
    elements.glyphsNumbers.innerHTML = numerals.split('').map(char => `
      <div class="glyph-cell" style="font-family: '${font.id}-preview', ${fallbackStack};">${char}</div>
    `).join('');

    const symbols = '.,:;!?&@#*(){}[]"/\\';
    elements.glyphsSymbols.innerHTML = symbols.split('').map(char => `
      <div class="glyph-cell" style="font-family: '${font.id}-preview', ${fallbackStack};">${char}</div>
    `).join('');

    // 3. Licensing Details
    elements.licensingContent.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 14px; font-size: 13px;">
        <div><strong>License:</strong> ${track.license_name || lic.type}</div>
        <div><strong>Commercial Use:</strong> ${track.commercial_use ? 'Approved for commercial projects' : 'Personal / Demo only'}</div>
        <div><strong>Redistribution:</strong> ${track.redistribution ? 'Permitted in public open-source repositories' : 'Restricted; retain in catalog-only mode'}</div>
        <div><strong>Source / Foundry:</strong> ${track.source || 'Foundry Package'}</div>
        <div><strong>Notes:</strong> ${track.redistribution_notes || 'Standard terms apply.'}</div>
      </div>
    `;

    // 4. Code Tokens
    const bestFile = (font.files || []).find(f => f.format === 'woff2') || (font.files || [])[0];
    const cssCode = `@font-face {
  font-family: '${font.name}';
  src: url('../fonts/${bestFile ? bestFile.filename || font.id + '.woff2' : font.id + '.woff2'}') format('${bestFile?.format || "woff2"}');
  font-weight: ${weights[0] || 400};
  font-style: ${tech.italic ? 'italic' : 'normal'};
  font-display: swap;
}

:root {
  --font-${font.id}: '${font.name}', ${fallbackStack};
}`;

    const flutterCode = `flutter:
  fonts:
    - family: ${font.name}
      fonts:
        - asset: assets/fonts/${font.id}/${font.id}-regular.ttf
          weight: ${weights[0] || 400}`;

    elements.codeCss.textContent = cssCode;
    elements.codeFlutter.textContent = flutterCode;

    elements.modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    elements.modal.classList.add('hidden');
    document.body.style.overflow = '';
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
    }, 2400);
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  window.addEventListener('DOMContentLoaded', init);
})();
