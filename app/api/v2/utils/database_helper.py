""" Contains helper functions related to database transactions """
from flask import jsonify
from app.dbconnection import DbConnection

class DatabaseHelper:
    def __init__(self):
        ''' Creates an admin user '''
        self.conn = DbConnection().db_connection()

    def insert_into_db(self, table, columns, values, record):
        """ INSERT INTO A TABLE """
        cursor= self.conn.cursor()
        sql = "INSERT INTO {table} ({col}) VALUES ({val})".format(table = table, col = columns, val = values)
        #return jsonify({'msg':sql})
        cursor.execute(sql)
        self.conn.commit()
        return jsonify({'msg': '{} added successfully'.format(record), 'status':201}), 201
        

    def find_in_db(self, table , field):
        """ Find an Item in a database """
        cursor = self.conn.cursor()
        sql = "SELECT * FROM {table} WHERE {field} ".format(table=table, field=field)
        cursor.execute(sql)
        row = cursor.fetchone()
        return row
        

    def update_record(self, table, flag, id ):
        """ Updates a record in a database """
        cursor = self.conn.cursor()
        query = "UPDATE {table} SET flag = {flag} WHERE id = {id}".format(table,flag,id)
        print(query)
        cursor.execute(query)

    def delete_record(self, table, field, flag):
        """ Deletes a record from the database """
        cursor = self.conn.cursor()
        query = "DELETE FROM {table} WHERE {field} = {flag}".format(table=table, field=field, flag=flag)
        cursor.execute(query)
        self.conn.commit()

    def fethall_records(self, tbl):
        """ Fetch all records in a database """
        cursor = self.conn.cursor()
        sql = "SELECT * FROM {table} ".format(table=tbl)
        cursor.execute(sql)
        row = cursor.fetchall()
        return row

    def update_columns_record(self, table, flag, key, id ):
        """ Updates a record in a database """
        cursor = self.conn.cursor()
        query = "UPDATE {table} SET {flag} WHERE {key} = {id}".format(table,flag,key,  id)
        print(query)
        cursor.execute(query)
