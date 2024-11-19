import mysql.connector as mandu

man = mandu.connect(
    host="localhost",
    user="root",
    password="mandu",
    database="quiz_db"
)

cursor = man.cursor()

def setup_database():
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question TEXT NOT NULL,
        option1 VARCHAR(50),
        option2 VARCHAR(50),
        option3 VARCHAR(50),
        option4 VARCHAR(50),
        answer VARCHAR(50),
        topic VARCHAR(50) NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        score INT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Add 20 questions for each topic
    questions = [
        # Python Questions
        ("What is the correct file extension for Python files?", ".python", ".py", ".pyt", ".txt", ".py", "Python"),
        ("Which function is used to get the length of a list in Python?", "size()", "len()", "length()", "count()", "len()", "Python"),
        ("What is the output of print(type(5))?", "<class 'int'>", "<class 'float'>", "<class 'number'>", "int", "<class 'int'>", "Python"),
        ("What does // operator do in Python?", "Division", "Floor Division", "Modulus", "Power", "Floor Division", "Python"),
        ("Which keyword is used to define a function in Python?", "define", "def", "function", "func", "def", "Python"),
        ("How do you start a block of code in Python?", "Using {}", "Using indentation", "Using ()", "Using ;", "Using indentation", "Python"),
        ("What is the default data type for numbers in Python?", "int", "float", "complex", "str", "int", "Python"),
        ("Which of the following is not a core data type in Python?", "List", "Tuple", "Class", "Dictionary", "Class", "Python"),
        ("What is the output of print(2 ** 3)?", "6", "8", "9", "Error", "8", "Python"),
        ("Which method is used to add an element to a list in Python?", "append()", "add()", "push()", "insert()", "append()", "Python"),
        ("Which of the following is immutable in Python?", "List", "Dictionary", "Set", "Tuple", "Tuple", "Python"),
        ("How do you comment a single line in Python?", "//", "#", "/* */", "--", "#", "Python"),
        ("What does the len() function return?", "Size of a variable", "Number of items in an object", "Data type of an object", "Type of a variable", "Number of items in an object", "Python"),
        ("Which of the following is a valid variable name in Python?", "1variable", "_variable", "variable-name", "variable name", "_variable", "Python"),
        ("What is the output of print(10 / 3)?", "3", "3.33", "3.0", "3.333...", "3.333...", "Python"),
        ("What is the purpose of the 'with' keyword in Python?", "Looping", "Managing context", "Error handling", "String formatting", "Managing context", "Python"),
        ("What is the output of print('Hello' + 'World')?", "HelloWorld", "Hello World", "Error", "None", "HelloWorld", "Python"),
        ("Which of the following is used to handle exceptions in Python?", "try-catch", "try-except", "try-finally", "try-catch-finally", "try-except", "Python"),
        ("What is the default value of an integer in Python?", "0", "None", "Undefined", "-1", "0", "Python"),
        ("What is the output of print(bool(0))?", "True", "False", "Error", "None", "False", "Python"),

        # RDBMS Questions
        ("What does SQL stand for?", "Structured Query Language", "Simple Query Language", "Standard Query Language", "None", "Structured Query Language", "RDBMS"),
        ("Which command is used to retrieve data from a database?", "SELECT", "INSERT", "DELETE", "UPDATE", "SELECT", "RDBMS"),
        ("What is the primary key in a database?", "Unique identifier", "Column name", "Data type", "Index", "Unique identifier", "RDBMS"),
        ("Which keyword is used to sort data in ascending order?", "ASC", "DESC", "ORDER", "GROUP", "ASC", "RDBMS"),
        ("What is a foreign key?", "A unique column", "A reference to another table", "A column with no data", "None of the above", "A reference to another table", "RDBMS"),
        # (add more RDBMS and JavaScript questions as per need)
    ]

    # Insert questions
    cursor.executemany("""
    INSERT INTO questions (question, option1, option2, option3, option4, answer, topic)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, questions)

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        man.commit()
        print("Registration successful!")
    except mandu.errors.IntegrityError:
        print("Username already exists. Please try again.")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        return user[0]
    else:
        print("Invalid credentials. Please try again.")
        return None

def take_quiz(user_id):
    topic = input("Choose a topic (Python, RDBMS, JavaScript): ")
    cursor.execute("SELECT question, option1, option2, option3, option4, answer FROM questions WHERE topic = %s ORDER BY RAND() LIMIT 5", (topic,))
    questions = cursor.fetchall()

    if not questions:
        print("No questions available for the chosen topic.")
        return

    score = 0
    for question, option1, option2, option3, option4, answer in questions:
        print("\n" + question)
        print(f"A. {option1}\nB. {option2}\nC. {option3}\nD. {option4}")
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        if user_answer == "A" and option1 == answer:
            score += 1
        elif user_answer == "B" and option2 == answer:
            score += 1
        elif user_answer == "C" and option3 == answer:
            score += 1
        elif user_answer == "D" and option4 == answer:
            score += 1

    print(f"\nYou scored {score}/5.")
    cursor.execute("INSERT INTO scores (user_id, score) VALUES (%s, %s)", (user_id, score))
    man.commit()

# Initialize database
setup_database()

# Menu
while True:
    print("\n1. Register\n2. Login\n3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        register()
    elif choice == "2":
        user_id = login()
        if user_id:
            take_quiz(user_id)
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
