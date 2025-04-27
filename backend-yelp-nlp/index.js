const express = require("express");
const cors = require("cors");
const sqlite3 = require("sqlite3").verbose();
const path = require("path");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

// SQLite database paths
const businessDB = new sqlite3.Database(path.join(__dirname, "../databases/business_data.db"));
const reviewsDB = new sqlite3.Database(path.join(__dirname, "../databases/reviews_data.db"));
const usersDB = new sqlite3.Database(path.join(__dirname, "../databases/users_data.db"));

// --- Business Search (Updated for Pagination) ---
app.get("/api/businesses", (req, res) => {
  const query = req.query.query || "";
  const page = parseInt(req.query.page) || 1; // Default page is 1
  const limit = parseInt(req.query.limit) || 5; // Default limit is 10
  
  const offset = (page - 1) * limit;
  
  const sql = `
    SELECT b.business_id, b.name, b.address
    FROM business_fts fts
    JOIN business b ON b.rowid = fts.rowid
    WHERE fts.name MATCH ?
    LIMIT ? OFFSET ?
  `;
  businessDB.all(sql, [query + "*", limit, offset], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(rows);
  });
});

// --- User Search (Updated for Pagination) ---
app.get("/api/users", (req, res) => {
  const query = req.query.query || "";
  const page = parseInt(req.query.page) || 1; // Default page is 1
  const limit = parseInt(req.query.limit) || 10; // Default limit is 10
  
  const offset = (page - 1) * limit;
  
  const sql = `
    SELECT u.user_id, u.name, u.review_count
    FROM users_fts fts
    JOIN user u ON u.rowid = fts.rowid
    WHERE fts.name MATCH ?
    LIMIT ? OFFSET ?
  `;
  usersDB.all(sql, [query + "*", limit, offset], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(rows);
  });
});


// --- Start Server ---
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
