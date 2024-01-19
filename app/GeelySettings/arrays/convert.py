import argparse
import os
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify_xml(elem):
    """ Функция для форматирования XML с отступами и переносами строк. """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def process_file(input_path, prefix=''):
    input_dir = os.path.dirname(input_path)

    # Создаем резервную копию исходного файла
    backup_path = input_path + '.bak'
    shutil.copyfile(input_path, backup_path)
    print(f"Backup created at: {backup_path}")

    tree = ET.parse(input_path)
    root = tree.getroot()

    # Создаем новые деревья XML для strings.xml и string_arrays.xml
    strings_root = ET.Element("resources")
    string_arrays_root = ET.Element("resources")

    for string_array in root.findall('string-array'):
        array_name = string_array.get('name')
        new_array = ET.SubElement(string_arrays_root, 'string-array', {'name': array_name})

        for i, item in enumerate(string_array):
            new_string_name = f"{prefix}{array_name}_{i}"
            new_string = ET.SubElement(strings_root, 'string', {'name': new_string_name})
            new_string.text = item.text

            new_item = ET.SubElement(new_array, 'item')
            new_item.text = f"@string/{new_string_name}"

    # Запись обновленных XML файлов с форматированием
    strings_output_path = os.path.join(input_dir, 'strings.xml')
    string_arrays_output_path = os.path.join(input_dir, 'string_arrays.xml')

    with open(strings_output_path, "w", encoding='utf-8') as f:
        f.write(prettify_xml(strings_root))

    with open(string_arrays_output_path, "w", encoding='utf-8') as f:
        f.write(prettify_xml(string_arrays_root))

    print(f"Files created: {strings_output_path}, {string_arrays_output_path}")

def main():
    parser = argparse.ArgumentParser(description='Transform string-arrays to individual strings with references, create a backup, and format XML output.')
    parser.add_argument('-i', '--input', help='Input XML file', default='arrays.xml')
    parser.add_argument('-p', '--prefix', help='Prefix for string names', default='')
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)

    if os.path.isfile(input_path):
        print('Processing file:', input_path)
        process_file(input_path, args.prefix)
    else:
        print('Input file does not exist:', input_path)
        exit(1)

if __name__ == "__main__":
    main()
