import sqlite3

DB_FILE = "botzilla.db"

def save_link_data(url, title, category, tags):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS links (url TEXT, title TEXT, category TEXT, tags TEXT)")
    conn.execute("INSERT INTO links VALUES (?, ?, ?, ?)", (url, title, category, ",".join(tags)))
    conn.commit()
    conn.close()

def get_latest_links(n=5):
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("SELECT * FROM links ORDER BY rowid DESC LIMIT ?", (n,)).fetchall()
    conn.close()
    return [dict(zip(["url", "title", "category", "tags"], row)) for row in rows]

def get_links_by_tag(tag):
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("SELECT * FROM links WHERE tags LIKE ?", (f"%{tag}%",)).fetchall()
    conn.close()
    return [dict(zip(["url", "title", "category", "tags"], row)) for row in rows]
