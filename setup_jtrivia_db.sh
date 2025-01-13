#!/bin/zsh
# Define the database file name
DB_NAME="jtrivia.db"
# Remove the database file if it exists
if [ -f "$DB_NAME" ]; then
    echo "Removing existing database: $DB_NAME."
    rm "$DB_NAME"
fi

# Create a new SQLite database and tables
echo "Creating new database: $DB_NAME."
sqlite3 "$DB_NAME" <<EOF

-- Create the Seasons table
CREATE TABLE IF NOT EXISTS Seasons (
    season_id INTEGER PRIMARY KEY AUTOINCREMENT,
    season_number INTEGER NOT NULL UNIQUE
);

-- Create the Webrefs table
CREATE TABLE IF NOT EXISTS Webrefs (
    webref_id INTEGER PRIMARY KEY AUTOINCREMENT,
    webref INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    FOREIGN KEY (season_id) REFERENCES Seasons(season_id) ON DELETE CASCADE
);

-- Create the Showinfo table
CREATE TABLE IF NOT EXISTS Showinfo (
    showinfo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_number INTEGER NOT NULL UNIQUE,
    web_id_number INTEGER NOT NULL UNIQUE,
    show_date DATE NOT NULL,
    show_comments TEXT
);


-- Create the Questions table
CREATE TABLE IF NOT EXISTS Questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    difficulty_id INTEGER NOT NULL,  
    category_id INTEGER NOT NULL,  
    showinfo_id INTEGER NOT NULL,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (showinfo_id) REFERENCES Showinfo(showinfo_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
    
);

-- Create the Answers table
CREATE TABLE IF NOT EXISTS Answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    answer_text TEXT NOT NULL,
    question_id INTEGER NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE

);

-- Create the Categories table
CREATE TABLE IF NOT EXISTS Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
);

-- Create the Difficulties table
CREATE TABLE IF NOT EXISTS Difficulties (
    difficulty_id INTEGER PRIMARY KEY AUTOINCREMENT,
    difficulty_level TEXT NOT NULL UNIQUE
);

EOF
echo "Database and tables created successfully."