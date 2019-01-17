import os
import psycopg2

DATABASE_URL="dbname='questioner' host='localhost' user='postgres' password='emily' port='5432'"


class DbConnection:

    def db_connection(self):
        """ Establishes connection to a database """
        global DATABASE_URL
        self.conn = psycopg2.connect(DATABASE_URL)
        return self.conn

    def get_connection(self):
        """ Returns a database connection """
        return self.conn

    def db_clean(self):
        """ Deletes everything from the Database """
        DROP_DATABASE = """
                DROP SCHEMA public CASCADE;
                CREATE SCHEMA public;
                GRANT USAGE ON SCHEMA public TO postgres;;
        """
        return DROP_DATABASE

    def create_database_tables(self):
        """ Create all database tables """

        TABLE_USERS = """ 
                             CREATE TABLE IF NOT EXISTS users (
                                Id serial PRIMARY KEY NOT NULL,
                                firstname VARCHAR (40) NOT NULL, 
                                lastname VARCHAR (40) NOT NULL, 
                                othername VARCHAR (40),
                                email VARCHAR (40) NOT NULL, 
                                phone_number VARCHAR (40),
                                username VARCHAR (40) NOT NULL,
                                registered TIMESTAMP NOT NULL DEFAULT current_timestamp, 
                                password VARCHAR (256) NOT NULL,
                                IsAdmin VARCHAR (20) DEFAULT false
        );"""

        TABLE_MEETUPS = """ 
                            CREATE TABLE IF NOT EXISTS meetups (
                                Id serial PRIMARY KEY NOT NULL,
                                user_id INTEGER NOT NULL,
                                topic VARCHAR (90) NOT NULL,
                                happeningOn TIMESTAMP NOT NULL,
                                location VARCHAR (90) NOT NULL,
                                created_on TIMESTAMP NOT NULL DEFAULT current_timestamp
        );"""

        TABLE_QUESTIONS = """ 
                        CREATE TABLE IF NOT EXISTS questions (
                            Id serial PRIMARY KEY NOT NULL,
                            meetup_id INTEGER NOT NULL, 
                            created_by INTEGER NOT NULL, 
                            created_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
                            title VARCHAR (150) NOT NULL,
                            body VARCHAR (1000) NOT NULL, 
                            votes INTEGER DEFAULT 0                
        );"""
        TABLE_RSVPS = """ 
                        CREATE TABLE IF NOT EXISTS rsvps (
                            Id serial PRIMARY KEY NOT NULL,
                            meetup_id INTEGER NOT NULL, 
                            user_id INTEGER NOT NULL, 
                            response VARCHAR (200)
        );"""

        ADMIN_USER = """
                        INSERT INTO users(firstname,lastname,
                                          othername,email,phone_number,
                                          username,registered,password,isadmin) VALUES(
                            'Super Admin',
                            'Gicheha',
                            'Mwangi',
                            'mwangi@gmail.com',
                            '0724603546',
                            'Izzo',
                            current_timestamp,
                            'hello,world',
                            1
                        )
        """

        return [TABLE_USERS,TABLE_MEETUPS,TABLE_QUESTIONS,TABLE_RSVPS,ADMIN_USER]

    def execute_queries(self):
        curs = self.get_connection().cursor()

        for query in self.create_database_tables():
            curs.execute(query)

    def commit_changes(self):
        """ Commits changes to database """    
        self.get_connection().commit()

    def setUpTestDb(self):
        """ Sets up a test database """
        self.execute_queries()
        self.db_clean()


'''db = DbConnection()
db.db_connection(DATABASE_URL)
db.execute_queries()
db.commit_changes()'''

        
