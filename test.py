from Database import Database

connection = Database(host="localhost", user="root", password="root", database="pets")

# print(connection.insert('customers', 'Tim', 'Test Rd 6'))

print(connection.dropTable('customers'))
