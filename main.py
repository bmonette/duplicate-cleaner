from scanner import scan_folder
from deduplicator import find_duplicates
from mover import move_duplicates
from report import generate_report
from restore import parse_report, restore_files


def show_progress(current, total, file_path):
    percent = (current / total) * 100
    print(f"\rHashing files: {current}/{total} ({percent:.1f}%) - {file_path.name}", end="")


def run_duplicate_cleanup():
    folder = input("Enter the folder path to scan: ").strip()

    files = scan_folder(folder)
    duplicates = find_duplicates(files, progress_callback=show_progress)
    print()

    print(f"\nFiles scanned: {len(files)}")
    print(f"Duplicate groups found: {len(duplicates)}")

    if not duplicates:
        print("No duplicates found.")
        return

    review_folder, moved_files = move_duplicates(duplicates, folder)

    report_path = generate_report(
        root_path=folder,
        total_files_scanned=len(files),
        duplicate_groups=duplicates,
        moved_files=moved_files,
        review_folder=review_folder
    )

    print(f"\nReview folder created: {review_folder}")
    print(f"Duplicate files moved: {len(moved_files)}")
    print(f"Report created: {report_path}")


def run_restore():
    report_path = input("Enter the path to the report file: ").strip()

    move_records = parse_report(report_path)
    restored_files, skipped_files = restore_files(move_records)

    print(f"\nFiles restored: {len(restored_files)}")
    print(f"Files skipped: {len(skipped_files)}")

    if restored_files:
        print("\nRestored files:")
        for original_path, moved_path in restored_files:
            print(f"RESTORED: {moved_path} -> {original_path}")

    if skipped_files:
        print("\nSkipped files:")
        for original_path, moved_path, reason in skipped_files:
            print(f"SKIPPED: {moved_path} -> {original_path} ({reason})")


def main():
    while True:
        print("\nDuplicate File Cleaner")
        print("1. Scan and move duplicates")
        print("2. Restore files from report")
        print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            try:
                run_duplicate_cleanup()
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("\nPress Enter to continue...")

        elif choice == "2":
            try:
                run_restore()
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("\nPress Enter to continue...")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
