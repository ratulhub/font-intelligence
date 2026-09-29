# Flutter Typography Reference

Complete guide to declaring, loading, and styling Font Intelligence typefaces in Flutter mobile and desktop apps.

---

## 1. Asset Configuration (`pubspec.yaml`)

Place font files in `assets/fonts/` and register them in `pubspec.yaml`:

```yaml
flutter:
  uses-material-design: true

  fonts:
    - family: Chillax
      fonts:
        - asset: assets/fonts/Chillax-Bold.ttf
          weight: 700

    - family: GeneralSans
      fonts:
        - asset: assets/fonts/GeneralSans-Regular.ttf
          weight: 400
        - asset: assets/fonts/GeneralSans-Medium.ttf
          weight: 500
        - asset: assets/fonts/GeneralSans-Bold.ttf
          weight: 700
```

---

## 2. TextTheme Configuration (`theme/typography.dart`)

Configure `TextTheme` inside your application's `ThemeData`:

```dart
import 'package:flutter/material.dart';

class AppTypography {
  static const String headingFamily = 'Chillax';
  static const String bodyFamily = 'GeneralSans';

  static TextTheme createTextTheme(BuildContext context) {
    return const TextTheme(
      displayLarge: TextStyle(
        fontFamily: headingFamily,
        fontSize: 48,
        fontWeight: FontWeight.w700,
        letterSpacing: -1.2,
        height: 1.15,
      ),
      headlineMedium: TextStyle(
        fontFamily: headingFamily,
        fontSize: 28,
        fontWeight: FontWeight.w700,
        letterSpacing: -0.5,
        height: 1.25,
      ),
      bodyLarge: TextStyle(
        fontFamily: bodyFamily,
        fontSize: 16,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
        height: 1.6,
      ),
      bodyMedium: TextStyle(
        fontFamily: bodyFamily,
        fontSize: 14,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
        height: 1.5,
      ),
      labelLarge: TextStyle(
        fontFamily: bodyFamily,
        fontSize: 14,
        fontWeight: FontWeight.w600,
        letterSpacing: 0.3,
      ),
    );
  }
}
```

---

## 3. Handling Fallback Scripts (Bangla / Arabic)

Flutter automatically uses system fallback fonts for characters missing from custom font files. However, you can declare fallback font families explicitly in `TextStyle`:

```dart
TextStyle(
  fontFamily: 'GeneralSans',
  fontFamilyFallback: const ['HindSiliguri', 'NotoSansBengali', 'Roboto'],
  fontSize: 16,
)
```
