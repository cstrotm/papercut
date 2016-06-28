# Copyright (c) 2002 Joao Prado Maia. See the LICENSE file for more information.
import MySQLdb
import papercut.settings

settings = papercut.settings.CONF()

class Papercut_Auth:
    """
    Authentication backend interface
    """

    def __init__(self):
        self.conn = MySQLdb.connect(host=settings.dbhost, db=settings.dbname, user=settings.dbuser, passwd=settings.dbpass)
        self.cursor = self.conn.cursor()

    def is_valid_user(self, username, password):
        stmt = """
                SELECT
                    password
                FROM
                    papercut_groups_auth
                WHERE
                    username='%s'
                """ % (username)
        num_rows = self.cursor.execute(stmt)
        if num_rows == 0 or num_rows is None:
            settings.logEvent('Error - Authentication failed for username \'%s\' (user not found)' % (username))
            return 0
        db_password = self.cursor.fetchone()[0]
        if db_password != password:
            settings.logEvent('Error - Authentication failed for username \'%s\' (incorrect password)' % (username))
            return 0
        else:
            return 1

