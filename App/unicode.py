# -*- coding: utf-8 -*-
import os, bisect
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from fontTools.ttLib import TTFont

# from java.lang.Character.UnicodeBlock, with slight differeneces
_BLOCK_STARTS, _BLOCK_NAMES, _BLOCK_FONTS = (lambda x: (
    [i[0] for i in x], [i[1] for i in x], [i[2] for i in x]))([
    (0X0000, None, 'NotoSans-Regular.ttf'),
    (0X0020, 'SPACE', 'NotoSans-Regular.ttf'),
    (0X0021, 'BASIC_PUNCTUATION', 'NotoSans-Regular.ttf'),
    (0X0030, 'DIGIT', 'NotoSans-Regular.ttf'),
    (0X003A, 'BASIC_PUNCTUATION', 'NotoSans-Regular.ttf'),
    (0X0041, 'BASIC_LATIN', 'NotoSans-Regular.ttf'),
    (0X005B, 'BASIC_PUNCTUATION', 'NotoSans-Regular.ttf'),
    (0X0061, 'BASIC_LATIN', 'NotoSans-Regular.ttf'),
    (0X007B, 'BASIC_PUNCTUATION', 'NotoSans-Regular.ttf'),
    (0X007F, None, 'NotoSans-Regular.ttf'),
    (0X00A0, 'LATIN_1_SUPPLEMENT', 'NotoSans-Regular.ttf'),
    (0X00C0, 'LATIN_EXTENDED_LETTER', 'NotoSans-Regular.ttf'),
    (0X0100, 'LATIN_EXTENDED_A', 'NotoSans-Regular.ttf'),
    (0X0180, 'LATIN_EXTENDED_B', 'NotoSans-Regular.ttf'),
    (0X0250, 'IPA_EXTENSIONS', 'NotoSans-Regular.ttf'),
    (0X02B0, 'SPACING_MODIFIER_LETTERS', 'NotoSans-Regular.ttf'),
    (0X0300, 'COMBINING_DIACRITICAL_MARKS', 'NotoSans-Regular.ttf'),
    (0X0370, 'GREEK', 'NotoSans-Regular.ttf'),
    (0X0400, 'CYRILLIC', 'NotoSans-Regular.ttf'),
    (0X0500, 'CYRILLIC_SUPPLEMENTARY', 'NotoSans-Regular.ttf'),
    (0X0530, 'ARMENIAN', 'NotoSansArmenian-Bold.ttf'),
    (0X0590, 'HEBREW', 'NotoSansHebrew-Bold.ttf'),
    (0X0600, 'ARABIC', 'NotoKufiArabic-Bold.ttf'),
    (0X0700, 'SYRIAC', 'NotoSansSyriacEastern-Regular.ttf'),
    (0X0750, 'ARABIC_SUPPLEMENT', 'NotoKufiArabic-Bold.ttf'),
    (0X0780, 'THAANA', 'NotoSansThaana-Bold.ttf'),
    (0X07C0, 'NKO', 'NotoSansNKo-Regular.ttf'),
    (0X0800, 'SAMARITAN', 'NotoSansSamaritan-Regular.ttf'),
    (0X0840, 'MANDAIC', 'NotoSansMandaic-Regular.ttf'),
    (0X0860, None, 'NotoSans-Regular.ttf'),
    (0X0900, 'DEVANAGARI', 'NotoSansDevanagari-Bold.ttf'),
    (0X0980, 'BENGALI', 'NotoSerifBengali-Bold.ttf'),
    (0X0A00, 'GURMUKHI', 'NotoSansGurmukhi-Bold.ttf'),
    (0X0A80, 'GUJARATI', 'NotoSansGujarati-Bold.ttf'),
    (0X0B00, 'ORIYA', 'NotoSansOriya-Bold.ttf'),
    (0X0B80, 'TAMIL', 'NotoSansTamil-Bold.ttf'),
    (0X0C00, 'TELUGU', 'NotoSansTelugu-Bold.ttf'),
    (0X0C80, 'KANNADA', 'NotoSerifKannada-Bold.ttf'),
    (0X0D00, 'MALAYALAM', 'NotoSerifMalayalam-Bold.ttf'),
    (0X0D80, 'SINHALA', 'NotoSansSinhala-Bold.ttf'),
    (0X0E00, 'THAI', 'NotoSansThai-Bold.ttf'),
    (0X0E80, 'LAO', 'NotoSansLao-Bold.ttf'),
    (0X0F00, 'TIBETAN', 'NotoSansTibetan-Bold.ttf'),
    (0X1000, 'MYANMAR', 'NotoSansMyanmar-Bold.ttf'),
    (0X10A0, 'GEORGIAN', 'NotoSansGeorgian-Bold.ttf'),
    (0X1100, 'HANGUL_JAMO', 'NotoSansCJKjp-Black.otf'),
    (0X1200, 'ETHIOPIC', 'NotoSansEthiopic-Bold.ttf'),
    (0X1380, 'ETHIOPIC_SUPPLEMENT', 'NotoSansEthiopic-Bold.ttf'),
    (0X13A0, 'CHEROKEE', 'NotoSansCherokee-Regular.ttf'),
    (0X1400, 'UNIFIED_CANADIAN_ABORIGINAL_SYLLABICS', 'NotoSansCanadianAboriginal-Regular.ttf'),
    (0X1680, 'OGHAM', 'NotoSansOgham-Regular.ttf'),
    (0X16A0, 'RUNIC', 'NotoSansRunic-Regular.ttf'),
    (0X1700, 'TAGALOG', 'NotoSansTagalog-Regular.ttf'),
    (0X1720, 'HANUNOO', 'NotoSansHanunoo-Regular.ttf'),
    (0X1740, 'BUHID', 'NotoSansBuhid-Regular.ttf'),
    (0X1760, 'TAGBANWA', 'NotoSansTagbanwa-Regular.ttf'),
    (0X1780, 'KHMER', 'NotoSansKhmer-Bold.ttf'),
    (0X1800, 'MONGOLIAN', 'NotoSansMongolian-Regular.ttf'),
    (0X18B0, 'UNIFIED_CANADIAN_ABORIGINAL_SYLLABICS_EXTENDED', 'NotoSansCanadianAboriginal-Regular.ttf'),
    (0X1900, 'LIMBU', 'NotoSansLimbu-Regular.ttf'),
    (0X1950, 'TAI_LE', 'NotoSansTaiLe-Regular.ttf'),
    (0X1980, 'NEW_TAI_LUE', 'NotoSansNewTaiLue-Regular.ttf'),
    (0X19E0, 'KHMER_SYMBOLS', 'NotoSansKhmer-Bold.ttf'),
    (0X1A00, 'BUGINESE', 'NotoSansBuginese-Regular.ttf'),
    (0X1A20, 'TAI_THAM', 'NotoSansTaiTham-Regular.ttf'),
    (0X1AB0, None, 'NotoSans-Regular.ttf'),
    (0X1B00, 'BALINESE', 'NotoSansBalinese-Regular.ttf'),
    (0X1B80, 'SUNDANESE', 'NotoSansSundanese-Regular.ttf'),
    (0X1BC0, 'BATAK', 'NotoSansBatak-Regular.ttf'),
    (0X1C00, 'LEPCHA', 'NotoSansLepcha-Regular.ttf'),
    (0X1C50, 'OL_CHIKI', 'NotoSansOlChiki-Regular.ttf'),
    (0X1C80, None, 'NotoSans-Regular.ttf'),
    (0X1CD0, 'VEDIC_EXTENSIONS', 'NotoSansDevanagari-Bold.ttf'),
    (0X1D00, 'PHONETIC_EXTENSIONS', 'NotoSans-Regular.ttf'),
    (0X1D80, 'PHONETIC_EXTENSIONS_SUPPLEMENT', 'NotoSans-Regular.ttf'),
    (0X1DC0, 'COMBINING_DIACRITICAL_MARKS_SUPPLEMENT', 'NotoSans-Regular.ttf'),
    (0X1E00, 'LATIN_EXTENDED_ADDITIONAL', 'NotoSans-Regular.ttf'),
    (0X1F00, 'GREEK_EXTENDED', 'NotoSans-Regular.ttf'),
    (0X2000, 'GENERAL_PUNCTUATION', 'NotoSans-Regular.ttf'),
    (0X2070, 'SUPERSCRIPTS_AND_SUBSCRIPTS', 'NotoSans-Regular.ttf'),
    (0X20A0, 'CURRENCY_SYMBOLS', 'NotoSans-Regular.ttf'),
    (0X20D0, 'COMBINING_MARKS_FOR_SYMBOLS', 'NotoSansSymbols-Regular.ttf'),
    (0X2100, 'LETTERLIKE_SYMBOLS', 'NotoSansCJKjp-Black.otf'),
    (0X2150, 'NUMBER_FORMS', 'NotoSans-Regular.ttf'),
    (0X2190, 'ARROWS', 'NotoSans-Regular.ttf'),
    (0X2200, 'MATHEMATICAL_OPERATORS', 'NotoSansCJKjp-Black.otf'),
    (0X2300, 'MISCELLANEOUS_TECHNICAL', 'NotoSansSymbols-Regular.ttf'),
    (0X2400, 'CONTROL_PICTURES', 'NotoSansSymbols-Regular.ttf'),
    (0X2440, 'OPTICAL_CHARACTER_RECOGNITION', 'NotoSansSymbols-Regular.ttf'),
    (0X2460, 'ENCLOSED_ALPHANUMERICS', 'NotoSansCJKjp-Black.otf'),
    (0X2500, 'BOX_DRAWING', 'NotoSans-Regular.ttf'),
    (0X2580, 'BLOCK_ELEMENTS', 'NotoSans-Regular.ttf'),
    (0X25A0, 'GEOMETRIC_SHAPES', 'NotoSans-Regular.ttf'),
    (0X2600, 'MISCELLANEOUS_SYMBOLS', 'NotoColorEmoji.ttf'),
    (0X2700, 'DINGBATS', 'NotoSansSymbols-Regular.ttf'),
    (0X27C0, 'MISCELLANEOUS_MATHEMATICAL_SYMBOLS_A', 'NotoSansSymbols-Regular.ttf'),
    (0X27F0, 'SUPPLEMENTAL_ARROWS_A', 'NotoSansSymbols-Regular.ttf'),
    (0X2800, 'BRAILLE_PATTERNS', 'NotoSansSymbols-Regular.ttf'),
    (0X2900, 'SUPPLEMENTAL_ARROWS_B', 'NotoSansSymbols-Regular.ttf'),
    (0X2980, 'MISCELLANEOUS_MATHEMATICAL_SYMBOLS_B', 'NotoSansSymbols-Regular.ttf'),
    (0X2A00, 'SUPPLEMENTAL_MATHEMATICAL_OPERATORS', 'NotoSansSymbols-Regular.ttf'),
    (0X2B00, 'MISCELLANEOUS_SYMBOLS_AND_ARROWS', 'NotoSansSymbols-Regular.ttf'),
    (0X2C00, 'GLAGOLITIC', 'NotoSansGlagolitic-Regular.ttf'),
    (0X2C60, 'LATIN_EXTENDED_C', 'NotoSans-Regular.ttf'),
    (0X2C80, 'COPTIC', 'NotoSansCoptic-Regular.ttf'),
    (0X2D00, 'GEORGIAN_SUPPLEMENT', 'NotoSansGeorgian-Bold.ttf'),
    (0X2D30, 'TIFINAGH', 'NotoSansTifinagh-Regular.ttf'),
    (0X2D80, 'ETHIOPIC_EXTENDED', 'NotoSansEthiopic-Bold.ttf'),
    (0X2DE0, 'CYRILLIC_EXTENDED_A', 'NotoSans-Regular.ttf'),
    (0X2E00, 'SUPPLEMENTAL_PUNCTUATION', 'NotoSansSymbols-Regular.ttf'),
    (0X2E80, 'CJK_RADICALS_SUPPLEMENT', 'NotoSansCJKjp-Black.otf'),
    (0X2F00, 'KANGXI_RADICALS', 'NotoSansCJKjp-Black.otf'),
    (0X2FE0, None, 'NotoSans-Regular.ttf'),
    (0X2FF0, 'IDEOGRAPHIC_DESCRIPTION_CHARACTERS', 'NotoSansCJKjp-Black.otf'),
    (0X3000, 'CJK_SYMBOLS_AND_PUNCTUATION', 'NotoSansCJKjp-Black.otf'),
    (0X3041, 'HIRAGANA', 'NotoSansCJKjp-Black.otf'),
    (0X3097, 'CJK_SYMBOLS_AND_PUNCTUATION', 'NotoSansCJKjp-Black.otf'),
    (0X30A1, 'KATAKANA', 'NotoSansCJKjp-Black.otf'),
    (0X30FB, 'CJK_SYMBOLS_AND_PUNCTUATION', 'NotoSansCJKjp-Black.otf'),
    (0X30FC, 'KATAKANA', 'NotoSansCJKjp-Black.otf'),
    (0X3100, 'BOPOMOFO', 'NotoSansCJKjp-Black.otf'),
    (0X3130, 'HANGUL_COMPATIBILITY_JAMO', 'NotoSansCJKjp-Black.otf'),
    (0X3190, 'KANBUN', 'NotoSansCJKjp-Black.otf'),
    (0X31A0, 'BOPOMOFO_EXTENDED', 'NotoSansCJKjp-Black.otf'),
    (0X31C0, 'CJK_STROKES', 'NotoSansCJKjp-Black.otf'),
    (0X31F0, 'KATAKANA_PHONETIC_EXTENSIONS', 'NotoSansCJKjp-Black.otf'),
    (0X3200, 'ENCLOSED_CJK_LETTERS_AND_MONTHS', 'NotoSansCJKjp-Black.otf'),
    (0X3300, 'CJK_COMPATIBILITY', 'NotoSansCJKjp-Black.otf'),
    (0X3400, 'CJK_UNIFIED_IDEOGRAPHS_EXTENSION_A', 'NotoSansCJKjp-Black.otf'),
    (0X4DC0, 'YIJING_HEXAGRAM_SYMBOLS', 'NotoSansSymbols-Regular.ttf'),
    (0X4E00, 'CJK_UNIFIED_IDEOGRAPHS', 'NotoSansCJKjp-Black.otf'),
    (0XA000, 'YI_SYLLABLES', 'NotoSansYi-Regular.ttf'),
    (0XA490, 'YI_RADICALS', 'NotoSansYi-Regular.ttf'),
    (0XA4D0, 'LISU', 'NotoSansLisu-Regular.ttf'),
    (0XA500, 'VAI', 'NotoSansVai-Regular.ttf'),
    (0XA640, 'CYRILLIC_EXTENDED_B', 'NotoSans-Regular.ttf'),
    (0XA6A0, 'BAMUM', 'NotoSansBamum-Regular.ttf'),
    (0XA700, 'MODIFIER_TONE_LETTERS', 'NotoSansSymbols-Regular.ttf'),
    (0XA720, 'LATIN_EXTENDED_D', 'NotoSans-Regular.ttf'),
    (0XA800, 'SYLOTI_NAGRI', 'NotoSansSylotiNagri-Regular.ttf'),
    (0XA830, 'COMMON_INDIC_NUMBER_FORMS', 'NotoSansDevanagari-Bold.ttf'),
    (0XA840, 'PHAGS_PA', 'NotoSansPhagsPa-Regular.ttf'),
    (0XA880, 'SAURASHTRA', 'NotoSansSaurashtra-Regular.ttf'),
    (0XA8E0, 'DEVANAGARI_EXTENDED', 'NotoSansDevanagari-Bold.ttf'),
    (0XA900, 'KAYAH_LI', 'NotoSansKayahLi-Regular.ttf'),
    (0XA930, 'REJANG', 'NotoSansRejang-Regular.ttf'),
    (0XA960, 'HANGUL_JAMO_EXTENDED_A', 'NotoSansCJKjp-Black.otf'),
    (0XA980, 'JAVANESE', 'NotoSansJavanese-Regular.ttf'),
    (0XA9E0, None, 'NotoSans-Regular.ttf'),
    (0XAA00, 'CHAM', 'NotoSansCham-Bold.ttf'),
    (0XAA60, 'MYANMAR_EXTENDED_A', 'NotoSansMyanmar-Bold.ttf'),
    (0XAA80, 'TAI_VIET', 'NotoSansTaiViet-Regular.ttf'),
    (0XAAE0, None, 'NotoSans-Regular.ttf'),
    (0XAB00, 'ETHIOPIC_EXTENDED_A', 'NotoSansEthiopic-Bold.ttf'),
    (0XAB30, None, 'NotoSans-Regular.ttf'),
    (0XABC0, 'MEETEI_MAYEK', 'NotoSansMeeteiMayek-Regular.ttf'),
    (0XAC00, 'HANGUL_SYLLABLES', 'NotoSansCJKjp-Black.otf'),
    (0XD7B0, 'HANGUL_JAMO_EXTENDED_B', 'NotoSansCJKjp-Black.otf'),
    (0XD800, 'HIGH_SURROGATES', 'NotoSans-Regular.ttf'),
    (0XDB80, 'HIGH_PRIVATE_USE_SURROGATES', 'NotoSans-Regular.ttf'),
    (0XDC00, 'LOW_SURROGATES', 'NotoSans-Regular.ttf'),
    (0XE000, 'PRIVATE_USE_AREA', 'NotoSans-Regular.ttf'),
    (0XF900, 'CJK_COMPATIBILITY_IDEOGRAPHS', 'NotoSansCJKjp-Black.otf'),
    (0XFB00, 'ALPHABETIC_PRESENTATION_FORMS', 'NotoSansCJKjp-Black.otf'),
    (0XFB50, 'ARABIC_PRESENTATION_FORMS_A', 'NotoKufiArabic-Bold.ttf'),
    (0XFE00, 'VARIATION_SELECTORS', 'NotoSansPhagsPa-Regular.ttf'),
    (0XFE10, 'VERTICAL_FORMS', 'NotoSansCJKjp-Black.otf'),
    (0XFE20, 'COMBINING_HALF_MARKS', 'NotoSans-Regular.ttf'),
    (0XFE30, 'CJK_COMPATIBILITY_FORMS', 'NotoSansCJKjp-Black.otf'),
    (0XFE50, 'SMALL_FORM_VARIANTS', 'NotoSansCJKjp-Black.otf'),
    (0XFE70, 'ARABIC_PRESENTATION_FORMS_B', 'NotoKufiArabic-Bold.ttf'),
    (0XFF00, 'HALFWIDTH_AND_FULLWIDTH_FORMS', 'NotoSansCJKjp-Black.otf'),
    (0XFF10, 'FULLWIDTH_DIGIT', 'NotoSansCJKjp-Black.otf'),
    (0XFF1A, 'HALFWIDTH_AND_FULLWIDTH_FORMS', 'NotoSansCJKjp-Black.otf'),
    (0XFF21, 'FULLWIDTH_LATIN', 'NotoSansCJKjp-Black.otf'),
    (0XFF3B, 'HALFWIDTH_AND_FULLWIDTH_FORMS', 'NotoSansCJKjp-Black.otf'),
    (0XFF41, 'FULLWIDTH_LATIN', 'NotoSansCJKjp-Black.otf'),
    (0XFF5B, 'HALFWIDTH_AND_FULLWIDTH_FORMS', 'NotoSansCJKjp-Black.otf'),
    (0XFFF0, 'SPECIALS', 'NotoSans-Regular.ttf'),
    (0X10000, 'LINEAR_B_SYLLABARY', 'NotoSansLinearB-Regular.ttf'),
    (0X10080, 'LINEAR_B_IDEOGRAMS', 'NotoSansLinearB-Regular.ttf'),
    (0X10100, 'AEGEAN_NUMBERS', 'NotoSansLinearB-Regular.ttf'),
    (0X10140, 'ANCIENT_GREEK_NUMBERS', 'NotoSansSymbols-Regular.ttf'),
    (0X10190, 'ANCIENT_SYMBOLS', 'NotoSansSymbols-Regular.ttf'),
    (0X101D0, 'PHAISTOS_DISC', 'NotoSansSymbols-Regular.ttf'),
    (0X10200, None, 'NotoSans-Regular.ttf'),
    (0X10280, 'LYCIAN', 'NotoSansLycian-Regular.ttf'),
    (0X102A0, 'CARIAN', 'NotoSansCarian-Regular.ttf'),
    (0X102E0, None, 'NotoSans-Regular.ttf'),
    (0X10300, 'OLD_ITALIC', 'NotoSansOldItalic-Regular.ttf'),
    (0X10330, 'GOTHIC', 'NotoSansGothic-Regular.ttf'),
    (0X10350, None, 'NotoSans-Regular.ttf'),
    (0X10380, 'UGARITIC', 'NotoSansUgaritic-Regular.ttf'),
    (0X103A0, 'OLD_PERSIAN', 'NotoSansOldPersian-Regular.ttf'),
    (0X103E0, None, 'NotoSans-Regular.ttf'),
    (0X10400, 'DESERET', 'NotoSansDeseret-Regular.ttf'),
    (0X10450, 'SHAVIAN', 'NotoSansShavian-Regular.ttf'),
    (0X10480, 'OSMANYA', 'NotoSansOsmanya-Regular.ttf'),
    (0X104B0, None, 'NotoSans-Regular.ttf'),
    (0X10800, 'CYPRIOT_SYLLABARY', 'NotoSansCypriot-Regular.ttf'),
    (0X10840, 'IMPERIAL_ARAMAIC', 'NotoSansImperialAramaic-Regular.ttf'),
    (0X10860, None, 'NotoSans-Regular.ttf'),
    (0X10900, 'PHOENICIAN', 'NotoSansPhoenician-Regular.ttf'),
    (0X10920, 'LYDIAN', 'NotoSansLydian-Regular.ttf'),
    (0X10940, None, 'NotoSans-Regular.ttf'),
    (0X10A00, 'KHAROSHTHI', 'NotoSansKharoshthi-Regular.ttf'),
    (0X10A60, 'OLD_SOUTH_ARABIAN', 'NotoSansOldSouthArabian-Regular.ttf'),
    (0X10A80, None, 'NotoSans-Regular.ttf'),
    (0X10B00, 'AVESTAN', 'NotoSansAvestan-Regular.ttf'),
    (0X10B40, 'INSCRIPTIONAL_PARTHIAN', 'NotoSansInscriptionalParthian-Regular.ttf'),
    (0X10B60, 'INSCRIPTIONAL_PAHLAVI', 'NotoSansInscriptionalPahlavi-Regular.ttf'),
    (0X10B80, None, 'NotoSans-Regular.ttf'),
    (0X10C00, 'OLD_TURKIC', 'NotoSansOldTurkic-Regular.ttf'),
    (0X10C50, None, 'NotoSans-Regular.ttf'),
    (0X10E60, 'RUMI_NUMERAL_SYMBOLS', 'NotoSans-Regular.ttf'),
    (0X10E80, None, 'NotoSans-Regular.ttf'),
    (0X11000, 'BRAHMI', 'NotoSansBrahmi-Regular.ttf'),
    (0X11080, 'KAITHI', 'NotoSansKaithi-Regular.ttf'),
    (0X110D0, None, 'NotoSans-Regular.ttf'),
    (0X12000, 'CUNEIFORM', 'NotoSansCuneiform-Regular.ttf'),
    (0X12400, 'CUNEIFORM_NUMBERS_AND_PUNCTUATION', 'NotoSansCuneiform-Regular.ttf'),
    (0X12480, None, 'NotoSans-Regular.ttf'),
    (0X13000, 'EGYPTIAN_HIEROGLYPHS', 'NotoSansEgyptianHieroglyphs-Regular.ttf'),
    (0X13430, None, 'NotoSans-Regular.ttf'),
    (0X16800, 'BAMUM_SUPPLEMENT', 'NotoSansBamum-Regular.ttf'),
    (0X16A40, None, 'NotoSans-Regular.ttf'),
    (0X1B000, 'KANA_SUPPLEMENT', 'NotoSans-Regular.ttf'),
    (0X1B100, None, 'NotoSans-Regular.ttf'),
    (0X1D000, 'BYZANTINE_MUSICAL_SYMBOLS', 'NotoSansSymbols-Regular.ttf'),
    (0X1D100, 'MUSICAL_SYMBOLS', 'NotoSansSymbols-Regular.ttf'),
    (0X1D200, 'ANCIENT_GREEK_MUSICAL_NOTATION', 'NotoSansSymbols-Regular.ttf'),
    (0X1D250, None, 'NotoSans-Regular.ttf'),
    (0X1D300, 'TAI_XUAN_JING_SYMBOLS', 'NotoSansSymbols-Regular.ttf'),
    (0X1D360, 'COUNTING_ROD_NUMERALS', 'NotoSansSymbols-Regular.ttf'),
    (0X1D380, None, 'NotoSans-Regular.ttf'),
    (0X1D400, 'MATHEMATICAL_ALPHANUMERIC_SYMBOLS', 'NotoSansSymbols-Regular.ttf'),
    (0X1D800, None, 'NotoSans-Regular.ttf'),
    (0X1F000, 'MAHJONG_TILES', 'NotoSansSymbols-Regular.ttf'),
    (0X1F030, 'DOMINO_TILES', 'NotoSansSymbols-Regular.ttf'),
    (0X1F0A0, 'PLAYING_CARDS', 'NotoSansSymbols-Regular.ttf'),
    (0X1F100, 'ENCLOSED_ALPHANUMERIC_SUPPLEMENT', 'NotoSansCJKjp-Black.otf'),
    (0X1F200, 'ENCLOSED_IDEOGRAPHIC_SUPPLEMENT', 'NotoSansCJKjp-Black.otf'),
    (0X1F300, 'MISCELLANEOUS_SYMBOLS_AND_PICTOGRAPHS', 'NotoColorEmoji.ttf'),
    (0X1F600, 'EMOTICONS', 'NotoColorEmoji.ttf'),
    (0X1F650, None, 'NotoSans-Regular.ttf'),
    (0X1F680, 'TRANSPORT_AND_MAP_SYMBOLS', 'NotoColorEmoji.ttf'),
    (0X1F700, 'ALCHEMICAL_SYMBOLS', 'NotoSansSymbols-Regular.ttf'),
    (0X1F780, None, 'NotoSans-Regular.ttf'),
    (0X20000, 'CJK_UNIFIED_IDEOGRAPHS_EXTENSION_B', 'NotoSans-Regular.ttf'),
    (0X2A6E0, None, 'NotoSans-Regular.ttf'),
    (0X2A700, 'CJK_UNIFIED_IDEOGRAPHS_EXTENSION_C', 'NotoSans-Regular.ttf'),
    (0X2B740, 'CJK_UNIFIED_IDEOGRAPHS_EXTENSION_D', 'NotoSans-Regular.ttf'),
    (0X2B820, None, 'NotoSans-Regular.ttf'),
    (0X2F800, 'CJK_COMPATIBILITY_IDEOGRAPHS_SUPPLEMENT', 'NotoSansCJKjp-Black.otf'),
    (0X2FA20, None, 'NotoSans-Regular.ttf'),
    (0XE0000, 'TAGS', 'NotoSans-Regular.ttf'),
    (0XE0080, None, 'NotoSans-Regular.ttf'),
    (0XE0100, 'VARIATION_SELECTORS_SUPPLEMENT', 'NotoSans-Regular.ttf'),
    (0XE01F0, None, 'NotoSans-Regular.ttf'),
    (0XF0000, 'SUPPLEMENTARY_PRIVATE_USE_AREA_A', 'NotoSans-Regular.ttf'),
    (0X100000, 'SUPPLEMENTARY_PRIVATE_USE_AREA_B', 'NotoSans-Regular.ttf'),
    (0x10FFFF, None, 'NotoSans-Regular.ttf'),
])

def get_block_of(uchar):
    return _BLOCK_NAMES[bisect.bisect_right(_BLOCK_STARTS, ord(uchar)) - 1]

def get_font_of_char(uchar):
    return _BLOCK_FONTS[bisect.bisect_right(_BLOCK_STARTS, ord(uchar)) - 1]

def get_font_of_block(block):
    return _BLOCK_FONTS[_BLOCK_NAMES]

'''
Image Definitions
'''
def char_in_font(unicode_char, font):
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            if ord(unicode_char) in cmap.cmap:
                return True
    return False

def unicode_to_image(unicode_text, generate_test_file = False):
    # Configuration
    color_scheme = "RGB"
    width = 256
    height = 256
    back_ground_color = (255,255,255)
    font_size = 128
    font_color = (0,0,0)
    blockName = get_block_of(unicode_text[0])
    font = get_font_of_char(unicode_text[0])
    prefix_dir = os.getcwd() + '/'
    if (os.environ.has_key('HOME') and os.environ['HOME'] == '/afs/athena.mit.edu/course/urop/moji'):
        prefix_dir = "/mit/moji/"
    fontFilename = prefix_dir + "fonts/" + font
    ttfont = TTFont(fontFilename)

    im = Image.new(color_scheme, (width, height), back_ground_color)
    if font != "NotoColorEmoji.ttf":
        draw = ImageDraw.Draw(im)
        unicode_font = ImageFont.truetype(fontFilename, font_size)
        (w, h) = unicode_font.getsize(unicode_text[0])
        # TODO: what if w or h are bigger than image dimensions?
        (x, y) = (float(width - w) / 2, float(height - h) / 2)
        draw.text((x, y), unicode_text[0], font=unicode_font, fill=font_color)
        # Character boundary display
        # draw.rectangle([(x,y), (x+w, y+h)], outline=font_color)
        del draw

    # Save first block characters to view
    if generate_test_file:
        if not blockName:
            blockName = "None"
        else:
            decValue = "{0:#0{1}}".format(ord(unicode_text[0]),7)
            hexValue = "{0:#0{1}x}".format(ord(unicode_text[0]),6)
            filename = "test/" + decValue + '_' + blockName + "_" + hexValue + ".png"
            im.save(filename)
    
    return im

'''
Image Testing Methods
'''
def record_block_fonts():
    f = open("txt", "w")
    f2 = open("unicode_unknown_fonts.txt", "w")
    for firstUChar in _BLOCK_STARTS:
        a = unicode_to_image(unichr(firstUChar), True)
        hexValue = "{0:#0{1}x}".format(firstUChar,6)
        line = "(" + hexValue.upper() + ", '" + str(a[0]) + "', '" + str(a[1]) + "'),\n"
        if a[0] is None:
            line = "(" + hexValue.upper() + ", " + str(a[0]) + ", '" + str(a[1]) + "'),\n"
        if not a[2]:
            for offset in xrange(1,6):
                # For some blocks, first characters might be undefined or reserved
                a = unicode_to_image(unichr(firstUChar + offset), True)
                if a[2]:
                    hexValue = "{0:#0{1}x}".format(firstUChar,6)
                    if a[0] is None:
                        line = "(" + hexValue.upper() + ", " + str(a[0]) + ", '" + str(a[1]) + "'),\n"
                    else:
                        line = "(" + hexValue.upper() + ", '" + str(a[0]) + "', '" + str(a[1]) + "'),\n"
                    break
            if not a[2]:
                f2.write(line)
        f.write(line)
    f2.close()
    f.close()

def find_font(unicode_text):
    # Configuration
    color_scheme = "RGB"
    width = 256
    height = 256
    back_ground_color = (255,255,255)
    font_size = 128
    font_color = (0,0,0)
    blockName = get_block_of(unicode_text[0])
    font = get_font_of_char(unicode_text[0])

    prefix_dir = os.getcwd() + '/'
    if (os.environ.has_key('HOME') and os.environ['HOME'] == '/afs/athena.mit.edu/course/urop/moji'):
        prefix_dir = "/mit/moji/"

    fontFilename = prefix_dir + "fonts/" + font
    ttfont = TTFont(fontFilename)

    fonts = os.walk(prefix_dir + '/fonts').next()[2]
    fontIndex = 0
    hasUsableFont = True and blockName is not None
    tempFont = font
    tempFontFilename = fontFilename
    tempTTFont = ttfont
    while blockName is None or not char_in_font(unicode_text[0], tempTTFont):
        if fontIndex >= len(fonts):
            hasUsableFont = False
            break
        tempFont = fonts[fontIndex]
        fontIndex += 1
        if tempFont[-4:] != ".ttf" and tempFont[-4:] != ".otf":
            continue
        tempFontFilename = prefix_dir + "fonts/" + tempFont
        tempTTFont = TTFont(tempFontFilename)

    if hasUsableFont:
        ttfont = tempTTFont
        font = tempFont
        fontFilename = tempFontFilename
        print "[INFO] Found font", font, "for Unicode Block", blockName
    else:
        print "[WARNING] Could not find font for Unicode Block", blockName

    # Write to an external file
    return (blockName, font, hasUsableFont)

def generate_block_first_character_images():
    for code in _BLOCK_STARTS:
        unicode_to_image(unichr(code), True)

# # Main Code
# unicode_text = u'{か'
# unicode_text_image = unicode_to_image(unicode_text)
# output_filename = "test.png"
# unicode_text_image.save(output_filename)

# generate_block_first_character_images()
