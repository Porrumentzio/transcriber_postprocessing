import xml.etree.ElementTree as ET

def truncate_text(text, max_words=4):
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:2]) + " (...) " + " ".join(words[-2:])

def fix_typo_formatting(xml_path, tree=None):
    """
    Fix formatting typos in text following <Sync> tags:
    1. If segment is "(Musika)" replace it with empty string.
    2. If text ends with ',', replace ',' with '...'.
    3. Capitalize first letter if starting lowercase.
    4. Add period at the end if missing punctuation (?, !, .)
    """
    if tree is None:
        tree = ET.parse(xml_path)
    root = tree.getroot()

    syncs = root.findall(".//Sync")
    cap_corrections = []
    punct_corrections = []
    other_corrections = []

    for sync in syncs:
        text = sync.tail
        if not text or text.strip() == "":
            continue

        fixed_text = text.strip()
        original_text = fixed_text

        # Rule: if segment is exactly "(Musika)", replace with empty string
        if fixed_text == "(Musika)":
            fixed_text = ""
            other_corrections.append(f"'(Musika)' -> empty string")
            sync.tail = fixed_text + " "
            continue  # Skip other corrections on empty

        # Rule: convert trailing comma to ellipsis
        if fixed_text.endswith(","):
            fixed_text = fixed_text[:-1] + "..."

        # Capitalization correction
        capitalized = False
        if fixed_text and fixed_text[0].islower():
            fixed_text = fixed_text[0].upper() + fixed_text[1:]
            capitalized = True

        # Punctuation correction
        punctuated = False
        if fixed_text and fixed_text[-1] not in {'.', '?', '!'}:
            fixed_text += '.'
            punctuated = True

        if fixed_text != original_text:
            sync.tail = fixed_text + " "
            if capitalized:
                cap_corrections.append(
                    f"'{original_text}' -> '{truncate_text(fixed_text)}'"
                )
            if punctuated:
                punct_corrections.append(
                    f"'{original_text}' -> '{truncate_text(fixed_text)}'"
                )
            if not capitalized and not punctuated and fixed_text != original_text:
                other_corrections.append(
                    f"'{original_text}' -> '{truncate_text(fixed_text)}'"
                )

    if other_corrections:
        print("\nSpecial corrections:")
        for line in other_corrections:
            print(f"    {line}")
    else:
        print("\nNo other special corrections needed.")

    if cap_corrections:
        print("\nCapitalization corrections at the beginning of a sentence:")
        for c in cap_corrections:
            print(f"    {c}")
    else:
        print("\nNo capitalization corrections needed at the beginning of a sentence.")

    if punct_corrections:
        print("\nPunctuation corrections:")
        for p in punct_corrections:
            print(f"    {p}")
    else:
        print("\nNo punctuation corrections needed.")

    return tree
