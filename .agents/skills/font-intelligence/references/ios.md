# Native iOS (SwiftUI & UIKit) Typography Reference

Configuring Font Intelligence typefaces in native iOS applications with Dynamic Type support.

---

## 1. Bundle Registration (`Info.plist`)

1. Add your `.ttf` or `.otf` files to your Xcode project and ensure their Target Membership includes your main app.
2. In your `Info.plist`, add the key **Fonts provided by application** (`UIAppFonts`):

```xml
<key>UIAppFonts</key>
<array>
    <string>Chillax-Bold.otf</string>
    <string>GeneralSans-Regular.otf</string>
    <string>GeneralSans-Bold.otf</string>
</array>
```

---

## 2. SwiftUI Typography Extension

```swift
import SwiftUI

extension Font {
    static func headingDisplay(size: CGFloat = 34) -> Font {
        return Font.custom("Chillax-Bold", size: size, relativeTo: .largeTitle)
    }

    static func headingTitle(size: CGFloat = 24) -> Font {
        return Font.custom("Chillax-Bold", size: size, relativeTo: .title)
    }

    static func bodyText(size: CGFloat = 16) -> Font {
        return Font.custom("GeneralSans-Regular", size: size, relativeTo: .body)
    }

    static func buttonLabel(size: CGFloat = 15) -> Font {
        return Font.custom("GeneralSans-Bold", size: size, relativeTo: .headline)
    }
}
```

Using `relativeTo:` ensures custom fonts automatically scale with iOS system accessibility settings (Dynamic Type).

---

## 3. Finding the Exact PostScript Name

iOS requires the exact PostScript name, not the file name. Check it in terminal:
```bash
python -c "from fontTools.ttLib import TTFont; f=TTFont('Chillax-Bold.otf'); print(f['name'].getDebugName(6))"
```
Or in Swift:
```swift
for family in UIFont.familyNames {
    for name in UIFont.fontNames(forFamilyName: family) {
        print("Font name: \(name)")
    }
}
```
