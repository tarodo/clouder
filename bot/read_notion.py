import uuid
from zipfile import ZipFile
from pathlib import Path


def handle_release_file_from_zip(tmp_dir: str, release_file: str) -> dict:
    zip_file_path = Path(tmp_dir, release_file)
    new_dir_path = Path(tmp_dir, str(uuid.uuid4()))
    new_dir_path.mkdir()

    with ZipFile(zip_file_path) as myzip:
        myzip.extractall(new_dir_path)

    for one_file in new_dir_path.iterdir():
        if not one_file.is_file():
            continue
        if one_file.suffix != ".md":
            continue
        with open(one_file, "r") as file_release:
            release_links = {}
            for line in file_release:
                if ": " not in line:
                    continue
                line_data = line.split(": ")
                if len(line_data) != 2:
                    continue
                if not line_data[1].startswith("http"):
                    continue
                release_links[line_data[0]] = line_data[1].strip()
            break
    return release_links
