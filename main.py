
import os
import re
import sys

def main() -> int:
    print(
"""
This script converts any files with extension cue to common text: (Track number). (Title) - (Artist)
This script assumes that file has TRACK, TITLE and PERFORMER fields.
"""
    )

    for cue_file_name in return_all_file_names_with_cue_extension():
        text_from_cue_file = return_text_from_file_by_file_name(cue_file_name)
        if (not text_from_cue_file):
            print(f"File {text_from_cue_file} is empty")

        text_to_save = convert_text_from_cue_to_txt(text_from_cue_file)
        save_text_to_file(cue_file_name, text_to_save)

    return 0

def return_all_file_names_with_cue_extension() -> list[str]:
    file_names:list[str] = []

    for file_name in os.listdir("."):
        if file_name.endswith(".cue"):
            file_names.append(file_name)

    return file_names

def return_text_from_file_by_file_name(file_name: str) -> str:
    if not os.path.isfile(file_name):
        print(f"File {file_name} does not exist")
        return ""

    f = open(file_name, "r")
    temp = f.readlines()
    f.close()

    return temp

def convert_text_from_cue_to_txt(text_from_cue_file: str) -> str:
    simplified_text :str = ""

    for line in text_from_cue_file:
        line = line.replace("\n", "")
        line = line.strip()
        if line.startswith("TRACK"):
            simplified_text +=  f"{ re.search('TRACK(.*)AUDIO', line).group(1).replace(" ", "")}. "
        if line.startswith("TITLE"):
            simplified_text += f"{ line.lstrip("TITLE").strip()[1:-1]} - " # remove TITLE and quotes([1:-1])
        elif line.startswith("PERFORMER"):
            simplified_text += f"{ line.lstrip("PERFORMER").strip()[1:-1]}\n" # remove PERFORMER and quotes([1:-1])
    return simplified_text

def save_text_to_file(original_file_name: str, text_to_save: str):
    file_name_for_saving = original_file_name.replace(".cue", ".txt")

    if os.path.isfile(file_name_for_saving):
        print(f"File {file_name_for_saving} exists")
        return

    f = open(file_name_for_saving, "w")
    f.write(text_to_save)
    f.close()

    print(f"File {original_file_name} is converted to {file_name_for_saving}")

if __name__ == '__main__':
    sys.exit(main())
