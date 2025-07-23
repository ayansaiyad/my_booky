# My Booky - Tkinter GUI Version
# This GUI lets you view, add, search, and delete your books.
# Uses the Library class as backend (JSON, auto-save).

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from library_manager import Library, Book
import datetime

class InputDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt, position=None):
        super().__init__(parent)
        self.title(title)
        # Set custom icon for the dialog
        try:
            self.iconbitmap("my_booky.ico")
        except Exception:
            pass
        self.resizable(False, False)
        self.value = None
        self.grab_set()
        self.focus_force()
        tk.Label(self, text=prompt).pack(padx=10, pady=(10, 0))
        self.entry = tk.Entry(self, width=30)
        self.entry.pack(padx=10, pady=10)
        self.entry.focus_set()
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=(0, 10))
        tk.Button(btn_frame, text="OK", width=10, command=self.on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", width=10, command=self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Return>", lambda event: self.on_ok())
        self.bind("<Escape>", lambda event: self.on_cancel())
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.transient(parent)
        # Set geometry if position is given
        self._last_position = None
        self.update_idletasks()
        if position:
            self.geometry(f"+{position[0]}+{position[1]}")
        self.wait_window()
    def on_ok(self):
        self.value = self.entry.get()
        self._last_position = (self.winfo_x(), self.winfo_y())
        self.destroy()
    def on_cancel(self):
        self.value = None
        self._last_position = (self.winfo_x(), self.winfo_y())
        self.destroy()

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        # Set the correct window title
        self.root.title("My Booky")
        # Set the window icon (.ico file must be in the same folder)
        try:
            self.root.iconbitmap("my_booky.ico")
        except Exception:
            pass  # If icon is missing or invalid, app will still run
        self.library = Library()
        self.last_dialog_pos = None  # Remember last dialog position
        self.create_widgets()
        self.populate_table(self.library.books)

    def get_dialog_value(self, title, prompt):
        dlg = InputDialog(self.root, title, prompt, position=self.last_dialog_pos)
        # Update last position if dialog was moved
        if hasattr(dlg, '_last_position') and dlg._last_position:
            self.last_dialog_pos = dlg._last_position
        return dlg.value

    def create_widgets(self):
        # Table (Treeview)
        columns = ("Title", "Author", "Year", "ISBN")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Add Book Button
        add_btn = ttk.Button(self.root, text="Add Book", command=self.add_book_dialog)
        add_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Search Book Button
        search_btn = ttk.Button(self.root, text="Search", command=self.search_dialog)
        search_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Delete Book Button
        del_btn = ttk.Button(self.root, text="Delete Selected", command=self.delete_selected)
        del_btn.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Show All Button
        showall_btn = ttk.Button(self.root, text="Show All", command=self.show_all)
        showall_btn.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Status Label
        self.status = tk.Label(self.root, text="Welcome to My Booky!", anchor="w")
        self.status.grid(row=2, column=0, columnspan=4, sticky="ew", padx=10, pady=(0,10))

    def populate_table(self, books):
        # Clear the table
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Show all books
        for book in books:
            self.tree.insert("", "end", values=(book.title, book.author, book.year, book.isbn))

    def add_book_dialog(self):
        # Use custom input dialogs for all fields, no validation
        title = self.get_dialog_value("Book Title", "Enter book title:")
        if not title:
            self.set_status("Title is required.")
            return
        author = self.get_dialog_value("Author", "Enter author name:") or ""
        year = self.get_dialog_value("Year", "Enter year (e.g. 2024):") or ""
        isbn = self.get_dialog_value("ISBN", "Enter ISBN number (optional):") or ""
        book = Book(title.strip(), author.strip(), year.strip(), isbn.strip())
        self.library.add_book(book)
        self.populate_table(self.library.books)
        self.set_status(f"Book '{title}' added to My Booky!")

    def search_dialog(self):
        # Use custom input dialogs for all fields
        keyword = self.get_dialog_value("Search", "Title/Author (optional):")
        year = self.get_dialog_value("Search", "Year (optional):")
        isbn = self.get_dialog_value("Search", "ISBN (optional):")
        results = self.library.search_books(keyword or None, year or None, isbn or None)
        self.populate_table(results)
        self.set_status(f"{len(results)} book(s) found in My Booky.")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            self.set_status("Please select a book to delete.")
            return
        idx = self.tree.index(selected[0])
        book = self.library.books[idx]
        confirm = messagebox.askyesno("Delete", f"Delete '{book.title}' from My Booky?")
        if confirm:
            self.library.delete_book(idx+1)
            self.populate_table(self.library.books)
            self.set_status(f"Book '{book.title}' deleted from My Booky.")

    def show_all(self):
        self.populate_table(self.library.books)
        self.set_status("All books are displayed (My Booky).")

    def set_status(self, msg):
        self.status.config(text=msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop() 