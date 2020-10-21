
import mysql.connector
import sql_params

class SQL_Credentials:

    def __init__(self):

        self.creds = sql_params.sql_credentials()

    def authenticate(self, db=None):

        if db == None:

            creds = {

                'host': 'localhost',
                'user': self.creds['user'],
                'password': self.creds['password']
            }

            return creds 
        
        else:

            creds = {

                'host': 'localhost',
                'user': self.creds['user'],
                'password': self.creds['password'],
                'database': db
            }

            return creds


class SQL_Cli:

    def __init__(self, db=None):

        self.auth = SQL_Credentials().authenticate(db)
        self.db = mysql.connector.connect( 

            host=self.auth['host'],
            user=self.auth['user'],
            password=self.auth['password'],
            database=self.auth['database']

        )

    def execute(self, query):

        cursor = self.db.cursor()
        print('Connection Established')
        cursor.execute(query)
        cursor.close()

        return print('Query Executed')

    def insert(self, query):

        cursor = self.db.cursor()
        print('Connection Established')
        cursor.execute(query)
        self.db.commit()
        cursor.close()

        return print(f'Row Count: {cursor.rowcount} inserted')

    def fetch(self, query):

        cursor = self.db.cursor()
        print('Connection Established')
        cursor.execute(query)
        res = cursor.fetchall()
        print('Query Fetched')
        cursor.close()

        for r in res:
            print(f'Line: {r}')

        return res


def read_sql(file):

    sql = open(file)
    sql = sql.read()
    sql = sql.split(';')

    return sql







    