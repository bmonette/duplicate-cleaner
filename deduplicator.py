from collections import defaultdict
from hasher import calculate_hash


def group_files_by_hash(files, progress_callback=None):
    hash_map = defaultdict(list)
    total_files = len(files)

    for index, file in enumerate(files, start=1):
        file_hash = calculate_hash(file)
        hash_map[file_hash].append(file)

        if progress_callback is not None:
            progress_callback(index, total_files, file)

    return hash_map


def find_duplicates(files, progress_callback=None):
    grouped = group_files_by_hash(files, progress_callback=progress_callback)

    duplicates = []

    for file_hash, file_list in grouped.items():
        if len(file_list) > 1:
            duplicates.append(file_list)

    return duplicates
