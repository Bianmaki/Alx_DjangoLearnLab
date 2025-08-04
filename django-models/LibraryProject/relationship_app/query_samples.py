from relationship_app.models import Author, Book, Library, Librarian

author_name = "Author Name Here"
books_by_author = Book.objects.filter(author__name=author_name)
print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

library_name = "Library Name Here"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print(f"Books in {library_name}: {[book.title for book in books_in_library]}")

librarian_for_library = Librarian.objects.get(library__name=library_name)
print(f"Librarian for {librarian_name}: {librarian_for_library.name}")