import psycopg2.extras

DATABASE = psycopg2.connect(user='flask', password='blogappflask', database='blog',
                            cursor_factory=psycopg2.extras.RealDictCursor)
DATABASE.autocommit = True

COOKIE_NAME = 'MSTID'
