from pathlib import Path
import shutil


def parse_report(report_path):
    report_path = Path(report_path)

    if not report_path.exists():
        raise FileNotFoundError(f"Report file not found: {report_path}")

    move_records = []

    with open(report_path, "r", encoding="utf-8") as report_file:
        for line in report_file:
            line = line.strip()

            if " -> " in line:
                original_path, moved_path = line.split(" -> ", 1)
                move_records.append((Path(original_path), Path(moved_path)))

    return move_records


def restore_files(move_records):
    restored_files = []
    skipped_files = []

    for original_path, moved_path in move_records:
        if not moved_path.exists():
            skipped_files.append((original_path, moved_path, "Moved file not found"))
            continue

        if original_path.exists():
            skipped_files.append((original_path, moved_path, "Original path already exists"))
            continue

        original_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(moved_path), str(original_path))
        restored_files.append((original_path, moved_path))

    return restored_files, skipped_files
