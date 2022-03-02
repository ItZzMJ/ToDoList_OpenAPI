import requests
import json
from pprint import pprint

url = "http://127.0.0.1/"
headers = {'content-type': 'application/json'}

# user erstellen

# todo listen erstellen

# einträge erzeugen

def user_test():
    # 2 user erstellen
    user1 = "Hans"
    user2 = "Günter"

    print(f"Creating User {user1}: ", end=' ')
    r = requests.post(url + "user", json={'name': user1})
    print(f"{r.status_code} {r.json()}")

    print(f"Creating User {user2}: ", end=' ')
    r = requests.post(url + "user", json={'name': user2})
    print(f"{r.status_code} {r.json()}")

    # get users
    print("Get Users: ", end=' ')
    r = requests.get(url + "user")
    print(f"{r.status_code} {r.json()}")

    user_id = json.loads(r.json()[0]).get('id')

    # einen User löschen
    print("Delete Users: ", end=' ')
    r = requests.delete(url + f"user/{user_id}")
    print(f"{r.status_code}")

    # get users
    print("Get Users: ", end=' ')
    r = requests.get(url + "user")
    print(f"{r.status_code} {r.json()}")

    return user_id


def todolist_test(user_id):
    # create list1
    print('Create List1: ', end=' ')
    r = requests.post(url + "todo-list", json={"name": "list1", "entries": []})
    print(f"{r.status_code} {r.json()}")

    list1_id = r.json().get('id')


    # create list2
    print('\nCreate List2: ', end=' ')
    r = requests.post(url + "todo-list", json={"name": "list2", "entries": []})
    print(f"{r.status_code} {r.json()}")

    list2_id = r.json().get('id')

    # add entry to lists 1+2
    print('\nAdding Entries to List1', end=' ')
    r = requests.post(url + f"todo-list/{list1_id}/entry", json={"name": "Milch", "description": "Description",
                                                                 "user_id": user_id})
    print(f"{r.status_code} {r.json()}")

    print('\nAdding Entries to List1', end=' ')
    r = requests.post(url + f"todo-list/{list1_id}/entry", json={"name": "Eier", "description": "Description",
                                                                 "user_id": user_id})
    print(f"{r.status_code} {r.json()}")

    entry_to_update = r.json()

    # add second list entry to lists 1+2
    print('\nAdding Entries to List2', end=' ')
    r = requests.post(url + f"todo-list/{list2_id}/entry", json={"name": "Maus", "description": "Description",
                                                                 "user_id": user_id})
    print(f"{r.status_code} {r.json()}")

    print('\nAdding Entries to List2', end=' ')
    r = requests.post(url + f"todo-list/{list2_id}/entry", json={"name": "Tastatur", "description": "Description",
                                                                 "user_id": user_id})
    print(f"{r.status_code} {r.json()}")

    entry_to_delete = r.json()

    # get todolist 2
    print("\nTodo-List 2:", end=' ')
    r = requests.get(url + f"todo-list/{list2_id}")
    print(f"{r.status_code} {r.json()}")

    # remove first entry from list2
    print("\nRemoving entry from list2", end=' ')
    r = requests.delete(url + f"todo-list/{list2_id}/entry/{entry_to_delete}")
    print(f"{r.status_code}")

    # get todolist 2
    print("\nTodo-List 2:", end=' ')
    r = requests.get(url + f"todo-list/{list2_id}")
    print(f"{r.status_code} {r.json()}")

    # update entry from list 1
    print("\nUpdating second entry from list1", end=' ')
    r = requests.put(url + f"todo-list/{list1_id}/entry/{entry_to_update}", json={"name": "Butter",
                                                                                  "description": "Description",
                                                                                  "user_id": user_id})
    print(f"{r.status_code}")

    # print list 1
    print("\nTodo-List 1:", end=' ')
    r = requests.get(url + f"todo-list/{list1_id}")
    print(f"{r.status_code} {r.json()}")

    # delete list 1
    print("\nDelete Todo-List 1:", end=' ')
    r = requests.delete(url + f"todo-list/{list1_id}")
    print(f"{r.status_code}")

    # print list 1
    print("\nTodo-List 1:", end=' ')
    r = requests.get(url + f"todo-list/{list1_id}")
    print(f"{r.status_code}")


if __name__ == "__main__":
    user_id = user_test()
    todolist_test(user_id)
    print("\nFinished\n")
