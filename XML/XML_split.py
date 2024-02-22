import os
import xml.etree.ElementTree as ET
import copy


def split_xml(input_folder, target_size):
    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            input_file_path = os.path.join(input_folder, filename)
            split_xml_file(input_file_path, target_size)


def split_xml_file(input_file_path, target_size):
    with open(input_file_path, 'rb') as f:
        tree = ET.parse(f)
        root = tree.getroot()

    total_size = os.path.getsize(input_file_path)
    chunk_size = min(target_size, total_size)

    chunks = []
    current_chunk = ET.Element(root.tag)
    current_size = 0

    for element in root:
        element_size = len(ET.tostring(element, encoding='utf-8'))

        if current_size + element_size <= chunk_size:
            current_chunk.append(copy.deepcopy(element))
            current_size += element_size
        else:
            chunks.append(current_chunk)
            current_chunk = ET.Element(root.tag)
            current_chunk.append(copy.deepcopy(element))
            current_size = element_size

    if len(current_chunk) > 0:
        chunks.append(current_chunk)

    output_folder = os.path.dirname(input_file_path)
    base_filename, extension = os.path.splitext(os.path.basename(input_file_path))

    for i, chunk in enumerate(chunks, start=1):
        output_filename = f"{base_filename}_{i}{extension}"
        output_file_path = os.path.join(output_folder, output_filename)

        # Creating a new ElementTree with the root and appending the chunk elements
        output_tree = ET.ElementTree(ET.Element(root.tag))
        output_tree.getroot().extend(chunk)

        with open(output_file_path, 'wb') as output_file:
            output_tree.write(output_file, encoding='utf-8')

        print(f"File {output_filename} created.")

input_folder = r"C:\Users\Loctimize\Downloads\Test"
target_size = 2000000  # Set your desired approximate target file
# size in bytes, 1 megabyte = 1 000 000 bytes

split_xml(input_folder, target_size)