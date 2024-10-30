from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data storage for budget items and income/expenses (for simplicity)
budget_items = []
income = 0
expenses = 0

@app.route('/')
def index():
    balance = income - expenses
    summary = {
        'total_income': income,
        'total_expenses': expenses,
        'remaining_balance': balance
    }
    return render_template('index.html', items=budget_items, summary=summary)

@app.route('/add', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    amount = request.form['amount']
    item_type = request.form['type']  # 'income' or 'expense'
    category = request.form['category']  # e.g., 'Food', 'Rent', 'Entertainment', 'Pay'
    if item_name and amount:
        amount = float(amount)
        budget_items.append({'name': item_name, 'amount': amount, 'type': item_type, 'category': category, 'done': False})
        global income, expenses
        if item_type == 'income':
            income += amount
        elif item_type == 'expense':
            expenses += amount
    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    if 0 <= item_id < len(budget_items):
        budget_items[item_id]['done'] = not budget_items[item_id]['done']
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 0 <= item_id < len(budget_items):
        global income, expenses
        item = budget_items[item_id]
        if item['type'] == 'income':
            income -= item['amount']
        elif item['type'] == 'expense':
            expenses -= item['amount']
        del budget_items[item_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)