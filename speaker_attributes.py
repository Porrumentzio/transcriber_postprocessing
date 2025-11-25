import pandas as pd
import xml.etree.ElementTree as ET

CSV_SPEAKER_NAMES = "./data/speaker-names-mapping.csv"

def load_name_accent_mapping(csv_path):
    df = pd.read_csv(csv_path, delimiter=";")
    mapping = {}
    for idx, row in df.iterrows():
        name_upper = str(row['name']).strip().upper()
        correct_name = str(row['correct name']).strip()
        accent_value = row.get('accent', '')
        if pd.isna(accent_value):
            accent_value = ''
        else:
            accent_value = str(accent_value).strip()
        mapping[name_upper] = (correct_name, accent_value)
    return mapping

def uppercase_all_speaker_names(root):
    speakers_block = root.find(".//Speakers")
    if speakers_block is None:
        print("Speakers block not found in the XML file.")
        return {}
    uppercased_to_original = {}
    for speaker in speakers_block.findall("Speaker"):
        orig_name = speaker.get("name")
        if orig_name and not orig_name.isupper():
            upper = orig_name.upper()
            speaker.set("name", upper)
            uppercased_to_original[upper] = orig_name
    return uppercased_to_original

def process_speaker_attributes(xml_path, tree=None):
    csv_path = CSV_SPEAKER_NAMES
    if tree is None:
        tree = ET.parse(xml_path)
    root = tree.getroot()

    uppercased_to_original = uppercase_all_speaker_names(root)
    mapping = load_name_accent_mapping(csv_path)
    correct_names_upper = {v[0].upper(): v[0] for v in mapping.values()}

    changed_names = []
    changed_accents = []
    speakers_block = root.find(".//Speakers")
    if speakers_block is None:
        print("Speakers block not found in the XML file.")
        return tree

    for speaker in speakers_block.findall("Speaker"):
        orig_name = speaker.get("name")
        if not orig_name:
            continue

        orig_name_upper = orig_name.strip().upper()

        if orig_name_upper in mapping:
            new_name, new_accent = mapping[orig_name_upper]
            if orig_name != new_name:
                speaker.set("name", new_name)
                # Guardar el nombre original correspondiente para imprimir
                orig_proper = uppercased_to_original.get(orig_name_upper, orig_name)
                changed_names.append((orig_proper, new_name))
                if orig_name_upper in uppercased_to_original:
                    del uppercased_to_original[orig_name_upper]

            accent_cur = speaker.get("accent", "").strip()
            if not accent_cur and new_accent:
                speaker.set("accent", new_accent)
                changed_accents.append(f"'{new_name}' accent set to '{new_accent}'")

        elif orig_name_upper in correct_names_upper:
            corrected_norm = correct_names_upper[orig_name_upper]
            if orig_name != corrected_norm.upper():
                speaker.set("name", corrected_norm.upper())
                orig_proper = uppercased_to_original.get(orig_name_upper, orig_name)
                changed_names.append((orig_proper, corrected_norm.upper()))
                if orig_name_upper in uppercased_to_original:
                    del uppercased_to_original[orig_name_upper]

            accent_cur = speaker.get("accent", "").strip()
            matched_entry = next((v for v in mapping.values() if v[0].upper() == orig_name_upper), None)
            if matched_entry:
                new_accent = matched_entry[1]
                if not accent_cur and new_accent:
                    speaker.set("accent", new_accent)
                    changed_accents.append(f"'{corrected_norm.upper()}' accent set to '{new_accent}'")

    if uppercased_to_original:
        print("\nUppercased speaker names not changed further:")
        for upper_name, original_name in uppercased_to_original.items():
            print(f"    {original_name} -> {upper_name}")

    if changed_names:
        print("\nChanged names:")
        for orig, new in changed_names:
            print(f"    {orig} -> {new}")
    else:
        print("\nNo names changed.")

    if changed_accents:
        print("\nChanged accents:")
        for entry in changed_accents:
            print(f"    {entry}")
    else:
        print("\nNo accents changed.")

    return tree
