import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000"; // Change if deploying backend elsewhere

function App() {
  const [transactions, setTransactions] = useState([]);
  const [form, setForm] = useState({
    sender: "",
    receiver: "",
    amount: "",
    due_date: "",
    interest_rate: "",
    penalty: ""
  });
  const [settlements, setSettlements] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch transactions from backend
  const fetchTransactions = async () => {
    try {
      const res = await axios.get(`${API_URL}/transactions/`);
      setTransactions(res.data);
    } catch (err) {
      alert("Error fetching transactions");
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  // Handle form changes
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Add a new transaction
  const handleAdd = async (e) => {
    e.preventDefault();
    const tx = {
      sender: form.sender,
      receiver: form.receiver,
      amount: parseFloat(form.amount),
      due_date: form.due_date || null,
      interest_rate: form.interest_rate ? parseFloat(form.interest_rate) : null,
      penalty: form.penalty ? parseFloat(form.penalty) : null
    };
    try {
      await axios.post(`${API_URL}/transactions/`, [tx]);
      setForm({
        sender: "",
        receiver: "",
        amount: "",
        due_date: "",
        interest_rate: "",
        penalty: ""
      });
      fetchTransactions();
    } catch (err) {
      alert("Error adding transaction");
    }
  };

  // Minimize settlements
  const handleSettle = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/settle/`, transactions);
      setSettlements(res.data);
    } catch (err) {
      alert("Error computing settlements");
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 800, margin: "auto", padding: 20 }}>
      <h2>Cash Flow Minimizer</h2>
      <form onSubmit={handleAdd} style={{ marginBottom: 20 }}>
        <input
          name="sender"
          value={form.sender}
          onChange={handleChange}
          placeholder="Sender"
          required
        />
        <input
          name="receiver"
          value={form.receiver}
          onChange={handleChange}
          placeholder="Receiver"
          required
        />
        <input
          name="amount"
          value={form.amount}
          onChange={handleChange}
          placeholder="Amount"
          type="number"
          min="0.01"
          step="0.01"
          required
        />
        <input
          name="due_date"
          value={form.due_date}
          onChange={handleChange}
          placeholder="Due Date (YYYY-MM-DD)"
          type="date"
        />
        <input
          name="interest_rate"
          value={form.interest_rate}
          onChange={handleChange}
          placeholder="Interest Rate (per day, e.g. 0.01)"
          type="number"
          step="0.01"
        />
        <input
          name="penalty"
          value={form.penalty}
          onChange={handleChange}
          placeholder="Penalty"
          type="number"
          step="0.01"
        />
        <button type="submit">Add Transaction</button>
      </form>

      <h3>All Transactions</h3>
      <table border="1" cellPadding={5} style={{ width: "100%", marginBottom: 20 }}>
        <thead>
          <tr>
            <th>Sender</th>
            <th>Receiver</th>
            <th>Amount</th>
            <th>Due Date</th>
            <th>Interest Rate</th>
            <th>Penalty</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx, idx) => (
            <tr key={idx}>
              <td>{tx.sender}</td>
              <td>{tx.receiver}</td>
              <td>{tx.amount}</td>
              <td>{tx.due_date || "-"}</td>
              <td>{tx.interest_rate || "-"}</td>
              <td>{tx.penalty || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <button onClick={handleSettle} disabled={loading || transactions.length === 0}>
        {loading ? "Calculating..." : "Minimize Cash Flow"}
      </button>

      <h3>Settlements</h3>
      {settlements.length === 0 && <div>No settlements to show.</div>}
      <ul>
        {settlements.map((s, idx) => (
          <li key={idx}>
            <b>{s.sender}</b> pays <b>{s.receiver}</b> <b>{s.amount}</b>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
