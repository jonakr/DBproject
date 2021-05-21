from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

class Influx:
    """
    A class used to connect to a InfluxDB Cloud 2.0
    and write or query data from it.

    ...

    Attributes
    ----------
    __token : str
        the token to connect to the database
    __org : str
        the org in which the bucket is located
    __bucket : str
        the bucket the data will be written to or querried from
    __url : str
        the url of the used InfluxDB Cloud 2.0
    __client : object
        contains the connection

    Methods
    -------
    __open()
        opens the connection to the database
    __close
        closes the connection to the database
    write(data)
        receives data to write to the database
    query(query, df=False)
        queries data from the database (can be returned as data frame)
    """

    __token = None
    __org = None
    __bucket = None
    __url = None

    __client = None

    def __init__(self, token, org, bucket, url):
        """
        Parameters
        ----------
        token : str
            the token to connect to the database
        org : str
            the org in which the bucket is located
        bucket : str
            the bucket the data will be written to or querried from
        url : str
            the url of the used InfluxDB Cloud 2.0
        """

        self.__token = token
        self.__org = org
        self.__bucket = bucket
        self.__url = url

    def __open(self):
        """
        opens connection to database and sets __client attribute

        Raises
        ------
        Exception
            throws error if connection fails
        """

        try:
            client = InfluxDBClient(url=self.__url, token=self.__token)
            self.__client = client
        
        except Exception as err:
            print("Something went wrong: {}".format(err))

    def __close(self):
        """
        closes the connection to the database
        """

        self.__client.close()

    def write(self, data):
        """
        Receives data to write to the database

        Parameters
        ----------
        data : str
            data that is written to the database with the following structure:
            "bucket,host=host1 data1=,data2=,... timestamp"
        """

        self.__open()
        write_api = self.__client.write_api(write_options=SYNCHRONOUS)
        write_api.write(self.__bucket, self.__org, data, write_precision='s')
        self.__close()

    def query(self, query, df=False):
        """
        Querys data from the database

        Parameters
        ----------
        query : str
            the query string to query from the database
        df : bool
            can be set to true to return the query as data frame
        """

        self.__open()
        if df:
            result = self.__client.query_api().query_data_frame(query, org=self.__org)
        else:
            result = self.__client.query_api().query(query, self.__org)
        self.__close()
        return result
