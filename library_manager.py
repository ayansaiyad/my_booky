# My Booky (Backend & CLI)
# -----------------------
# This file contains the core logic for the My Booky app.
# Features:
# - Manage your personal book collection (add, view, search, delete, save/load)
# - Object-Oriented Design (Book, Library classes)
# - Data is stored in a JSON file with auto-save functionality
# - Ready for both GUI (Tkinter) and CLI usage
# - Includes exception handling and clear, maintainable code

import os
import json

DEFAULT_FILE = 'library.json'

class Book:
    def __init__(self, title, author, year, isbn):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'isbn': self.isbn
        }

    @staticmethod
    def from_dict(data):
        return Book(data['title'], data['author'], data['year'], data['isbn'])

    def __str__(self):
        return f"{self.title} | {self.author} | {self.year} | {self.isbn}"

class Library:
    def __init__(self, filename=DEFAULT_FILE):
        self.books = []
        self.filename = filename
        self.load_from_file()

    def add_book(self, book):
        self.books.append(book)
        print("Book added successfully in My Booky!\n")
        self.auto_save()

    def view_books(self):
        if not self.books:
            print("No books in My Booky.\n")
            return
        print("\nAll Books in My Booky:")
        for idx, book in enumerate(self.books, 1):
            print(f"{idx}. {book}")
        print()

    def search_books(self, keyword=None, year=None, isbn=None):
        results = self.books
        if keyword:
            results = [b for b in results if keyword.lower() in b.title.lower() or keyword.lower() in b.author.lower()]
        if year:
            results = [b for b in results if str(b.year) == str(year)]
        if isbn:
            results = [b for b in results if b.isbn == isbn]
        if not results:
            print("No matching books found in My Booky.\n")
        else:
            print("\nSearch Results in My Booky:")
            for book in results:
                print(book)
            print()
        return results

    def delete_book(self, idx):
        try:
            removed = self.books.pop(idx-1)
            print(f"Deleted from My Booky: {removed}\n")
            self.auto_save()
        except IndexError:
            print("Invalid book number!\n")

    def save_to_file(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([b.to_dict() for b in self.books], f, indent=2)
            print(f"My Booky saved to {self.filename}\n")
        except Exception as e:
            print(f"Error saving file: {e}\n")

    def load_from_file(self):
        if not os.path.exists(self.filename):
            self.books = []
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.books = [Book.from_dict(b) for b in data]
            print(f"My Booky loaded from {self.filename}\n")
        except Exception as e:
            print(f"Error loading file: {e}\n")
            self.books = []

    def auto_save(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([b.to_dict() for b in self.books], f, indent=2)
        except Exception:
            pass  # Silent fail for auto-save

    def __del__(self):
        self.auto_save()

# CLI code abhi ke liye rakha hai, GUI ke liye backend ready hai

def menu():
    print("""
My Booky
--------
1. Add Book
2. View All Books
3. Search Book
4. Delete Book
5. Save My Booky
6. Load My Booky
7. Exit
""")

def main():
    library = Library()
    while True:
        menu()
        choice = input("Enter your choice (1-7): ")
        if choice == '1':
            title = input("Book Title: ")
            author = input("Author: ")
            year = input("Year: ")
            isbn = input("ISBN: ")
            library.add_book(Book(title, author, year, isbn))
        elif choice == '2':
            library.view_books()
        elif choice == '3':
            keyword = input("Enter title/author (leave blank to skip): ").strip()
            year = input("Enter year (leave blank to skip): ").strip()
            isbn = input("Enter ISBN (leave blank to skip): ").strip()
            year = year if year else None
            isbn = isbn if isbn else None
            keyword = keyword if keyword else None
            library.search_books(keyword, year, isbn)
        elif choice == '4':
            library.view_books()
            try:
                idx = int(input("Enter book number to delete: "))
                library.delete_book(idx)
            except ValueError:
                print("Please enter a valid number!\n")
        elif choice == '5':
            library.save_to_file()
        elif choice == '6':
            library.load_from_file()
        elif choice == '7':
            print("Goodbye from My Booky!")
            break
        else:
            print("Invalid choice! Please try again.\n")

if __name__ == "__main__":
    main() 