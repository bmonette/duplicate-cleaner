import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from scanner import scan_folder
from deduplicator import find_duplicates
from mover import move_duplicates
from report import generate_report
from restore import parse_report, restore_files


class DuplicateCleanerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Duplicate File Cleaner")
        self.geometry("800x500")
        self.resizable(True, True)

        self.cleanup_folder_var = tk.StringVar()
        self.restore_report_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")

        self._build_ui()

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.cleanup_tab = ttk.Frame(notebook)
        self.restore_tab = ttk.Frame(notebook)

        notebook.add(self.cleanup_tab, text="Cleanup")
        notebook.add(self.restore_tab, text="Restore")

        self._build_cleanup_tab()
        self._build_restore_tab()

        status_bar = ttk.Label(self, textvariable=self.status_var, anchor="w")
        status_bar.pack(fill="x", padx=10, pady=(0, 10))

    def _build_cleanup_tab(self):
        frame = ttk.Frame(self.cleanup_tab, padding=10)
        frame.pack(fill="both", expand=True)

        folder_label = ttk.Label(frame, text="Folder to scan:")
        folder_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        folder_entry = ttk.Entry(frame, textvariable=self.cleanup_folder_var, width=70)
        folder_entry.grid(row=1, column=0, sticky="ew", padx=(0, 5))

        browse_button = ttk.Button(frame, text="Browse", command=self.browse_cleanup_folder)
        browse_button.grid(row=1, column=1, sticky="ew")

        start_button = ttk.Button(frame, text="Scan and Move Duplicates", command=self.start_cleanup)
        start_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        self.progress_bar = ttk.Progressbar(frame, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.cleanup_results = tk.Text(frame, height=18, wrap="word")
        self.cleanup_results.grid(row=4, column=0, columnspan=2, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(4, weight=1)

    def _build_restore_tab(self):
        frame = ttk.Frame(self.restore_tab, padding=10)
        frame.pack(fill="both", expand=True)

        report_label = ttk.Label(frame, text="Report file:")
        report_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        report_entry = ttk.Entry(frame, textvariable=self.restore_report_var, width=70)
        report_entry.grid(row=1, column=0, sticky="ew", padx=(0, 5))

        browse_button = ttk.Button(frame, text="Browse", command=self.browse_restore_report)
        browse_button.grid(row=1, column=1, sticky="ew")

        restore_button = ttk.Button(frame, text="Restore Files", command=self.start_restore)
        restore_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        self.restore_results = tk.Text(frame, height=18, wrap="word")
        self.restore_results.grid(row=3, column=0, columnspan=2, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(3, weight=1)

    def browse_cleanup_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.cleanup_folder_var.set(folder)

    def browse_restore_report(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.restore_report_var.set(file_path)

    def set_cleanup_results(self, text):
        self.cleanup_results.delete("1.0", tk.END)
        self.cleanup_results.insert(tk.END, text)

    def set_restore_results(self, text):
        self.restore_results.delete("1.0", tk.END)
        self.restore_results.insert(tk.END, text)

    def update_progress(self, current, total, file_path):
        def _update():
            self.progress_bar["maximum"] = total
            self.progress_bar["value"] = current
            self.status_var.set(f"Hashing files: {current}/{total} - {file_path.name}")

        self.after(0, _update)

    def start_cleanup(self):
        folder = self.cleanup_folder_var.get().strip()

        if not folder:
            messagebox.showerror("Error", "Please select a folder to scan.")
            return

        self.progress_bar["value"] = 0
        self.set_cleanup_results("")
        self.status_var.set("Starting cleanup...")

        thread = threading.Thread(target=self.run_cleanup_task, args=(folder,), daemon=True)
        thread.start()

    def run_cleanup_task(self, folder):
        try:
            files = scan_folder(folder)
            duplicates = find_duplicates(files, progress_callback=self.update_progress)

            if not duplicates:
                self.after(0, lambda: self.set_cleanup_results("No duplicates found."))
                self.after(0, lambda: self.status_var.set("No duplicates found."))
                return

            review_folder, moved_files = move_duplicates(duplicates, folder)

            report_path = generate_report(
                root_path=folder,
                total_files_scanned=len(files),
                duplicate_groups=duplicates,
                moved_files=moved_files,
                review_folder=review_folder,
            )

            summary = (
                f"Files scanned: {len(files)}\n"
                f"Duplicate groups found: {len(duplicates)}\n"
                f"Duplicate files moved: {len(moved_files)}\n"
                f"Review folder: {review_folder}\n"
                f"Report created: {report_path}\n"
            )

            self.after(0, lambda: self.set_cleanup_results(summary))
            self.after(0, lambda: self.status_var.set("Cleanup completed successfully."))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.after(0, lambda: self.status_var.set("Cleanup failed."))

    def start_restore(self):
        report_path = self.restore_report_var.get().strip()

        if not report_path:
            messagebox.showerror("Error", "Please select a report file.")
            return

        self.set_restore_results("")
        self.status_var.set("Starting restore...")

        thread = threading.Thread(target=self.run_restore_task, args=(report_path,), daemon=True)
        thread.start()

    def run_restore_task(self, report_path):
        try:
            move_records = parse_report(report_path)
            restored_files, skipped_files = restore_files(move_records)

            summary_lines = [
                f"Files restored: {len(restored_files)}",
                f"Files skipped: {len(skipped_files)}",
                "",
            ]

            if restored_files:
                summary_lines.append("Restored files:")
                for original_path, moved_path in restored_files:
                    summary_lines.append(f"{moved_path} -> {original_path}")

            if skipped_files:
                summary_lines.append("")
                summary_lines.append("Skipped files:")
                for original_path, moved_path, reason in skipped_files:
                    summary_lines.append(f"{moved_path} -> {original_path} ({reason})")

            summary = "\n".join(summary_lines)

            self.after(0, lambda: self.set_restore_results(summary))
            self.after(0, lambda: self.status_var.set("Restore completed successfully."))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.after(0, lambda: self.status_var.set("Restore failed."))


if __name__ == "__main__":
    app = DuplicateCleanerApp()
    app.mainloop()
