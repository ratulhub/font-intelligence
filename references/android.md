# Native Android (XML & Jetpack Compose) Typography Reference

Configuring Font Intelligence typefaces in native Android development.

---

## 1. Jetpack Compose (`ui/theme/Type.kt`)

Place TrueType (`.ttf`) or OpenType (`.otf`) binaries into `app/src/main/res/font/`:
*(Note: Android requires all-lowercase file names with underscores, e.g. `chillax_bold.ttf`, `general_sans_regular.ttf`)*.

```kotlin
package com.example.app.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.example.app.R

val ChillaxFamily = FontFamily(
    Font(R.font.chillax_bold, FontWeight.Bold)
)

val GeneralSansFamily = FontFamily(
    Font(R.font.general_sans_regular, FontWeight.Normal),
    Font(R.font.general_sans_medium, FontWeight.Medium),
    Font(R.font.general_sans_bold, FontWeight.Bold)
)

val AppTypography = Typography(
    headlineLarge = TextStyle(
        fontFamily = ChillaxFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 32.sp,
        lineHeight = 38.sp,
        letterSpacing = (-0.5).sp
    ),
    headlineMedium = TextStyle(
        fontFamily = ChillaxFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 24.sp,
        lineHeight = 30.sp,
        letterSpacing = (-0.25).sp
    ),
    bodyLarge = TextStyle(
        fontFamily = GeneralSansFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.sp
    ),
    labelLarge = TextStyle(
        fontFamily = GeneralSansFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    )
)
```

---

## 2. Classic Android XML Font Family (`res/font/app_fonts.xml`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<font-family xmlns:app="http://schemas.android.com/apk/res-auto">
    <font
        app:font="@font/general_sans_regular"
        app:fontStyle="normal"
        app:fontWeight="400" />
    <font
        app:font="@font/general_sans_bold"
        app:fontStyle="normal"
        app:fontWeight="700" />
</font-family>
```
