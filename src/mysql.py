import mysql.connector

class Mysql:

    __host = None
    __user = None
    __password = None
    __database = None
    
    __cursor = None
    __connection = None

    def __init__(self, host, user, password, database):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def open(self):
        try:
            cnx = mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__database
            )
            self.__connection = cnx
            self.__cursor = cnx.cursor(buffered=True, dictionary=True)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exists')
            else:
                print(err)

    def close(self):
        self.__cursor.close()
        self.__connection.close()

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = kwargs.values()
            query += "(" + ",".join(["`%s`"]*len(keys)) % tuple(keys) + ") VALUES(" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"
        self.open()
        self.__cursor.execute(query, values)
        self.__connection.commit()
        self.close()
        return self.__cursor.lastrowid

    def select(self, table, where=None, *args):
        result = None
        query = "SELECT "
        keys = args
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"`"
            if i < l:
                query += ","
        query += " FROM %s" % table
        if where:
            query += " WHERE %s" % where
        self.open()
        self.__cursor.execute(query)
        result = self.__cursor.fetchall()
        self.close()
        return result

    def addTable(self, template):
        self.open()
        self.__cursor.execute(template)
        self.close()
    
    def checkIfTableExists(self, table):
        self.open()
        query = "SHOW TABLES LIKE '{}'".format(table)
        self.__cursor.execute(query)
        result = self.__cursor.fetchall()
        self.close()
        return result

    def dropTable(self, table):
        self.open()
        query = "DROP TABLE {}".format(table)
        self.__cursor.execute(query)
        self.close()


    ## Doesnt work atm

    # def update(self, table, n, **kwargs):
    #     query = "UPDATE %s SET " % table
    #     keys = kwargs.keys()
    #     values = kwargs.values()
    #     l = len(keys) - 1
    #     for i, key in enumerate(keys):
    #         query += key + " = '%s'" 
    #         if i < l:
    #             query += ","
    #     query += " WHERE name = '%s'" % n
    #     print(query)
    #     self.open()
    #     self.__cursor.execute(query, values)
    #     self.__connection.commit()
    #     self.close()

    # def delete(self, table, index):
    #     query = "DELETE FROM %s WHERE uuid=%d" % (table, index)
    #     self.open()
    #     self.__cursor.execute(query)
    #     self.__connection.commit()
    #     self.close()