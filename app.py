#! python3

"""
Возможные запросы:
/
/?amount=2 (сколько показать)
/?column=названиеCтолбца (author или content)
"""

from flask import Flask, request, jsonify
import sqlite3
import logging as l

l.basicConfig(level=l.DEBUG, format='%(levelname)s %(lineno)d, %(funcName)s - %(message)s')
# l.disable(l.DEBUG)

app = Flask(__name__)

conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
cur = conn.cursor()


@app.route('/')
def get_all():
    """
    Get all data from the database
    :return: {"content":[], "authors":[]}
    """
    args = request.args
    l.debug(f'Args = {args}')
    column = args.get('column')
    column = column or '*'
    amount = args.get('amount')  # None if not found
    l.debug(f'column = {column}')
    l.debug(f'amount: {amount}')
    l.debug(f'amount type: {type(amount)}')
    l.debug(f'Request args: {request.args}')
    l.debug(f"request.args.get('content'): {request.args.get('content', 'Nothing here')}")
    l.debug(f'Request values: {request.values}')
    l.debug(f'request values with get(\'content\'): {request.values.get("content")}')
    l.debug(f'request path: {request.path}')

    query = f'SELECT {column} FROM news'
    l.debug(f'Query: {query}')
    # Fill the cursor
    cur.execute(query)

    # Convert to get amount of data a user wants
    try:
        amount = int(amount)
    except:
        l.error('converting to int has failed', exc_info=True)

    # Take data from the cursor
    data = cur.fetchmany(amount) if amount else cur.fetchall()
    l.debug(f'Data = {data}')

    # Create return_var

    # If both columns are parsed
    if column == '*':
        return_var = []
        for t in data:
            return_var.append(
                {
                    'content': t[0],
                    'author': t[1],
                }
            )
    # If column arg is provided
    else:
        return_var = {}
        for t in data:
            return_var.setdefault(column, [])
            return_var[column].append(t[0])

    l.debug(f'return_var = {return_var}')
    return_var = jsonify(return_var)
    return return_var


if __name__ == '__main__':
    app.run(debug=True, port=5001)
