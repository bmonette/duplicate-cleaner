# Duplicate File Cleaner

Duplicate File Cleaner is a Python utility that scans folders for
**exact duplicate files** using SHA256 hashing, safely moves duplicate
copies to a review folder, and generates a detailed cleanup report.

It also includes a **full restore system**, allowing all moved files to
be returned to their original locations using the generated report.

The project includes both a **CLI interface** and a **Tkinter GUI**.

------------------------------------------------------------------------

## Features

-   Recursive folder scanning
-   Exact duplicate detection using **SHA256 hashing**
-   Safe duplicate isolation (duplicates are **moved**, not deleted)
-   Timestamped cleanup reports
-   Full **restore capability**
-   CLI interface
-   GUI interface with progress bar
-   Threaded processing (prevents UI freezing)
-   Detailed audit trail of all moved files

------------------------------------------------------------------------

## How It Works

1.  The program scans the selected folder recursively.
2.  Each file is hashed using **SHA256**.
3.  Files with identical hashes are grouped as duplicates.
4.  The first file is kept in place.
5.  Remaining duplicates are moved to:

```{=html}
<!-- -->
```
    Duplicate_Review_YYYY-MM-DD

6.  A report is generated containing:

-   Scan date
-   Files scanned
-   Duplicate groups
-   Files moved
-   Space recovered
-   Full move history

Example report file:

    duplicate_report_2026-03-16_15-34-32.txt

------------------------------------------------------------------------

## Restore System

The report contains all original file paths and moved file paths.

Using the restore function:

1.  The report file is read.
2.  Each move operation is reversed.
3.  Files are returned to their original locations.

This ensures the cleanup process is **fully reversible**.

------------------------------------------------------------------------

## Project Structure

    duplicate-cleaner/
    │
    ├── scanner.py
    ├── hasher.py
    ├── deduplicator.py
    ├── mover.py
    ├── report.py
    ├── restore.py
    ├── main.py
    │
    └── ui/
        └── app.py

### Module Overview

  Module            Purpose
  ----------------- ---------------------------------------------
  scanner.py        Recursively scans folders for files
  hasher.py         Generates SHA256 file hashes
  deduplicator.py   Groups files by hash and detects duplicates
  mover.py          Moves duplicate files safely
  report.py         Generates cleanup reports
  restore.py        Restores files from report
  main.py           CLI application
  ui/app.py         GUI application

------------------------------------------------------------------------

## Running the CLI Version

From the project root:

    python main.py

Menu:

    1. Scan and move duplicates
    2. Restore files from report
    3. Exit

------------------------------------------------------------------------

## Running the GUI Version

    python ui/app.py

The GUI provides:

-   Folder browser
-   Cleanup progress bar
-   Restore tab
-   Status messages
-   Results summary

------------------------------------------------------------------------

## Packaging as a Windows Executable

Install PyInstaller:

    pip install pyinstaller

Build executable:

    pyinstaller --onefile --windowed ui/app.py

The executable will appear in:

    dist/app.exe

You can rename it to:

    duplicate-file-cleaner.exe

------------------------------------------------------------------------

## Safety Design

This tool is designed to **avoid accidental data loss**.

Key safety mechanisms:

-   Files are **never deleted automatically**
-   Duplicates are moved to a **review folder**
-   A detailed **report file** is created
-   All actions can be **reversed using restore**

------------------------------------------------------------------------

## Example Use Cases

-   Cleaning duplicate photo libraries
-   Removing duplicate downloads
-   Organizing messy document folders
-   Preparing datasets
-   Cleaning backup directories
-   Fiverr file cleanup services

------------------------------------------------------------------------

## Future Improvements

Possible enhancements:

-   Smarter "file to keep" selection
-   Preview duplicate groups before moving
-   Similar image detection
-   Drag-and-drop GUI support
-   Disk usage visualization
-   Batch folder processing

------------------------------------------------------------------------

## License

This project is intended for educational and utility use.

Feel free to modify, extend, and improve it.
