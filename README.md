

# 📘 JapanVerse

### An Object-Oriented In-Memory Database Project (Python)

> A student-level project that simulates a small database engine using **pure Python**, focused on **Object-Oriented Programming**, **Inheritance**, and **Functional Programming** — without using any external libraries.

---

## 🎯 Project Overview

**JapanVerse** is a Python project that models a mini knowledge base about **Japan**, including:

* 🎌 Anime & Japanese TV Dramas
* 🤖 Japanese Technology, Companies, and Gadgets
* 🔗 Relationships between media and technology (graph-based)

Instead of using ready-made databases (SQLite, JSON, ORM, etc.), the project **builds its own in-memory database engine** using Python classes.

This project is designed for **students** who want to deeply understand:

* How data can be structured internally
* How OOP and inheritance are used in real systems
* How querying and indexing concepts work under the hood

---

## 🧠 Key Concepts Implemented

### 🔹 Object-Oriented Programming (OOP)

* Base class: `Entity`
* Multi-level inheritance:

  * `Entity → Media → Anime / Drama`
  * `Entity → Tech → Company / Gadget`
* Shared behavior in parent classes, specialized behavior in child classes

### 🔹 In-Memory Database Engine

* Custom `Table` class (like a database table)
* Primary Key enforcement
* Insert / Update / Delete operations
* Operation history logging
* Manual indexing system for faster lookups

### 🔹 Graph Relationships

* `Link` entities represent relationships between records
* Supports directional relationships (`in`, `out`, `both`)
* Enables recommendation and related-entity queries

### 🔹 Functional Programming

Used **meaningfully**, not decoratively:

* `map()` for transformations
* `filter()` for querying
* `reduce()` for aggregations (e.g. averages)
* Generator-based iteration for streaming results

### 🔹 No External Libraries

* ❌ No SQLite
* ❌ No Pandas
* ❌ No JSON
* ✅ Pure Python only

---

## 🗂 Project Structure (Conceptual)

```
JapanVerse
│
├── Entity (base class)
│   ├── Media
│   │   ├── Anime
│   │   └── Drama
│   └── Tech
│       ├── Company
│       └── Gadget
│
├── Table (in-memory DB table)
├── Index (manual indexing system)
├── Link (graph relationships)
└── CLI Interface
```

---

## 🚀 How to Run

1. Make sure Python **3.10+** is installed
2. Save the file as `japanverse.py`
3. Run in terminal:

```bash
python japanverse.py
```

You will see an interactive CLI menu to explore the database.

---

## 🧪 Example Features You Can Test

* List all anime and dramas
* Search entities by name
* Get top anime by binge score
* Compute average ratings per studio
* Explore graph relationships
* Get recommendations based on tags

---

## 🎓 Educational Value

This project is ideal for:

* Computer Science students
* Python OOP courses
* Data Structures fundamentals
* Understanding how databases *actually* work internally

It goes **beyond typical CRUD assignments** by combining:

* Architecture
* Clean inheritance
* Query logic
* Data validation
* Performance awareness

---

## 🔧 Possible Extensions (Future Work)

* Save/load database to file (custom format)
* Foreign key constraints for relationships
* Query DSL (chainable queries)
* Ranking & recommendation improvements

---

## ✍️ Author Note

This project was built as a **learning-focused system**, prioritizing clarity, structure, and correctness over shortcuts.

---

---
