import json
import random
from pprint import pprint

from flask import Flask, jsonify, request, abort
import uuid

app = Flask(__name__)

todoLists = dict()
userList = dict()


@app.after_request
def apply_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify("Index")


@app.route("/todo-list/<list_id>", methods=["GET", "DELETE"])
def get_delete_list(list_id):
    if request.method == "GET":
        list = get_list(list_id)
        if list is None:
            # if no list is found return 404
            abort(404)
        else:
            return list.toJson(), 200

    elif request.method == "DELETE":
        list = get_list(list_id)
        if list is None:
            # if no list is found return 404
            abort(404)
        else:
            todoLists.pop(list_id)  # check if this works
            return '', 200
        # if no list is found return 404
        abort(404)
    else:
        abort(405)  # Method not allowed


@app.route("/todo-list", methods=["POST"])
def add_list():
    entries = dict()
    data = request.get_json()

    list = TodoList(data['name'])

    for entry in data['entries']:

        tmp = TodoEntry(entry['name'], entry['description'], list.id, data.user)
        # add entry to list
        entries[tmp.id] = tmp

    list.entries = entries
    todoLists[list.id] = list
    return list.toJson(), 200


@app.route("/todo-list/<list_id>/entry", methods=["POST"])
def add_to_todolist(list_id):
    list = get_list(list_id)
    if list is None:
        # if no list is found return 404
        abort(404)
    else:
        data = request.get_json()
        entry = TodoEntry(data['name'], data['description'], list_id, data['user_id'])
        list.entries[entry.id] = entry
        return list.toJson(), 200
    # abort(404)


@app.route("/todo-list/<list_id>/entry/<entry_id>", methods=["PUT", "DELETE"])
def change_todolist_entry(list_id, entry_id):
    list = get_list(list_id)
    if list is None:
        abort(404)

    if request.method == "PUT":

        # get data from body
        body = request.get_json()

        # create new entry with same id as old one
        new_entry = TodoEntry(body['name'], body['description'], list_id, body['user_id'], entry_id)

        # replace the old entry with the new one
        set_entry(list_id, entry_id, new_entry)

        return jsonify("OK", success=True)
    elif request.method == "DELETE":
        # successful delete
        if delete_entry(list_id, entry_id):
            return '', 200
        else:
            abort(404)
    else:
        abort(405)


@app.route('/user', methods=["GET", "POST"])
def get_users():
    if request.method == "GET":
        print("Get Users")
        return jsonify([userList[i].toJson() for i in userList])
    elif request.method == "POST":
        print("Post Users")

        body = request.get_json()

        # print(f"Form: {form}")
        # print("BODY: ")
        print(body)

        user = User(body['name'])
        userList[user.id] = user
        return user.toJson(), 200
    else:
        abort(405)


@app.route('/user/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    if userList[user_id]:
        del userList[user_id]
        return '', 200
    else:
        abort(404)


def get_list(list_id):
    if todoLists[list_id]:
        return todoLists[list_id]
    return None


def set_list(list_id, new_list):
    if todoLists[list_id]:
        todoLists[list_id] = new_list
        return 0  # success
    return -1  # failure


def get_entry(list_id, entry_id):
    list = get_list(list_id)
    entries = list.entries
    if list.entries[entry_id]:
        return list.entries[entry_id]
    return None


def set_entry(list_id, entry_id, new_entry):
    list = get_list(list_id)
    if list.entries[entry_id]:
        list.entries[entry_id] = new_entry
        set_list(list_id, list)


def delete_entry(list_id, entry_id):
    list = get_list(list_id)
    print(list.entries, entry_id)

    if list.entries[entry_id]:
        del list.entries[entry_id]
        return True
    return False


class TodoEntry:
    def __init__(self, name, description, list_id, user_id, id=None):
        if id is None:
            self.id = f"tde_{uuid.uuid4()}"
        else:
            self.id = id

        self.name = name
        self.description = description
        self.list_id = list_id
        self.user_id = user_id

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class TodoList:
    def __init__(self, name, entries=None, id=None):
        if id is None:
            self.id = f"tdl_{uuid.uuid4()}"
        else:
            self.id = id
        self.name = name
        if entries is None:
            self.entries = dict()
        else:
            self.entries = entries

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class User:
    def __init__(self, name, id=None):
        if id is None:
            self.id = f"usr_{uuid.uuid4()}"
        else:
            self.id = id
        self.name = name

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        # return json.dump({'id': self.id, 'name': self.name})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
