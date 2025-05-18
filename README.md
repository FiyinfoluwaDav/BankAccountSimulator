# Fiyinfoluwa Microfinance Bank  
🏦 A GUI Banking System with Tkinter (Python)  

A secure, object-oriented banking application with GUI interface that manages customer accounts, transactions, and data persistence using JSON.  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)  
![OOP](https://img.shields.io/badge/Design-Object_Oriented-orange)  

---

## Key Features  
✅ **Account Management**  
- Create, login, recover, and delete accounts  
- Stores active accounts in `active_accounts.json` and deleted accounts in `deleted_accounts.json`  

✅ **Transactions**  
- Deposit and withdraw funds with password confirmation  
- Real-time balance validation (prevents overdrafts)  

✅ **Security**  
- Password-protected operations (with masking `****`)  
- Separate databases for active/deleted accounts  

✅ **User-Friendly GUI**  
- Clean Tkinter interface with color-coded buttons  
- Responsive error handling (pop-up messages)  

---

## Installation  
1. **Clone the repository**:  
   ```bash
   git clone https://github.com/FiyinfoluwaDav/Fiyinfoluwa-Microfinance-Bank.git
   cd Fiyinfoluwa-Microfinance-Bank

2. **Run the application**:
   ```bash
   Python L1Q4_app.py

3. **Code Structure**
   ```bash   
    ├── L1Q4_app.py             # Entry point
    ├── active_accounts.json    # Active accounts database
    ├── deleted_accounts.json   # Deleted accounts archive
    └── README.md
