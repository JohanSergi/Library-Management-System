## 🧠 Advanced Odoo 14 Library Management System

This version of the system (found in `odoo_library_system/library_extended/`) is a refined implementation using deeper Odoo concepts:

### ✅ Features

- 📚 **Book Management** using `product.product` model for better inventory control
- 👥 **Member Management** extending `res.partner`
- 🔐 **Role-based Access Control**
  - **Librarian**: Full Access
  - **Staff Novel**: Limited to managing Novel genre books/transactions
  - **Staff Fantasy**: Limited to managing Fantasy genre books/transactions
- 🧾 **Transaction System**
  - Take Book / Return Book actions
  - Smart button in member view to access transactions
- 📅 **Due Tracking**
  - Automatically calculates due date 2 weeks from issue
  - Updates member’s `books_due` count
- 💸 **Fine System**
  - Calculates fine per day after due date
- 🧾 **PDF Report Generation**
  - Generates a downloadable QWeb-based receipt for every transaction

### 📦 Architecture Highlights

- `library.transaction`: Core model to handle issuing and returning books
- `transaction.line`: Tracks each book in a transaction
- Uses `virtual_available` to manage real-time book stock
- Fine logic is calculated on return based on overdue days

---

### 🔧 To Use

1. Place `library_extended` inside your custom addons path.
2. Update app list: **Apps → Update Apps List**
3. Search and install **Library Extended**
4. Log in as different users (with proper group assignment) to test role restrictions.

---
