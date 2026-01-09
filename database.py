import mysql.connector
import pandas as pd
import os

from dotenv import load_dotenv


class DB:
    def __init__(self):
        load_dotenv()
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )

            self.myCursor = self.conn.cursor(buffered=True)
            print("connection established")
        except Exception as e:
            print(f"connection error:{e}")

    def fetching_city(self):
       city=[]
       self.myCursor.execute ("""   SELECT distinct(Source) FROM flights.planes
                            UNION 
                                select distinct(Destination) FrOM flights.planes""")
       data = self.myCursor.fetchall()
       for item in data:
           city.append(item[0])
       return city

    def fetching_flights(self,Sources,Destination):
        query= """
                                SELECT airline, flight, Source,Destination,duration,price FROM planes
                                where Source = %s And Destination = %s
                                """
        try :

            df= pd.read_sql(query,self.conn, params=(Sources, Destination))

            return df.head(11)
        except Exception as e:
            print(f"Error fetching flights: {e}")
            return pd.DataFrame()


    def fetching_count(self):
        airline=[]
        count=[]
        query= """
        SELECT airline,count(*) FROM flights.planes
        GRoup by airline 
        """
        self.myCursor.execute(query)
        count_data=self.myCursor.fetchall()
        for item in count_data:
            airline.append(item[0])
            count.append(item[1])

        return airline,count