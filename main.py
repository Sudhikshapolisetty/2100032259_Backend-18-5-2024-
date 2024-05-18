import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sudhiksha@2004",
    database="pythonSql",
    port=3306
)

cursor = conn.cursor()

def createtable():
    try:
        query = """
        CREATE TABLE customers
        (
            customerID int primary key,
            first_name varchar(30),
            last_name varchar(30),
            email varchar(30),
            dateofbirth date
        )
        """
        cursor.execute(query)

        query = """
                CREATE TABLE products
                (
                    productid int primary key,
                    productname varchar(30),
                    price int
                )
                """

        cursor.execute(query)

        query = """
                CREATE TABLE orders
                (
                    orderid INT PRIMARY KEY AUTO_INCREMENT,
                    customerid INT,
                    orderdate DATE,
                    FOREIGN KEY (customerid) REFERENCES customers(customerid)
                )
                """

        cursor.execute(query)

        query = """
                create table orderItem
                (
                    orderitemid int primary key AUTO_INCREMENT,
                    orderid int,
                    productid int,
                    quantity int,
                    foreign key(productid) references products(productid),
                    foreign key(orderid) references orders(orderid)
                )
                """
        cursor.execute(query)
        print("Tables created successfully")
    except Exception as e:
        print(e)

def  insert_customers():
    try:
        query = """
                INSERT INTO customers (customerid, first_name, last_name, email, dateofbirth)
                VALUES (%s, %s, %s, %s, %s)
                """
        data = (1, 'John', 'Deo', 'john.deo@example.com', '1985-01-15')

        cursor.execute(query, data)

        data = (2,'Jane','Smith','jane.smith@example.com','1990-06-20')

        cursor.execute(query, data)
        conn.commit()

        print("Inserted Successfully")

    except Exception as e:
        print(e)


def insert_order():
    try:
        query = """
                insert into orders(customerid,orderdate)
                values(%s,%s)
                """
        data = (1, '2023-01-10')

        cursor.execute(query, data)

        data = (2, '2023-01-12')

        cursor.execute(query, data)
        conn.commit()
        print("Inserted Successfully")
    except Exception as e:
        print(e)

def insert_products():
    try:
        query = """
                insert into products(productid,productname,price)
                values (%s, %s, %s)
                """
        data = (1, 'Laptop', 1000)
        cursor.execute(query, data)

        data = (2, 'Smartphone', 600)
        cursor.execute(query, data)

        data = (3, 'HeadPhones', 100)
        cursor.execute(query, data)
        conn.commit()
        print("Inserted Successfully")
    except Exception as e:
        print(e)

def insert_orderItem():
    try:
        query = """
                insert into orderItem(orderid,productid,quantity)
                values(%s,%s,%s)
        """
        data = (1, 1, 1)
        cursor.execute(query, data)
        data = (1, 3, 2)
        cursor.execute(query, data)
        data = (2, 2, 1)
        cursor.execute(query, data)
        data = (2, 3, 1)
        cursor.execute(query, data)
        conn.commit()
        print("Inserted Successfully")
    except Exception as e:
        print(e)

#1. List all customers.
def query_1():
    try:
        query = "select * from customers"

        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
    except Exception as e:
            print(e)

#2. Find all orders placed in January 2023.
def query_2():
    try:
        query = "select * from orders where month(orderDate) = 1 and year(orderDate) = 2023;"

        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
    except Exception as e:
            print(e)

#3. Get the details of each order, including the customer name and email.
def query_3():
    try:
        query = "select orderID,first_name,last_name,email,orderDate from orders o left join customers c on o.customerID=c.customerID;"

        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
    except Exception as e:
            print(e)

#4. List the products purchased in a specific order (e.g., OrderID = 1).
def query_4():
    try:
        query = "select oi.orderID,p.productName from orderItem oi right join products p on oi.productID=p.productID where orderId = 1;"

        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
    except Exception as e:
            print(e)

#5. Calculate the total amount spent by each customer.
def query_5():
    try:
        query = """select cu.customerid, cu.first_name, sum(oi.quantity * p.price) AS total_spent from customers cu
                    join orders o ON cu.customerid = o.customerid
                    join orderItem oi ON o.orderid = oi.orderid
                    join products p ON oi.productid = p.productid
                    group by cu.customerid, cu.first_name 
                    order by cu.customerid asc;"""

        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
    except Exception as e:
            print(e)

#6. Find the most popular product (the one that has been ordered the most).
def query_6():
    try:
        query = """select p.productName as Most_Popular from products p join orderItem oi on p.productId=oi.productid
                   group by p.productName
                   order by Most_Popular desc
                   limit 1;"""

        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
    except Exception as e:
            print(e)

# 7. Get the total number of orders and the total sales amount for each month in 2023.
def query_7():
    try:
        query = """select date_format(orderDate, "%y %m") AS month, count(o.orderid) AS total_orders, SUM(oi.quantity * p.price) AS total_sales
                    from orders o
                    join orderItem oi ON o.orderid = oi.orderid
                    join products p ON oi.productid = p.productid
                    where orderDate >= '2023-01-01' and orderDate < '2024-01-01'
                    group by date_format(orderDate, "%y %m");"""

        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
    except Exception as e:
            print(e)

#    8.Find customers who have spent more than $1000.
def query_8():
    try:
        query = """select c.customerid, c.first_name, sum(oi.quantity * p.price) AS total_spent
                    from customers c
                    join orders o ON c.customerid = o.customerid
                    join orderItem oi ON o.orderid = oi.orderid
                    join products p ON oi.productid = p.productid
                    group by c.customerid, c.first_name
                    having total_spent > 1000;"""

        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
    except Exception as e:
        print(e)

#createtable()
# insert_customers()
# insert_products()
# insert_order()
# insert_orderItem()
#query_1()
#query_2()
#query_3()
#query_4()
#query_5()
#query_6()
#query_7()
query_8()

conn.close()
