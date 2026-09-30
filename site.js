document.addEventListener("DOMContentLoaded", () => {
  initClipboardButtons();
  initVibePlayground();
  initAgentTabs();
  initSpecimenTester();
});

const VIBE_PRESETS = {
  luxury: {
    category: "High-End Editorial & Luxury",
    headlineText: "The Architecture of Uncompromising Silence.",
    bodyText: "High-contrast Didone serifs meet sculpted neo-grotesque proportion. Wide capital tracking, restrained leadings, and crisp mathematical contrast announce timeless authority.",
    headingFont: "'Cormorant Garamond', Georgia, serif",
    headingWeight: "600",
    headingTracking: "-0.015em",
    headingLineHeight: "1.05",
    bodyFont: "'Hanken Grotesk', -apple-system, sans-serif",
    bodyWeight: "400",
    score: "96 / 100",
    delta: "200 (600 / 400)",
    contrast: "Structural Serif / Sans",
    endurance: "9.4 / 10",
    cssToken: `:root {
  --font-heading: 'Cormorant Garamond', Georgia, serif;
  --font-body: 'Hanken Grotesk', system-ui, sans-serif;
  --font-weight-heading: 600;
  --font-weight-body: 400;
  --letter-spacing-heading: -0.015em;
  --line-height-body: 1.65;
}`
  },
  modernist: {
    category: "Modernist SaaS & Fintech",
    headlineText: "Precision Engineered for High Velocity Systems.",
    bodyText: "Geometric clarity with tall x-height and open counters. Engineered specifically for complex data tables, transaction feeds, and 12px microcopy without optical fatigue.",
    headingFont: "'Plus Jakarta Sans', system-ui, sans-serif",
    headingWeight: "700",
    headingTracking: "-0.025em",
    headingLineHeight: "1.12",
    bodyFont: "'Plus Jakarta Sans', system-ui, sans-serif",
    bodyWeight: "400",
    score: "94 / 100",
    delta: "300 (700 / 400)",
    contrast: "Optical Weight Scale",
    endurance: "9.2 / 10",
    cssToken: `:root {
  --font-heading: 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-body: 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-weight-heading: 700;
  --font-weight-body: 400;
  --letter-spacing-heading: -0.02em;
  --line-height-body: 1.6;
}`
  },
  not_ai: {
    category: "Signature Character — Not AI-Looking",
    headlineText: "Artisanal Grit. Typographic Soul Beyond Defaults.",
    bodyText: "Replaces sterile corporate sameness with distinctive optical curves. Paired with calibrated humanist sans to preserve rock-solid legibility across both web and native apps.",
    headingFont: "'Cinzel', Georgia, serif",
    headingWeight: "700",
    headingTracking: "0.02em",
    headingLineHeight: "1.1",
    bodyFont: "'Hanken Grotesk', system-ui, sans-serif",
    bodyWeight: "400",
    score: "97 / 100",
    delta: "300 (700 / 400)",
    contrast: "Distinctive Vocal Lead",
    endurance: "9.1 / 10",
    cssToken: `:root {
  --font-heading: 'Cinzel', Georgia, serif;
  --font-body: 'Hanken Grotesk', system-ui, sans-serif;
  --font-weight-heading: 700;
  --font-weight-body: 400;
  --letter-spacing-heading: 0.02em;
  --line-height-body: 1.7;
}`
  },
  developer: {
    category: "Developer Tooling & Infrastructure",
    headlineText: "Zero Optical Ambiguity. Uncompromising Clarity.",
    bodyText: "High x-height sans headlines combined with unambiguous monospace tabular characters. Slashed zeroes, distinct 1/l/I glyphs, and calibrated code blocks.",
    headingFont: "'Plus Jakarta Sans', system-ui, sans-serif",
    headingWeight: "600",
    headingTracking: "-0.015em",
    headingLineHeight: "1.15",
    bodyFont: "'JetBrains Mono', Menlo, monospace",
    bodyWeight: "400",
    score: "95 / 100",
    delta: "200 (600 / 400)",
    contrast: "Sans Lead / Mono Data",
    endurance: "9.5 / 10",
    cssToken: `:root {
  --font-heading: 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-body: 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --font-feature-settings: 'tnum' 1, 'zero' 1;
}`
  },
  editorial: {
    category: "Literary & Cultural Publishing",
    headlineText: "The Quiet Majesty of Considered Form.",
    bodyText: "Oldstyle serif cadence rooted in five centuries of printing history. Balanced stroke modulation designed for sustained longform reading endurance on retina displays.",
    headingFont: "'Cormorant Garamond', Georgia, serif",
    headingWeight: "400",
    headingTracking: "-0.01em",
    headingLineHeight: "1.12",
    bodyFont: "'Hanken Grotesk', system-ui, sans-serif",
    bodyWeight: "500",
    score: "98 / 100",
    delta: "Harmonic Optical Balance",
    contrast: "Literary Classic / Grotesque",
    endurance: "9.6 / 10",
    cssToken: `:root {
  --font-heading: 'Cormorant Garamond', Georgia, serif;
  --font-body: 'Hanken Grotesk', system-ui, sans-serif;
  --font-weight-heading: 400;
  --font-weight-body: 500;
  --line-height-body: 1.75;
}`
  }
};

function initVibePlayground() {
  const buttons = document.querySelectorAll(".vibe-btn");
  const headingEl = document.getElementById("vibe-heading");
  const bodyEl = document.getElementById("vibe-body");
  const catEl = document.getElementById("vibe-category");
  const scoreEl = document.getElementById("vibe-score");
  const deltaEl = document.getElementById("vibe-delta");
  const contrastEl = document.getElementById("vibe-contrast");
  const enduranceEl = document.getElementById("vibe-endurance");
  const tokenCodeEl = document.getElementById("vibe-token-code");

  if (!buttons.length || !headingEl) return;

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const vibe = btn.dataset.vibe;
      const data = VIBE_PRESETS[vibe];
      if (!data) return;

      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      headingEl.style.fontFamily = data.headingFont;
      headingEl.style.fontWeight = data.headingWeight;
      headingEl.style.letterSpacing = data.headingTracking;
      headingEl.style.lineHeight = data.headingLineHeight;
      headingEl.textContent = data.headlineText;

      bodyEl.style.fontFamily = data.bodyFont;
      bodyEl.style.fontWeight = data.bodyWeight;
      bodyEl.textContent = data.bodyText;

      if (catEl) catEl.textContent = data.category;
      if (scoreEl) scoreEl.textContent = data.score;
      if (deltaEl) deltaEl.textContent = data.delta;
      if (contrastEl) contrastEl.textContent = data.contrast;
      if (enduranceEl) enduranceEl.textContent = data.endurance;
      if (tokenCodeEl) tokenCodeEl.textContent = data.cssToken;
    });
  });
}

function initAgentTabs() {
  const tabs = document.querySelectorAll(".agent-tab");
  const contents = document.querySelectorAll(".agent-tab-content");

  if (!tabs.length) return;

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const target = tab.dataset.target;
      tabs.forEach(t => t.classList.remove("active"));
      contents.forEach(c => c.classList.remove("active"));

      tab.classList.add("active");
      const targetEl = document.getElementById(target);
      if (targetEl) targetEl.classList.add("active");
    });
  });
}

function initSpecimenTester() {
  const output = document.getElementById("specimen-live-text");
  const sizeInput = document.getElementById("slider-font-size");
  const sizeLabel = document.getElementById("label-font-size");
  const leadingInput = document.getElementById("slider-leading");
  const leadingLabel = document.getElementById("label-leading");
  const trackingInput = document.getElementById("slider-tracking");
  const trackingLabel = document.getElementById("label-tracking");
  const familySelect = document.getElementById("select-font-family");
  const weightSelect = document.getElementById("select-font-weight");

  if (!output) return;

  if (sizeInput) {
    sizeInput.addEventListener("input", (e) => {
      const val = e.target.value;
      output.style.fontSize = val + "px";
      if (sizeLabel) sizeLabel.textContent = val + "px";
    });
  }

  if (leadingInput) {
    leadingInput.addEventListener("input", (e) => {
      const val = e.target.value;
      output.style.lineHeight = val;
      if (leadingLabel) leadingLabel.textContent = val;
    });
  }

  if (trackingInput) {
    trackingInput.addEventListener("input", (e) => {
      const val = (parseFloat(e.target.value) / 100).toFixed(2);
      output.style.letterSpacing = val + "em";
      if (trackingLabel) trackingLabel.textContent = val + "em";
    });
  }

  if (familySelect) {
    familySelect.addEventListener("change", (e) => {
      output.style.fontFamily = e.target.value;
    });
  }

  if (weightSelect) {
    weightSelect.addEventListener("change", (e) => {
      output.style.fontWeight = e.target.value;
    });
  }
}

function initClipboardButtons() {
  document.querySelectorAll("[data-copy-target]").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetSelector = btn.getAttribute("data-copy-target");
      const targetEl = document.querySelector(targetSelector);
      if (!targetEl) return;

      const text = targetEl.innerText || targetEl.textContent;
      navigator.clipboard.writeText(text.trim()).then(() => {
        const originalText = btn.textContent;
        btn.textContent = "Copied!";
        btn.classList.add("btn-copied");
        setTimeout(() => {
          btn.textContent = originalText;
          btn.classList.remove("btn-copied");
        }, 1800);
      }).catch(err => {
        console.error("Clipboard copy failed:", err);
      });
    });
  });

  document.querySelectorAll("[data-copy-text]").forEach(btn => {
    btn.addEventListener("click", () => {
      const text = btn.getAttribute("data-copy-text");
      navigator.clipboard.writeText(text).then(() => {
        const originalText = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => {
          btn.textContent = originalText;
        }, 1800);
      });
    });
  });
}
