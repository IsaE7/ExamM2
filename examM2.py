import sqlite3


def create_tables_and_insert_data():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        code TEXT PRIMARY KEY,
        title TEXT
    )
    ''')

    cursor.executemany('''
    INSERT INTO categories (code, title) VALUES (?, ?)
    ''', [
        ('FD', 'Food products'),
        ('EL', 'Electronics'),
        ('CL', 'Clothes')
    ])

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        title TEXT,
        category_code TEXT,
        unit_price REAL,
        stock_quantity INTEGER,
        store_id INTEGER,
        FOREIGN KEY (category_code) REFERENCES categories(code),
        FOREIGN KEY (store_id) REFERENCES store(store_id)
    )
    ''')

    cursor.executemany('''
    INSERT INTO products (id, title, category_code, unit_price, stock_quantity, store_id) VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        (1, 'Chocolate', 'FD', 10.5, 129, 1),
        (2, 'Jeans', 'CL', 120.0, 55, 2),
        (3, 'T-Shirt', 'CL', 0.5, 15, 1)
    ])

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS store (
        store_id INTEGER PRIMARY KEY,
        title TEXT
    )
    ''')

    cursor.executemany('''
    INSERT INTO store (store_id, title) VALUES (?, ?)
    ''', [
        (1, 'Asia'),
        (2, 'Globus'),
        (3, 'Spar')
    ])

    conn.commit()
    conn.close()


def display_stores(cursor):
    cursor.execute("SELECT store_id, title FROM store")
    stores = cursor.fetchall()
    print(
        "Вы можете отобразить список продуктов по выбранному id магазина из перечня магазинов ниже, для выхода из программы введите цифру 0:")
    for store in stores:
        print(f"{store[0]}. {store[1]}")


def display_products(cursor, store_id):
    query = """
    SELECT p.title, c.title, p.unit_price, p.stock_quantity
    FROM products p
    JOIN categories c ON p.category_code = c.code
    WHERE p.store_id = ?
    """
    cursor.execute(query, (store_id,))
    products = cursor.fetchall()
    for product in products:
        print(f"Название продукта: {product[0]}")
        print(f"Категория: {product[1]}")
        print(f"Цена: {product[2]}")
        print(f"Количество на складе: {product[3]}")
        print("")


def main():
    create_tables_and_insert_data()

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    while True:
        display_stores(cursor)
        store_id = int(input("Введите id магазина: "))
        if store_id == 0:
            break
        display_products(cursor, store_id)

    conn.close()


if __name__ == "__main__":
    main()
