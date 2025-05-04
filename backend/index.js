const express = require("express");
const cors = require("cors");
const sqlite3 = require("sqlite3").verbose();
const path = require("path");
const axios = require("axios"); // Added axios import

const app = express();
const PORT = 5000;

// Environment variables (optional, for flexibility)
const PYTHON_API_URL = process.env.PYTHON_API_URL || "http://localhost:8000";

app.use(cors());
app.use(express.json());

// SQLite database paths
const businessDB = new sqlite3.Database(path.join(__dirname, "../databases/business_data.db"));
const reviewsDB = new sqlite3.Database(path.join(__dirname, "../databases/reviews_data.db"));
const usersDB = new sqlite3.Database(path.join(__dirname, "../databases/users_data.db"));

// --- Business Search (Updated for Pagination) ---
app.get("/api/businesses", (req, res) => {
  const query = req.query.query || "";
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 5;
  
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
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  
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

// --- Proxy to Python Predict Ratings API ---
app.post("/api/predict-ratings", async (req, res) => {
  const { business_id, user_id, review_text } = req.body;
  if (!business_id || !user_id || !review_text) {
    return res.status(400).json({ error: "Missing required fields: business_id, user_id, review_text" });
  }
  try {
    const response = await axios.post(`${PYTHON_API_URL}/predict-ratings`, req.body);
    res.json(response.data);
  } catch (error) {
    console.error("Predict Ratings Error:", error.message); // Added logging
    res.status(500).json({ error: error.message });
  }
});

// --- Proxy to Python Generate Review API ---
app.post("/api/generate-review", async (req, res) => {
  const { business_id, user_id, helpful_text } = req.body;
  if (!business_id || !user_id || !helpful_text) {
    return res.status(400).json({ error: "Missing required fields: business_id, user_id, helpful_text" });
  }
  try {
    const response = await axios.post(`${PYTHON_API_URL}/generate-review`, req.body);
    res.json(response.data);
  } catch (error) {
    console.error("Generate Review Error:", error.message); // Added logging
    res.status(500).json({ error: error.message });
  }
});

// --- Start Server ---
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});