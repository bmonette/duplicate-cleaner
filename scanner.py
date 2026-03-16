from pathlib import Path


def should_skip_dir(dir_name):
    return dir_name.startswith("Duplicate_Review_")


def scan_folder(root_path):
    root = Path(root_path)

    if not root.exists():
        raise FileNotFoundError(f"Folder does not exist: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root}")

    files_found = []

    for item in root.iterdir():
        if item.is_dir():
            if should_skip_dir(item.name):
                continue

            files_found.extend(scan_folder(item))

        elif item.is_file():
            files_found.append(item)

    return files_found
