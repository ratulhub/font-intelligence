# React & Modern Frontend Typography Reference

Implementing custom typography in React applications (Vite, Create React App, Webpack) with full design system support.

---

## 1. Asset Placement & Bundling (Vite)

In Vite-based applications, place font binaries inside `public/fonts/` or `src/assets/fonts/`:
```
src/
├── assets/
│   └── fonts/
│       ├── Chillax-Bold.woff2
│       └── GeneralSans-Regular.woff2
├── styles/
│   └── fonts.css
```

In `src/styles/fonts.css`:
```css
@font-face {
  font-family: 'Chillax';
  src: url('../assets/fonts/Chillax-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'General Sans';
  src: url('../assets/fonts/GeneralSans-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

Import `fonts.css` in your root entry point (`src/main.jsx` or `src/index.tsx`):
```javascript
import './styles/fonts.css';
import './styles/index.css';
```

---

## 2. Design Tokens in Styled-Components or Emotion

If using CSS-in-JS, define calibrated typography tokens:

```javascript
export const typography = {
  fonts: {
    heading: "'Chillax', system-ui, -apple-system, sans-serif",
    body: "'General Sans', -apple-system, BlinkMacSystemFont, sans-serif",
    mono: "'Ubuntu Mono', monospace",
  },
  weights: {
    regular: 400,
    medium: 500,
    bold: 700,
  },
  sizes: {
    hero: '3.5rem',
    h1: '2.5rem',
    h2: '2rem',
    h3: '1.5rem',
    body: '1rem',
    small: '0.875rem',
  },
  letterSpacing: {
    tight: '-0.025em',
    normal: '0',
    wide: '0.05em',
  },
  lineHeights: {
    tight: 1.15,
    normal: 1.6,
  }
};
```

---

## 3. Font Loading Optimization Hooks

Detect font load state to prevent unstyled layout jumps:
```javascript
import { useEffect, useState } from 'react';

export function useFontLoaded(fontFamily) {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (document.fonts) {
      document.fonts.load(`1em "${fontFamily}"`).then(() => {
        setLoaded(true);
      });
    } else {
      setLoaded(true);
    }
  }, [fontFamily]);

  return loaded;
}
```
