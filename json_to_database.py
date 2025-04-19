import json
import sqlite3

# Load the JSON file
with open('vulnerabilities.json') as f:
    data = json.load(f)

# Get the list of vulnerabilities
vulnerabilities = data["vulnerabilities"]

# Connect to the database
conn = sqlite3.connect('vulnerabilities.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vulnerabilities (
        name TEXT,
        affected_versions TEXT,
        cve TEXT
    )
''')

# Insert data
for vuln in vulnerabilities:
    name = vuln.get("name", "")
    affected_versions = ', '.join(vuln.get("affected_versions", []))
    cve = ', '.join(vuln.get("cve", []))
    print(f"inserting : {name}, affected_version: {affected_versions} CVE : {cve}")
    cursor.execute('''
        INSERT INTO vulnerabilities (name, affected_versions, cve)
        VALUES (?, ?, ?)
    ''', (name, affected_versions, cve))

conn.commit()
conn.close()

