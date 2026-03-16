from collections import defaultdict
from hasher import calculate_hash


def group_files_by_hash(files):
    hash_map = defaultdict(list)

    for file in files:
        file_hash = calculate_hash(file)
        hash_map[file_hash].append(file)

    return hash_map


def find_duplicates(files):
    grouped = group_files_by_hash(files)

    duplicates = []

    for file_hash, file_list in grouped.items():
        if len(file_list) > 1:
            duplicates.append(file_list)

    return duplicates
