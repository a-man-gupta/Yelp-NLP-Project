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

// --- Business Search ---
app.get("/api/businesses", (req, res) => {
  const query = req.query.query || "";
  const sql = `
    SELECT b.business_id, b.name, b.address
    FROM business_fts fts
    JOIN business b ON b.rowid = fts.rowid
    WHERE fts.name MATCH ?
    LIMIT 10
  `;
  businessDB.all(sql, [query + "*"], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(rows);
  });
});

// --- User Search ---
app.get("/api/users", (req, res) => {
  const { query } = req.query;
  const sql = `SELECT user_id, name, review_count FROM user WHERE name LIKE ? LIMIT 10`;
  usersDB.all(sql, [`%${query}%`], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// --- Get Reviews for a Business ---
app.get("/api/reviews/:businessId", (req, res) => {
  const { businessId } = req.params;
  const sql = `SELECT review_id, text, stars, useful, funny, cool FROM review WHERE business_id = ? LIMIT 5`;
  reviewsDB.all(sql, [businessId], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// --- Get User Details ---
app.get("/api/user/:userId", (req, res) => {
  const { userId } = req.params;
  const sql = `SELECT name, review_count, yelping_since, useful, funny, cool, elite FROM user WHERE user_id = ?`;
  usersDB.get(sql, [userId], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(row);
  });
});

// --- Start Server ---
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
