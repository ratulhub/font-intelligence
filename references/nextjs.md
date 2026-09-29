# Next.js Typography & Font Optimization Reference

Next.js provides built-in automatic font optimization through `next/font`. It automatically downloads font files at build time, hosts them with other static assets, and eliminates layout shift (CLS).

---

## 1. Local Fonts with `next/font/local`

For Font Intelligence catalog fonts stored as local files:

```typescript
// app/fonts.ts or src/lib/fonts.ts
import localFont from 'next/font/local';

export const fontHeading = localFont({
  src: [
    {
      path: '../public/fonts/Chillax-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  variable: '--font-heading',
  display: 'swap',
});

export const fontBody = localFont({
  src: [
    {
      path: '../public/fonts/GeneralSans-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../public/fonts/GeneralSans-Medium.woff2',
      weight: '500',
      style: 'normal',
    },
  ],
  variable: '--font-body',
  display: 'swap',
});
```

---

## 2. Root Layout Integration (App Router)

Apply the font CSS variables to the root `<html>` element:

```tsx
// app/layout.tsx
import { fontHeading, fontBody } from './fonts';
import './globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${fontHeading.variable} ${fontBody.variable}`}>
      <body className="font-sans antialiased text-slate-900 bg-white">
        {children}
      </body>
    </html>
  );
}
```

---

## 3. Pairing with Verified Companions for Non-Latin (Bangla/Arabic)

When supporting non-Latin languages, import open-source Google companion fonts via `next/font/google`:

```typescript
import { Hind_Siliguri } from 'next/font/google';

export const fontBangla = Hind_Siliguri({
  subsets: ['bengali'],
  weight: ['400', '600', '700'],
  variable: '--font-bangla',
  display: 'swap',
});
```
