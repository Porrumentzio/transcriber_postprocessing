import xml.etree.ElementTree as ET

def write_xml_with_formatting(tree, file_path):
    declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_bytes = ET.tostring(tree.getroot(), encoding="utf-8", method="xml")
    xml_str = xml_bytes.decode("utf-8").replace(" />", "/>")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(declaration)
        f.write(xml_str)
    print(f"\nFile saved with cleaned XML formatting: {file_path}")

def get_doctype_line(xml_path):
    with open(xml_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("<!DOCTYPE"):
                return line.strip()
    return None

def insert_doctype(xml_file, doctype_line):
    with open(xml_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    insert_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("<?xml"):
            insert_index = i + 1
            break
    lines.insert(insert_index, doctype_line + "\n")
    with open(xml_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"DOCTYPE line inserted: {doctype_line}")
