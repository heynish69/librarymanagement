import csv
import hashlib
from datetime import datetime

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load books from CSV
def load_books():
    books = {}
    with open('books.csv', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books[row['book_id']] = {
                'title': row['title'],
                'author': row['author'],
                'available_copies': int(row['available_copies'])
            }
    return books

# Save books to CSV
def save_books(books):
    with open('books.csv', 'w', newline='') as file:
        fieldnames = ['book_id', 'title', 'author', 'available_copies']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for book_id, info in books.items():
            writer.writerow({
                'book_id': book_id,
                'title': info['title'],
                'author': info['author'],
                'available_copies': info['available_copies']
            })

# Load members from CSV
def load_members():
    members = {}
    with open('members.csv', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            members[row['member_id']] = {
                'name': row['name'],
                'password_hash': row['password_hash']
            }
    return members

# Login function
def login(members):
    member_id = input("Enter Member ID: ")
    password = input("Enter Password: ")
    if member_id in members:
        if hash_password(password) == members[member_id]['password_hash']:
            print(f"Welcome {members[member_id]['name']}!")
            return member_id
        else:
            print("Incorrect password!")
    else:
        print("Member ID not found!")
    return None

# Search books
def search_books(books):
    query = input("Enter book title or author to search: ").lower()
    found = False
    for book_id, info in books.items():
        if query in info['title'].lower() or query in info['author'].lower():
            print(f"ID: {book_id}, Title: {info['title']}, Author: {info['author']}, Available: {info['available_copies']}")
            found = True
    if not found:
        print("No books found.")

# Issue book
def issue_book(member_id, books):
    book_id = input("Enter Book ID to issue: ")
    if book_id in books:
        if books[book_id]['available_copies'] > 0:
            # Decrease available copies
            books[book_id]['available_copies'] -= 1
            # Save loan record
            with open('loans.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                loan_id = str(int(datetime.now().timestamp()))  # simple unique ID
                issue_date = datetime.now().strftime("%Y-%m-%d")
                writer.writerow([loan_id, book_id, member_id, issue_date, ''])
            save_books(books)
            print(f"Book '{books[book_id]['title']}' issued successfully!")
        else:
            print("Book not available right now.")
    else:
        print("Invalid Book ID.")

# Return book
def return_book(member_id, books):
    loan_id = input("Enter Loan ID to return: ")
    loans = []
    found = False
    with open('loans.csv', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            loans.append(row)
    for row in loans:
        if row[0] == loan_id and row[2] == member_id and row[4] == '':
            row[4] = datetime.now().strftime("%Y-%m-%d")
            books[row[1]]['available_copies'] += 1
            found = True
            break
    if found:
        with open('loans.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(loans)
        save_books(books)
        print("Book returned successfully!")
    else:
        print("Loan record not found or already returned.")

# Main program
def main():
    books = load_books()
    members = load_members()

    member_id = login(members)
    if not member_id:
        return

    while True:
        print("\n1. Search Books")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            search_books(books)
        elif choice == '2':
            issue_book(member_id, books)
        elif choice == '3':
            return_book(member_id, books)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__== "__main__":
    main()
