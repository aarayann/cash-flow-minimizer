# Cash Flow Minimizer

A full-stack web application to minimize cash flow among a group of individuals who have borrowed money from each other.  
Users can enter transactions with due dates, interest rates, and penalties.  
The app computes the minimum number of transactions needed to settle all debts, taking into account all constraints.

![Screenshot 2025-04-25 020958](https://github.com/user-attachments/assets/252d5522-db1d-4e2c-9b5f-b77a2f821239)

---

## Features

- **Add Transactions:** Input sender, receiver, amount, due date, interest rate, and penalty.
- **Transaction Table:** View all transactions with full details.
- **Cash Flow Minimization:** Calculate and display the minimal set of payments required to settle all debts.
- **Constraint Handling:** Supports due dates, per-day interest rates, and penalties for late payments.
- **Persistent Storage:** All transactions are stored in a Supabase database.
- **Modern Tech Stack:** FastAPI backend, React frontend, Supabase as database.


Features ||	Present in the App? ||	Notes
Input of all required fields ||	✅ ||	 All fields present in form
Display of all transactions ||	✅ ||	 Table shows all fields
Minimize cash flow logic ||	✅ || 	Settlement result shown
Handles due date, interest, penalty ||	✅ ||	 Reflected in settlement amount
User interface for input/output ||	✅ || 	Clean UI
Input validation ||	✅ || Required fields in form
Time series/chronological sorting ||	⚠️ || 	Due date present, not shown as timeline
Advanced algorithms (MCMF, DP, etc.) ||	 ⚠️ || 	Only if implemented in backend
Trees, stacks, queues (data structures) || ⚠️ ||	Backend only, not visible in UI
Batch/large data handling ||	⚠️  || 	Not shown, but backend may support
Integration with external APIs/databases ||	✅ || 	Supabase used for storage

---

## Technologies Used

- **Frontend:** React, Axios
- **Backend:** FastAPI (Python)
- **Database:** Supabase (PostgreSQL)
- **Other:** Node.js, npm

---

## Getting Started

### 1. Clone the Repository
git clone <your-repo-url>
cd cash_flow


### 2. Set Up the Backend

- Ensure you have Python 3.9+ and Node.js 18.x or 20.x LTS installed.
- Install backend dependencies:
pip install -r requirements.txt
- Create a `.env` file in the backend folder:
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key



- **Create the `transactions` table in Supabase** using the SQL Editor:

create table if not exists transactions (
id uuid primary key default gen_random_uuid(),
sender text not null,
receiver text not null,
amount float8 not null,
timestamp timestamptz not null default now(),
due_date date,
interest_rate float8,
penalty float8
);



- Start the backend server:
python -m uvicorn main:app --reload

The API will be available at [http://localhost:8000](http://localhost:8000).

---

### 3. Set Up the Frontend

- In a separate terminal:

cd cash_flow_frontend
npm install
npm install axios

- If using Node.js 17+, 18+, or 20+, start the app with:

$env:NODE_OPTIONS="--openssl-legacy-provider"
npm start


The frontend will run at [http://localhost:3000](http://localhost:3000).

---

## Usage

1. **Add a Transaction:** Fill in the sender, receiver, amount, due date, interest rate, and penalty, then click "Add Transaction".
2. **View Transactions:** All transactions are listed in the table below the form.
3. **Minimize Cash Flow:** Click "Minimize Cash Flow" to see the optimized settlements.
4. **All data is stored in Supabase and can be accessed or managed as needed.**

---

## Project Structure

cash_flow/
│
├── main.py # FastAPI backend
├── cashflow_logic.py # Business logic
├── supabase_client.py # Supabase DB connection
├── requirements.txt # Python dependencies
├── .env # Backend environment variables
├── cash_flow_frontend/ # React frontend app

