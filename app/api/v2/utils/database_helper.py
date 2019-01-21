""" Contains helper functions related to database transactions """
import psycopg2
from psycopg2.extras import DictCursor
from flask import jsonify
from app.dbconnection import DbConnection


class DatabaseHelper:
    def __init__(self):
        ''' Creates an admin user '''
        self.conn = DbConnection().db_connection()

    def insert_into_db(self, table, columns, values, record):
        """ INSERT INTO A TABLE """
        cursor = self.conn.cursor()
        sql = "INSERT INTO {table} ({col}) VALUES ({val})".format(table=table,
                                                                  col=columns,
                                                                  val=values)

        try:
            cursor.execute(sql)
        except:
            return jsonify({'msg': '{} not added successfully'.format(record),
                            'status': 400}), 400
        self.conn.commit()
        return jsonify({'msg': '{} added successfully'.format(record),
                        'status': 201}), 201

    def find_in_db(self, table, field):
        """ Find an Item in a database """
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * FROM {table} WHERE {field} ".format(table=table,
                                                            field=field)
        cursor.execute(sql)
        row = cursor.fetchall()
        return self.result_in_dict(row)
    
    def result_in_dict(self, rows):
        """ Returns a dictionary with results """
        dict_result = []
        for row in rows:
            dict_result.append(dict(row))
        return dict_result

    def update_record(self, table, flag, id):
        """ Updates a record in a database """
        cursor = self.conn.cursor()
        query = "UPDATE {table} SET flag = {flag} WHERE id = {id}".format(table,
                                                                          flag, id)
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
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * FROM {table} ".format(table=tbl)
        cursor.execute(sql)
        row = cursor.fetchall()
        return self.result_in_dict(row)

    def update_columns_record(self, table, flag, key, id):
        """ Updates a record in a database """
        cursor = self.conn.cursor()
        sql = "UPDATE {table} SET {flag} WHERE {key} = {id}".format(table=table,
                                                                    flag=flag,
                                                                    key=key,
                                                                    id=id)
        try:
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
        except:
            self.conn.rollback()
            return jsonify({'msg': 'Update was not successful'}), 400 
        return jsonify({'msg': 'Update was successful'}), 201 
