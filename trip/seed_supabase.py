import os
from dotenv import load_dotenv
from supabase import create_client, Client
from werkzeug.security import generate_password_hash

load_dotenv(r"c:\Users\Anu Rajput\Downloads\trip\.env")
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

if not url or not key:
    print("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")
    exit(1)

sb: Client = create_client(url, key)

from seed_data import seed_all
import sqlite3

# Extract the seed data from a temporary in-memory sqlite db using the existing seeder
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
with open(r"c:\Users\Anu Rajput\Downloads\trip\schema.sql", "r", encoding="utf-8") as f:
    conn.executescript(f.read())
seed_all(conn)

print("In-memory SQLite populated from seed_data.py. Now pushing to Supabase...")

# 1. Push Users
users = [dict(row) for row in conn.execute("SELECT * FROM users").fetchall()]
try:
    res = sb.table("users").upsert(users, on_conflict="username").execute()
    print(f"Users synced: {len(res.data)}")
except Exception as e:
    print(f"Error syncing users: {e}")

# 2. Push Destinations
dests = [dict(row) for row in conn.execute("SELECT * FROM destinations").fetchall()]
try:
    res = sb.table("destinations").upsert(dests, on_conflict="id").execute()
    print(f"Destinations synced: {len(res.data)}")
except Exception as e:
    print(f"Error syncing destinations: {e}")

# 3. Push Religious Site Details
details = [dict(row) for row in conn.execute("SELECT * FROM religious_site_details").fetchall()]
try:
    res = sb.table("religious_site_details").upsert(details, on_conflict="destination_id").execute()
    print(f"Religious Site Details synced: {len(res.data)}")
except Exception as e:
    print(f"Error syncing religious site details: {e}")

# Try other tables if they exist
for table in ['circuits', 'festivals', 'hotels', 'restaurants', 'vehicles']:
    try:
        rows = [dict(row) for row in conn.execute(f"SELECT * FROM {table}").fetchall()]
        res = sb.table(table).upsert(rows, on_conflict="id").execute()
        print(f"Table '{table}' synced: {len(res.data)}")
    except Exception as e:
        print(f"Table '{table}' not yet created in Supabase: {e}")

conn.close()
print("Supabase seed sync finished!")
