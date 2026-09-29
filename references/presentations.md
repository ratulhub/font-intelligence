# Presentation Typography Reference (PowerPoint & Google Slides)

Typography for pitch decks, corporate presentations, and academic keynotes. Designed for high legibility at extreme viewing distances and reliable file sharing.

---

## 1. Viewing Distance & Projection Contrast

- **Slide Headings**: Minimum **32pt to 44pt**. Viewers at the back of a conference room must be able to read headers in under 2 seconds.
- **Body Bullets**: Minimum **18pt to 24pt**. Never use < 16pt text on presentation slides.
- **Limit Density**: Maximum 6 lines of text per slide (the "6x6 Rule"). High-contrast typefaces emphasize clarity over narrative density.

---

## 2. Microsoft PowerPoint TrueType (`.ttf`) Embedding Rule

**Critical Technical Limitation**:
- Microsoft PowerPoint and Word on Windows and macOS frequently fail to render or embed OpenType with PostScript outlines (`.otf`) or CFF fonts, silently substituting them with system default fonts (Calibri or Arial).
- **Mandate**: For all slide decks and documents distributed as `.pptx` or `.docx`, **always use TrueType (`.ttf`) outlines** and verify that `OS/2.fsType` permissions permit Installable or Editable Embedding.

### How to Embed Fonts in PowerPoint (Windows):
1. Open **File** > **Options** > **Save**.
2. Under *Preserve fidelity when sharing this presentation*, check **Embed fonts in the file**.
3. Select **Embed all characters (best for editing by other people)**.

---

## 3. Recommended Presentation Pairings

| Use Case | Slide Heading (36pt+) | Bullet Body (18pt+) | Vibe |
| :--- | :--- | :--- | :--- |
| **Startup Pitch Deck** | `Chillax` (700) | `General Sans` (400) | High-growth, modern, visionary |
| **Corporate / Financial** | `General Sans` (700) | `Ubuntu` (400) | Trustworthy, disciplined, crisp |
| **Academic / Keynote** | `Credit Valley` (700) | `Credit Valley` (400) | Scholarly, distinguished, intellectual |
| **Creative / Agency** | `Ithaca` (500) | `General Sans` (400) | High-fashion, avant-garde, premium |
