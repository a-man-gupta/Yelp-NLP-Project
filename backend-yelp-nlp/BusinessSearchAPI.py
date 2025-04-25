from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sqlite3
from contextlib import closing

app = FastAPI()
# uvicorn BusinessSearchAPI:app --reload

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/businesses")
def search_businesses(query: str = Query(..., min_length=1)) -> List[dict]:
    db_path = "../databases/business_data.db"
    with closing(sqlite3.connect(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT b.business_id, b.name, b.address
            FROM business_fts f
            JOIN business b ON b.rowid = f.rowid
            WHERE f.name MATCH ?
            LIMIT 10
        """, (query + '*',))  # FTS5 partial matching style

        results = cursor.fetchall()
        return [dict(row) for row in results]
