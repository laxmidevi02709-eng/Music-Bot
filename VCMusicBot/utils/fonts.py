"""Premium font / styled string helpers (Unicode 'mathematical bold' looks like a premium font)."""

_BOLD_MAP = {
    **{c: chr(0x1D5D4 + ord(c) - ord('A')) for c in "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹"},
    **{c: chr(0x1D5EE + ord(c) - ord('a')) for c in "𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓"},
    **{c: chr(0x1D7EC + ord(c) - ord('0')) for c in "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫"},
}

_ITALIC_MAP = {
    **{c: chr(0x1D608 + ord(c) - ord('A')) for c in "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹"},
    **{c: chr(0x1D622 + ord(c) - ord('a')) for c in "𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓"},
}


def premium(text: str) -> str:
    return "".join(_BOLD_MAP.get(ch, ch) for ch in text)


def italic_premium(text: str) -> str:
    return "".join(_ITALIC_MAP.get(ch, ch) for ch in text)
