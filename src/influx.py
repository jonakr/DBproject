from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class Influx:

    __token = None
    __org = None
    __bucket = None
    __url = None

    __client = None

    def __init__(self, token, org, bucket, url):
        self.__token = token
        self.__org = org
        self.__bucket = bucket
        self.__url = url

    def open(self):
        # TODO: Try Except
        client =  InfluxDBClient(url=self.__url, token=self.__token)
        self.__client = client

    def close(self):
        self.__client.close()

    def write(self, data):
        self.open()
        write_api = self.__client.write_api(write_options=SYNCHRONOUS)
        write_api.write(self.__bucket, self.__org, data, write_precision='s')
        self.close()

    def query(self, query, df=False):
        self.open()
        if df:
            result = self.__client.query_api().query_data_frame(query, org=self.__org)
        else:
            result = self.__client.query_api().query(query, self.__org)
        self.close()
        return result