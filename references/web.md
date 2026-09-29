# Web Typography & Performance Reference

Optimal web typography prioritizes Core Web Vitals (Largest Contentful Paint, Cumulative Layout Shift), payload size, format compression, and smooth rendering.

---

## 1. Format Hierarchy & Compression

1. **WOFF2 (Web Open Font Format 2)**: Mandatory primary format. Uses Brotli compression (~30% smaller than WOFF). Supported by >98% of global browsers.
2. **WOFF (Web Open Font Format 1)**: Legacy fallback for older web views.
3. **TTF / OTF**: Raw outline formats. Larger payload; use primarily as development fallbacks or for non-browser platforms.
4. **Target Payload Budget**: Total font assets on initial page load should not exceed **100 KB** compressed. Limit initial font weights to 2 or 3 essential cuts (e.g. 400 Regular, 700 Bold).

---

## 2. Production `@font-face` Rules

Always use `font-display: swap` to prevent Flash of Invisible Text (FOIT) and ensure fast Largest Contentful Paint (LCP):

```css
@font-face {
  font-family: 'Chillax';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url('/fonts/Chillax-Bold.woff2') format('woff2'),
       url('/fonts/Chillax-Bold.ttf') format('truetype');
}

@font-face {
  font-family: 'General Sans';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/fonts/GeneralSans-Regular.woff2') format('woff2'),
       url('/fonts/GeneralSans-Regular.ttf') format('truetype');
}
```

---

## 3. CSS Custom Properties Tokens

Define tokens at the root level for easy maintenance and consistent application:

```css
:root {
  --font-heading: 'Chillax', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-body: 'General Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  --font-mono: 'Ubuntu Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  --weight-heading: 700;
  --weight-body: 400;
  --weight-bold: 600;

  --tracking-display: -0.025em;
  --tracking-body: 0;
  --tracking-caps: 0.05em;

  --leading-tight: 1.15;
  --leading-normal: 1.6;
}

h1, h2, h3 {
  font-family: var(--font-heading);
  font-weight: var(--weight-heading);
  letter-spacing: var(--tracking-display);
  line-height: var(--leading-tight);
}

body {
  font-family: var(--font-body);
  font-weight: var(--weight-body);
  letter-spacing: var(--tracking-body);
  line-height: var(--leading-normal);
}
```

---

## 4. Cumulative Layout Shift (CLS) Mitigation

When custom fonts swap in, differences in x-height and width against system fonts can trigger layout shifts.
- Use `size-adjust`, `ascent-override`, and `descent-override` in fallback `@font-face` definitions to match custom font metrics:
```css
@font-face {
  font-family: 'FallbackSans';
  src: local('Arial');
  ascent-override: 95%;
  descent-override: 25%;
  size-adjust: 102%;
}
```
