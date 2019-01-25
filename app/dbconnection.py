import os
import psycopg2
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


class DbConnection:

    def __init__(self,):
        ''' Initializes a database connection '''
        if os.getenv('FLASK_ENV') == 'development':
            self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        else:
            self.conn = psycopg2.connect(os.getenv("DATABASE_TEST_URL"))
       
    def db_connection(self, app):
        """ Establishes connection to a database """
        return self.conn

    def get_connection(self):
        """ Returns a database connection """
        return self.conn

    def db_clean(self):
        """ Deletes everything from the Database """
        DROP_TABLES = """
                DROP SCHEMA public CASCADE;
                CREATE SCHEMA public;
                GRANT USAGE ON SCHEMA public TO postgres;;
        """
        return DROP_TABLES

    def create_database_tables(self):
        """ Create all database tables """
        
        TABLE_USERS = """ 
                             CREATE TABLE IF NOT EXISTS users (
                                Id serial PRIMARY KEY NOT NULL,
                                firstname VARCHAR (40) NOT NULL,
                                lastname VARCHAR (40) NOT NULL,
                                othername VARCHAR (40),
                                email VARCHAR (40) UNIQUE NOT NULL,
                                phone_number VARCHAR (40),
                                username VARCHAR (40) UNIQUE NOT NULL,
                                registered TIMESTAMP NOT NULL DEFAULT current_timestamp, 
                                password VARCHAR (256) NOT NULL,
                                IsAdmin VARCHAR (6) NULL DEFAULT 0
        );"""

        TABLE_MEETUPS = """ 
                            CREATE TABLE IF NOT EXISTS meetups (
                                Id serial PRIMARY KEY NOT NULL,
                                user_id INTEGER NOT NULL REFERENCES users(Id),
                                topic VARCHAR (90) NOT NULL,
                                happeningOn TIMESTAMP NOT NULL,
                                location VARCHAR (90) NOT NULL,
                                created_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
                                images VARCHAR (200) NULL,
                                tags VARCHAR(200) NULL
        );"""

        TABLE_QUESTIONS = """ 
                        CREATE TABLE IF NOT EXISTS questions (
                            Id serial PRIMARY KEY NOT NULL,
                            meetup_id INTEGER  REFERENCES meetups(Id),
                            created_by INTEGER NOT NULL REFERENCES users(Id),
                            created_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
                            title VARCHAR (150) NOT NULL,
                            body VARCHAR (1000) NOT NULL, 
                            votes INTEGER DEFAULT 0,   
                            constraint votes_non_negative check (votes >= 0)             
        );"""
        TABLE_RSVPS = """ 
                        CREATE TABLE IF NOT EXISTS rsvps (
                            Id serial PRIMARY KEY NOT NULL,
                            meetup_id INTEGER NOT NULL REFERENCES meetups(Id),
                            user_id INTEGER NOT NULL REFERENCES users(Id),
                            response VARCHAR (200)
        );"""
        TABLE_COMMENTS = """
                        CREATE TABLE IF NOT EXISTS comments(
                            Id serial PRIMARY KEY NOT NULL,
                            question_id INTEGER NOT NULL REFERENCES questions(Id),
                            created_by INTEGER NOT NULL REFERENCES users(Id),
                            created_on TIMESTAMP NOT NULL DEFAULT current_timestamp,
                            comment VARCHAR(200) NOT NULL
                        )
        """

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
                            '%s',
                            true
                        ) ON CONFLICT(email) DO NOTHING
        """ % (generate_password_hash('hello'))

        return [TABLE_USERS, TABLE_MEETUPS, TABLE_QUESTIONS, TABLE_COMMENTS,
                TABLE_RSVPS], ADMIN_USER

    def execute_queries(self):
        ''' Creates all the tables in application '''
        curs = self.get_connection().cursor()
        #curs.execute(self.db_clean())
        for query in self.create_database_tables()[0]:
            curs.execute(query)
        
    def commit_changes(self):
        """ Commits changes to database """
        self.get_connection().commit()

    def setUpTestDb(self):
        """ Sets up a test database """
        self.execute_queries()
        curs = self.get_connection().cursor()
        curs.execute(self.create_database_tables()[1])
        self.get_connection().commit()

    def destroyTestDb(self):
        """ Drop tables in test database """
        curs = self.get_connection().cursor()
        curs.execute(self.db_clean())
        self.get_connection().commit()

dbConn = DbConnection()
dbConn.setUpTestDb()
