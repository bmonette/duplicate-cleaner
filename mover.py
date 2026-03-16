from pathlib import Path
from datetime import datetime
import shutil


def create_review_folder(root_path):
    root = Path(root_path)
    folder_name = f"Duplicate_Review_{datetime.now().strftime('%Y-%m-%d')}"
    review_folder = root / folder_name
    review_folder.mkdir(exist_ok=True)
    return review_folder


def get_unique_destination(destination_path):
    destination_path = Path(destination_path)

    if not destination_path.exists():
        return destination_path

    stem = destination_path.stem
    suffix = destination_path.suffix
    parent = destination_path.parent
    counter = 1

    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1


def move_duplicates(duplicate_groups, root_path):
    review_folder = create_review_folder(root_path)
    moved_files = []

    for group in duplicate_groups:
        duplicates_to_move = group[1:]

        for file_path in duplicates_to_move:
            destination = review_folder / file_path.name
            destination = get_unique_destination(destination)

            shutil.move(str(file_path), str(destination))
            moved_files.append((file_path, destination))

    return review_folder, moved_files
