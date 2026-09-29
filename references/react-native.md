# React Native Typography Reference

Configuring custom fonts across iOS and Android in React Native (Bare and Expo).

---

## 1. Asset Linking (Bare React Native)

Place TrueType (`.ttf`) or OpenType (`.otf`) fonts in `assets/fonts/`:

Create or edit `react-native.config.js`:
```javascript
module.exports = {
  project: {
    ios: {},
    android: {},
  },
  assets: ['./assets/fonts/'],
};
```

Run asset linking:
```bash
npx react-native-asset
```
This automatically updates `Info.plist` on iOS and copies binaries to `android/app/src/main/assets/fonts/`.

---

## 2. Platform Font Name Differences

- **Android**: References font files by their **exact filename** without extension (e.g. `GeneralSans-Regular`).
- **iOS**: References font files by their internal **PostScript Name** or **Full Name** (e.g. `General Sans` or `GeneralSans-Regular`).

### Universal Typography Helper (`src/theme/typography.js`):
```javascript
import { Platform, StyleSheet } from 'react-native';

const HEADING_FONT = Platform.select({
  ios: 'Chillax-Bold',
  android: 'Chillax-Bold',
});

const BODY_FONT = Platform.select({
  ios: 'GeneralSans-Regular',
  android: 'GeneralSans-Regular',
});

export const styles = StyleSheet.create({
  hero: {
    fontFamily: HEADING_FONT,
    fontSize: 36,
    lineHeight: 42,
    letterSpacing: -0.8,
    color: '#0F172A',
  },
  heading: {
    fontFamily: HEADING_FONT,
    fontSize: 24,
    lineHeight: 30,
    letterSpacing: -0.4,
    color: '#0F172A',
  },
  body: {
    fontFamily: BODY_FONT,
    fontSize: 16,
    lineHeight: 24,
    color: '#334155',
  },
  buttonText: {
    fontFamily: BODY_FONT,
    fontSize: 14,
    fontWeight: '600',
    letterSpacing: 0.2,
    color: '#FFFFFF',
  },
});
```

---

## 3. Expo Configuration (`app.json`)

If using Expo, load fonts with `expo-font`:
```javascript
import { useFonts } from 'expo-font';

const [fontsLoaded] = useFonts({
  'Chillax-Bold': require('./assets/fonts/Chillax-Bold.ttf'),
  'GeneralSans-Regular': require('./assets/fonts/GeneralSans-Regular.ttf'),
});
```
