import os
import psycopg2

DATABASE_URL="dbname='questioner' host='localhost' user='postgres' password='emily' port='5432'"

conn = psycopg2.connect(DATABASE_URL)

print('connected successfully')

curs = conn.cursor()


conn.commit()
conn.close()

