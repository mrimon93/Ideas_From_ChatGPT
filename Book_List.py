import pandas as pd
import psycopg2

# Ask the user for the database details
database_name = input("Enter the name of the PostgreSQL database to create: ")
user = input("Enter the PostgreSQL username: ")
password = input("Enter the PostgreSQL password: ")
host = input("Enter the PostgreSQL host: ")
port = input("Enter the PostgreSQL port: ")

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="postgres",
    user=user,
    password=password,
    host=host,
    port=port
)

# Create the database if it does not exist
cur = conn.cursor()
cur.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (database_name,))
exists = cur.fetchone()
if not exists:
    cur.execute(f"CREATE DATABASE {database_name};")
    conn.commit()

# Close the cursor and the connection to the default database
cur.close()
conn.close()

# Connect to the newly created database
conn = psycopg2.connect(
    database=database_name,
    user=user,
    password=password,
    host=host,
    port=port
)

# Create a table to store the book data
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        rating INTEGER
    );
""")
conn.commit()

# Ask the user for book details and store them in a list of dictionaries
books = []
while True:
    title = input("Enter the title of the book (or 'done' to exit): ")
    if title == "done":
        break
    author = input("Enter the author of the book: ")
    rating = int(input("Enter your rating of the book (1-10): "))
    book = {"title": title, "author": author, "rating": rating}
    books.append(book)

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(books)

# Print the DataFrame to a CSV file
df.to_csv("books.csv", index=False)

# Print the DataFrame to an Excel file
df.to_excel("books.xlsx", index=False)

# Insert the book data into the PostgreSQL database
for book in books:
    cur.execute("""
        INSERT INTO books (title, author, rating)
        VALUES (%s, %s, %s);
    """, (book["title"], book["author"], book["rating"]))
conn.commit()

# Close the database connection
cur.close()
conn.close()

