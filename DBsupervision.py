import os
import sqlite3

class PropertiesBase:
    """Class to operate database"""
    def __init__(self):
        self.path = './bin/lasstat.db'
        self.property_table = 'curves_propertyes'
        self.alias_table = 'curves_alias'

    def show_data_from(self, table):
        """Show data from table in DB"""
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        sql = F"SELECT * FROM {table}"
        self.cur.execute(sql)
        records = self.cur.fetchall()
        for record in records:
            print(record)
        self.con.close()
        return records

    def get_data_from_table(self, table):
        """Show data from table in DB"""
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        sql = F"SELECT * FROM {table}"
        self.cur.execute(sql)
        records = self.cur.fetchall()
        self.con.close()
        return records

    def connection_to_modify(function):
        """Decorator to modify database according to query from function"""
        def wrapped(self, *args):
            self.con = sqlite3.connect(self.path)
            self.cur = self.con.cursor()
            sql = function(self, *args)
            print(sql)
            self.cur.execute(sql)
            self.con.commit()
            self.con.close()
        return wrapped

    def create_database(self):
        """Create db"""
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        sql = F"create table if not exists {self.property_table} (id, 'curve_name', 'color', 'units', 'min', 'max', 'scale', 'description', 'type')"
        self.cur.execute(sql)
        sql = F"create table if not exists {self.alias_table} ('id', 'curve', 'alias_list')"
        self.cur.execute(sql)
        self.con.commit()
        self.con.close()


    @connection_to_modify
    def add_curve_properties(self, *args):
        """Add record in curves properties table"""
        return F"INSERT INTO {self.property_table} VALUES ({args[0]['id']}," \
               F" '{args[0]['curve_name']}', '{args[0]['color']}', '{args[0]['units']}'," \
               F" '{args[0]['min']}', '{args[0]['max']}', '{args[0]['scale']}'," \
               F" '{args[0]['description']}', '{args[0]['type']}')"

    @connection_to_modify
    def add_alias(self, *args):
        """Add record aliases table"""
        return F"INSERT INTO {self.alias_table} VALUES ({args[0]['id']}," \
               F" '{args[0]['curve']}', '{args[0]['alias_list']}')"

    @connection_to_modify
    def delete_table(self, *args):
        """Delete table from DB"""
        return F"DROP TABLE IF EXISTS {args[0]}"

    @connection_to_modify
    def delete_record_by_id(self, *args):
        """Delete record by id from DB table"""
        return F"DELETE FROM {args[0]} WHERE id = {int(args[1])}"


def main():
    path = './bin/lasstat.db'
    base = PropertiesBase()
    #base.create_database()
    #test_props = {'id':0, 'curve_name':'missing', 'color':'black', 'units':'missing', 'min':'missing', 'max':'missing', 'scale':'missing', 'description':'missing', 'type':'missing'}
    #base.add_curve_properties(test_props)
    #test_alias = {'id':2, 'curve':'GR', 'alias_list':'GR, GK, GR_LWD'}
    #base.add_alias(test_alias)
    #base.delete_table(base.alias_table)
    #base.show_data_from(base.property_table)
    #base.delete_record_by_id(base.property_table, 3)
    #base.show_data_from(base.property_table)


if __name__ == '__main__':
    main()
