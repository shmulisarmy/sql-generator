import sys
from colors import red, green, blue, yellow


import os
    
def get_folder_name() -> str:
    return os.getcwd().split('/')[-1]


def write_and_print(content):
    with open("database_interface.py", "a") as f:
        f.write(content + '\n')

    print(content)



def getenerate_sqlite_select_query(looking_for_args, fetch_type, table_name, db_name = 'main.db'):
    print(blue("getenerate sqlite select query").center(50, '-'))
    r = f"""def get_{to_singular(table_name)}(id: int) -> {'tuple' if fetch_type == 'o' else 'list[tuple]'}:
        '''gets {', '.join(looking_for_args)} from {table_name}'''
        query = "select {', '.join(looking_for_args)} from {table_name} where id = ?"
        with sqlite3.connect('{db_name}') as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, (id)).{'fetchone' if  fetch_type == 'o' else 'fetchall'}()
        return result
    
    """
    write_and_print(r)


def generate_sqlite_delete_query(table_name, db_name = 'main.db'):
    print(blue("getenerate sqlite select query").center(50, '-'))
    r = f"""def delete_{to_singular(table_name)}(id: int):
        query = "delete from {table_name} where id = ?"
        with sqlite3.connect('{db_name}') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id))
                
    """
    write_and_print(r)


    


def generate_sql_insert_query(insertions: list, table_name: str, db_name = 'main.db'):
    print(blue("generate insert select query").center(50, '-'))
    r = f"""def create_{to_singular(table_name)}({', '.join(insertions)}) -> int:
        '''inserts {', '.join(insertions)} into {table_name}'''
        query = "insert into {table_name} ({', '.join(insertions)}) values ({', '.join(['?'] * len(insertions))})"
        with sqlite3.connect('{db_name}') as conn:
            cursor = conn.cursor()
            cursor.execute(query, ({', '.join(insertions)}))
        return cursor.lastrowid
    
    """
    write_and_print(r)


def generate_sql_update_query(insertions: list, table_name: str, db_name = 'main.db',):
    print(blue("generate insert select query").center(50, '-'))
    r = f"""def update_{to_singular(table_name)}({', '.join(insertions)}, id: int) -> int:
        '''updates {', '.join(insertions)} in {table_name} table'''
        query = "update {table_name} set {', '.join((f"{arg} = ?" for arg in insertions))} where id = ?"
        with sqlite3.connect('{db_name}') as conn:
            cursor = conn.cursor()
            cursor.execute(query, {', '.join(insertions)}, id)
    
    """
    write_and_print(r)



def ask_for_update(db_name = None, table_name = None):
    if not table_name:
        table_name = input("table name: ")
    if not db_name:
        db_name = (input(green("db_name: ")) or "main.db") 

    insertions = tuple(input("insertions: ").split(" "))

    generate_sql_update_query(insertions, table_name, db_name)





def ask_for_select(db_name = None, table_name = None):
    if not table_name:
        table_name = input("table name: ")
    if not db_name:
        db_name = (input(green("db_name: ")) or "main.db") 

    args = tuple(input("args: ").split(" "))
    fetch_type = 'o'#input("fetch_type (o for one and a for all): ")
    # whereStatement = input(green("whereStatement (enter to skip): "))
    looking_with_args = tuple(input(green("looking_with_args (enter to skip): ")).split(" "))

    getenerate_sqlite_select_query(looking_with_args, args, fetch_type, table_name, db_name)



def ask_for_insert(db_name = None, table_name = None):
    if not table_name:
        table_name = input("table name: ")
    if not db_name:
        db_name = (input(green("db_name: ")) or "main.db") 

    insertions = tuple(input("insertions: ").split(" "))
    generate_sql_insert_query(insertions, table_name, db_name)






def to_singular(word):
    if word.endswith('men'):
        return word[:-2] + 'man'
    if word.endswith('ices'):
        return word[:-4] + 'ice'
    if word.endswith('ices'):
        return word[:-4] + 'ouse'
    if word.endswith('ves'):
        return word[:-3] + 'f'
    if word.endswith('ves'):
        return word[:-3] + 'fe'
    if word.endswith('s'):
        return word[:-1]
    if word.endswith('ies'):
        return word[:-3] + 'y'
    if word.endswith('ies'):
        return word[:-4] + 'ix'
    if word.endswith('feet'):
        return word[:-4] + 'foot'
    if word.endswith('teeth'):
        return word[:-5] + 'tooth'
    if word.endswith('uses'):
        return word[:-3] + 'us'
    if word.endswith('oes'):
        return word[:-2]
    return word

def entire_file(db_name = None, table_name = None):
    write_and_print("import sqlite3\n\n\n\n")
    if not table_name:
        table_name = input(f"{green('table name')} (if omitted will revert to {blue(get_folder_name())}): ") or get_folder_name()
    if not db_name:
        db_name = input(f"{green('table name')} (if omitted will revert to {blue('main.db')}): ") or 'main.db'

    fields = tuple(input("please enter the fields that you want in your table seperated by a space: ").split(" "))
    fetch_type = 'o'#input("fetch_type (o for one and a for all): ")
    

    getenerate_sqlite_select_query(fields, fetch_type, table_name, db_name)
    generate_sql_insert_query(fields, table_name, db_name = 'main.db',)
    generate_sql_update_query(fields, table_name, db_name = 'main.db',)
    generate_sqlite_delete_query(table_name, db_name = 'main.db')


    with open("statements.sql", "a") as f:
        f.write(f"create table query create table {table_name} (id integer primary key autoincrement, {', '.join(fields)})\n")

        for field in fields:
            f.write(f"create index {table_name}_{field}_index on {table_name} ({field})\n")


print(f"please enter either {green('f')} for entire file or {green('a')} for an update query generator")



if len(sys.argv) > 1:
    if sys.argv[1] == "f": 
        entire_file()
    else:
        ask_for_update()