import xml.etree.ElementTree as ET
import pandas as pd

CSV_MODE_CHANNEL = "./data/speaker-id-mapping.csv"

def load_speaker_mode_channel_map():
    df = pd.read_csv(CSV_MODE_CHANNEL, delimiter=";")
    mapping = {}
    ignored = set()

    for col, (mode, channel) in {
        "SS": ("spontaneous", "studio"),
        "ST": ("spontaneous", "telephone"),
        "PS": ("planned", "studio"),
        "PT": ("planned", "telephone"),
    }.items():
        for spks in df[col].dropna():
            for spk in str(spks).split(";"):
                spk = spk.strip()
                if spk:
                    mapping[spk] = (mode, channel)

    for spks in df["ignore"].dropna():
        for spk in str(spks).split(";"):
            spk = spk.strip()
            if spk:
                ignored.add(spk)

    return mapping, ignored

def change_mode_channel(xml_path, tree=None):
    if tree is None:
        tree = ET.parse(xml_path)
    root = tree.getroot()

    mapping, ignored = load_speaker_mode_channel_map()

    changed_attributes = {
        'mode': [],
        'channel': [],
    }

    for turn in root.findall(".//Turn"):
        spk = turn.get("speaker")
        if not spk:
            continue

        for spk_id in spk.split():
            if spk_id in ignored:
                continue
            if spk_id in mapping:
                mode, channel = mapping[spk_id]

                if "mode" not in turn.attrib:
                    turn.set("mode", mode)
                    changed_attributes['mode'].append(spk_id)

                if "channel" not in turn.attrib:
                    turn.set("channel", channel)
                    changed_attributes['channel'].append(spk_id)

    # Solo mostramos los totales, no cada cambio individual
    print(f"\nChanged mode attributes: {len(changed_attributes['mode'])}")
    print(f"Changed channel attributes: {len(changed_attributes['channel'])}")


    return tree
