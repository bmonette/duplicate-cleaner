from pathlib import Path
from datetime import datetime


def calculate_total_size(moved_files):
    total_size = 0

    for _, destination_path in moved_files:
        total_size += destination_path.stat().st_size

    return total_size


def format_size(size_in_bytes):
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_in_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024


def generate_report(root_path, total_files_scanned, duplicate_groups, moved_files, review_folder):
    root_path = Path(root_path)
    review_folder = Path(review_folder)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = root_path / f"duplicate_report_{timestamp}.txt"

    total_moved = len(moved_files)
    total_space_recovered = calculate_total_size(moved_files)
    formatted_space = format_size(total_space_recovered)

    report_lines = [
        "Duplicate File Cleaner Report",
        "=============================",
        f"Scan date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Scanned folder: {root_path}",
        f"Review folder: {review_folder}",
        "",
        "Summary",
        "-------",
        f"Files scanned: {total_files_scanned}",
        f"Duplicate groups found: {len(duplicate_groups)}",
        f"Duplicate files moved: {total_moved}",
        f"Space recovered: {formatted_space}",
        "",
        "Moved Files",
        "-----------",
    ]

    for original_path, destination_path in moved_files:
        report_lines.append(f"{original_path} -> {destination_path}")

    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write("\n".join(report_lines))

    return report_path


if __name__ == "__main__":
    from scanner import scan_folder
    from deduplicator import find_duplicates
    from mover import move_duplicates

    folder = input("Enter folder to scan: ")

    files = scan_folder(folder)
    duplicates = find_duplicates(files)

    if not duplicates:
        print("No duplicates found.")
    else:
        review_folder, moved_files = move_duplicates(duplicates, folder)

        report_path = generate_report(
            root_path=folder,
            total_files_scanned=len(files),
            duplicate_groups=duplicates,
            moved_files=moved_files,
            review_folder=review_folder
        )

        print(f"Report created: {report_path}")