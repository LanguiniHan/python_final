import sqlite3

import uuid
from flask import render_template, request, redirect, jsonify
# from dotenv import load_dotenv
import os
from routes.category import category

# load_dotenv()

TRUE = os.environ.get('true_code')
FALSE = os.environ.get('false_code')
CREATE = os.environ.get('create_code')
UPDATE = os.environ.get('update_code')
DELETE = os.environ.get('delete_code')

app = category

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(debug=True)

def do_OPTIONS(self):
    self.send_response(200, "ok")
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')

@app.route("/admin/category")
def category():
    return render_template("admin/category/index.html")


@app.route("/api/category")
def getCategories():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * from category;")
    categories = cur.fetchall()
    category = []
    for item in categories:
        category.append({
            'id': item['id'],
            'name': item['name'],
            'status': item['status']
        })
    return category


@app.route("/api/category", methods=["POST"])
def add_category():
    data = request.get_json()
    id = str(uuid.uuid4())
    name = data['name']
    status = 0
    if data['status']:
        status = 1
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO category (id,name,status) VALUES (?,?,?)", (id, name, status))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        res = jsonify({'data': {'id': id, 'name': name, 'status': status}, "message": "Successfully added category.",
                       'status': "success"})
        res.status_code = 201

        return res
    else:
        res = jsonify({"message": "Failed to add category.",
                       'status': "failed"})
        res.status_code = 400

        return res


@app.route("/api/category/<id>", methods=["DELETE"])
def delete_category(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM category WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(cursor.rowcount)
    if cursor.rowcount > 0:
        res = jsonify({"message": "Successfully deleted category"})

        res.status_code = 200

        return res
    else:
        res = jsonify({"message": "Failed to delete category"})
        res.status_code = 400

        return res


@app.route('/api/category', methods=["PUT"])
def edit_category():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    data = request.get_json()
    query = '''
    UPDATE category 
    SET name = ?, status = ? WHERE id = ?
    '''
    name = data['name']
    status = 0
    if (data['status']):
        status = 1
    cursor.execute(query, (name, status, data['id']))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        res = jsonify(
            {'data': {'id': data['id'], 'name': name, 'status': status}, "message": "Successfully edit category.",
             'status': "success"})
        res.status_code = 200
        return res
    else:
        res = jsonify({"message": "Successfully edit category.",
                       'status': "success"})
        res.status_code = 400
        return res


