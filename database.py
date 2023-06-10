import sqlite3
from todo import Todo
from typing import List
from datetime import datetime
conn = sqlite3.connect('todos.db') 
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS todos (
            id integer PRIMARY KEY AUTOINCREMENT,
            object text,
            task text,
            price real,
            date_added text,
            date_completed text,
            status integer,
            note text
        )''')
    
create_table()


def insert_todo(todo: Todo):
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    with conn:
        c.execute('INSERT INTO todos (object, task, price, date_added, date_completed, status, note) VALUES (?,?,?,?,?,?,?)',
                  (todo.object,todo.task,todo.price,todo.date_added, 
                   todo.date_completed, todo.status, todo.note))        


def get_all_todos() -> List[Todo]:
    c.execute('select * FROM todos')
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(id=result[0], object=result[1], task=result[2], price=result[3], date_added=result[4], date_completed=result[5], status=result[6], note=result[7]))

    return todos


def delete_todo(id):
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    with conn:
        c.execute('DELETE FROM todos WHERE id=:id', {'id':id})
        for pos in range(id+1, count):
            change_position(pos, pos-1, False)


def complete_task(id):
    with conn:
        c.execute('UPDATE todos SET status = 1, date_completed = :date_completed WHERE id = :id',
                {'id':id,'date_completed':datetime.now().isoformat()})


def reopen_task(id):
    with conn:
        c.execute('UPDATE todos SET status = 0, date_completed = :date_completed WHERE id = :id',
                {'id':id,'date_completed':None})


def edit_task(id, task):
    with conn:
        c.execute('UPDATE todos SET task = :task WHERE id = :id',
                {'id':id,'task':task})
   
        
def edit_price(id, price):
    with conn:
        c.execute('UPDATE todos SET price = :price WHERE id = :id',
                {'id':id,'price':price})
  
        
def edit_note(id, note):
    with conn:
        c.execute('UPDATE todos SET note = :note WHERE id = :id',
                {'id':id,'note':note})

           
def change_position(old_id, new_id, commit=True):
    c.execute('UPDATE todos SET id = :id_new WHERE id = :id_old',
              {'id_old':old_id, 'id_new':new_id})
    if commit:
        conn.commit()
