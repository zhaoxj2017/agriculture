from db.DBUtils import *


def create_table_crops(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS crops")
    cursor.execute('''create table crops( \
            id int auto_increment primary key,\
            vegetables varchar(255) not null\
            )
            default charset = utf8
            ''')


def create_table_crops_area(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS crops_area")
    cursor.execute('''create table crops_area(\
            id int auto_increment primary key,\
            varieties varchar(30) not null,\
            area varchar(50) null,\
            low_price varchar(10) null,\
            high_price varchar(10) null,\
            avg_price varchar(10) null,\
            mea_unit varchar(20) null,\
            date_time varchar(40) null\
            )
            default charset = utf8
            ''')


def create_table_district(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS district")
    cursor.execute('''create table district(\
            id int auto_increment primary key,\
            provence varchar(30) not null,\
            city varchar(30) not null,\
            district varchar(50) not null,\
            datetime varchar(30) not null\
            )
            default charset = utf8
            ''')


def create_tables():
    conn = get_instance()
    # create_table_crops(conn)
    create_table_crops_area(conn)
    # create_table_district(conn)
    close(conn)


if __name__== "__main__":
    create_table_district()