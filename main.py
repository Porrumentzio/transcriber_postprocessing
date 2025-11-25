import argparse
from speaker_attributes import process_speaker_attributes
from mode_channel import change_mode_channel
from typo_formatting import fix_typo_formatting
from xml_formatting import write_xml_with_formatting, get_doctype_line, insert_doctype

def main():
    parser = argparse.ArgumentParser(description="XML update process with chained modules.")
    parser.add_argument("-p", "--path", required=True, help="Path to the XML file to process")
    args = parser.parse_args()

    xml_path = args.path

    print(f"Processing XML file: {xml_path}")

    # Step 1: Speaker attributes processing (loads and modifies tree)
    tree = process_speaker_attributes(xml_path)

    # Step 2: Mode channel processing with updated tree
    tree = change_mode_channel(xml_path, tree)

    # Step 3: Typo formatting with updated tree
    tree = fix_typo_formatting(xml_path, tree)

    # Step 4: Write final XML with suffix _zuzenduta
    output_file = xml_path.rsplit('.', 1)[0] + "_zuzenduta." + xml_path.rsplit('.', 1)[1]
    write_xml_with_formatting(tree, output_file)

    # Insert DOCTYPE if exists in original
    doctype_line = get_doctype_line(xml_path)
    if doctype_line:
        insert_doctype(output_file, doctype_line)

if __name__ == "__main__":
    main()
