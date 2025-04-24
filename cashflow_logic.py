import heapq
from collections import defaultdict
from datetime import datetime

def validate_transactions(transactions):
    valid = []
    for tx in transactions:
        try:
            sender = tx['sender']
            receiver = tx['receiver']
            amount = float(tx['amount'])
            if sender and receiver and amount > 0:
                timestamp = tx.get('timestamp')
                due_date = tx.get('due_date')
                interest_rate = float(tx.get('interest_rate', 0)) if 'interest_rate' in tx else 0
                penalty = float(tx.get('penalty', 0)) if 'penalty' in tx else 0
                valid.append({
                    'sender': sender,
                    'receiver': receiver,
                    'amount': amount,
                    'timestamp': timestamp,
                    'due_date': due_date,
                    'interest_rate': interest_rate,
                    'penalty': penalty
                })
        except Exception:
            continue
    return valid

def sort_transactions_chronologically(transactions):
    def parse_ts(tx):
        ts = tx.get('timestamp')
        try:
            return datetime.fromisoformat(ts) if ts else datetime.min
        except Exception:
            return datetime.min
    return sorted(transactions, key=parse_ts)

def apply_constraints(transactions, payment_date=None):
    adjusted = []
    if payment_date is None:
        payment_date = datetime.utcnow()
    elif isinstance(payment_date, str):
        payment_date = datetime.fromisoformat(payment_date)
    for tx in transactions:
        amount = tx['amount']
        due_date = tx.get('due_date')
        interest_rate = tx.get('interest_rate', 0)
        penalty = tx.get('penalty', 0)
        if due_date:
            try:
                due_dt = datetime.fromisoformat(due_date)
                if payment_date > due_dt:
                    days_late = (payment_date - due_dt).days
                    amount += amount * interest_rate * days_late
                    amount += penalty
            except Exception:
                pass
        tx2 = tx.copy()
        tx2['amount'] = round(amount, 2)
        adjusted.append(tx2)
    return adjusted

def minimize_transactions(transactions):
    balances = defaultdict(float)
    for tx in transactions:
        balances[tx['sender']] -= tx['amount']
        balances[tx['receiver']] += tx['amount']

    debtors = []
    creditors = []
    for person, balance in balances.items():
        if balance < -1e-9:
            heapq.heappush(debtors, (balance, person))
        elif balance > 1e-9:
            heapq.heappush(creditors, (-balance, person))

    result = []
    while debtors and creditors:
        debt, debtor = heapq.heappop(debtors)
        credit, creditor = heapq.heappop(creditors)
        credit = -credit
        transfer = min(-debt, credit)
        result.append({'sender': debtor, 'receiver': creditor, 'amount': round(transfer, 2)})
        new_debt = debt + transfer
        new_credit = credit - transfer
        if new_debt < -1e-9:
            heapq.heappush(debtors, (new_debt, debtor))
        if new_credit > 1e-9:
            heapq.heappush(creditors, (-new_credit, creditor))
    return result
