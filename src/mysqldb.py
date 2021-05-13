import mysql.connector


class Mysql:
    """
    A class used to connect a MySQL database

    ...

    Attributes
    ----------
    __host : str
        the host of the MySQL database
    __user : str
        the user to login
    __password : str
        the password to login
    __database : str
        the database to connect to
    __cursor : object
        the cursor to write and query data with
    __connection : object
        the database connection that is made 

    Methods
    -------
    open()
        open connection to database
    close()
        close connection to database
    insert(table, *args, **kwargs)
        insert data into table
    select(table, where=None, *args)
        select data from table
    execute(sql)
        execute sql string
    addTable(template)
        add table to database
    checkIfTableExists(table)
        check if the table exists
    dropTable(table)
        drop table from database
    """

    __host = None
    __user = None
    __password = None
    __database = None

    __cursor = None
    __connection = None

    def __init__(self, host, user, password, database):
        """
        Parameters
        ----------
        host : str
            the host of the MySQL database
        user : str
            the user to login
        password : str
            the password to login
        database : str
            the database to connect to
        """

        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def open(self):
        """
        Opens a connection to MySQL database and creates cursor

        Raises
        ------
        mysql.connector.Error
            throws error if connection fails
        """

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
            print("Something went wrong: {}".format(err))

    def close(self):
        """
        Closes the connection to cursor and database
        """

        self.__cursor.close()
        self.__connection.close()

    def insert(self, table, *args, **kwargs):
        """
        Inserts data to a table in the database

        Parameters
        ----------
        table : str
            the table to insert data to
        *args : array of str
            every value to insert
        **kwargs : array of str, optional
            every where argument
        """

        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = kwargs.values()
            query += "(" + ",".join(["`%s`"]*len(keys)) % tuple(keys) + \
                ") VALUES(" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

        self.open()
        self.__cursor.execute(query, values)
        self.__connection.commit()
        self.close()
        return self.__cursor.lastrowid

    def select(self, table, where=None, *args):
        """
        Select data from a table in the database

        Parameters
        ----------
        table : str
            the table to select data from
        where : str
            set the where option
        *args : array of str
            every value that is selected
        """

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

    def execute(self, sql):
        """
        Execute a SQL statement that isn't implemented as function.

        Parameters
        ----------
        sql : str
            the sql statement to execute
        """

        self.open()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        self.close()
        return result

    def addTable(self, template):
        """
        Add a table to the database.

        Parameters
        ----------
        template : str
            the template that contains all configurations for the table
        """

        self.open()
        self.__cursor.execute(template)
        self.close()

    def checkIfTableExists(self, table):
        """
        Check if a table exists inside the database.

        Parameters
        ----------
        table : str
            the table that is searched
        """

        self.open()
        query = "SHOW TABLES LIKE '{}'".format(table)
        self.__cursor.execute(query)
        result = self.__cursor.fetchall()
        self.close()
        return result

    def dropTable(self, table):
        """
        Drop a table from the database.

        Parameters
        ----------
        table : str
            the table that is dropped
        """

        self.open()
        query = "DROP TABLE {}".format(table)
        self.__cursor.execute(query)
        self.close()
