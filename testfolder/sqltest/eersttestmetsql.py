import sqlite3 as sl
con = sl.connect('my-test.db')
def createtableuser():
    with con:
        con.execute("""
            CREATE TABLE USER (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            );
        """)

def insertdata():
    sql = 'INSERT INTO USER (id, name, age) values(?, ?, ?)'
    data = [
        (1, 'Alice', 21),
        (2, 'Bob', 22),
        (3, 'Chris', 23)

]
    return sql,data
#sql,data=insertdata()
#with con:
#    con.executemany(sql, data)

with con:
    data = con.execute("SELECT * FROM USER WHERE age <= 22")
    for row in data:
        print(row)


with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS provider (
        provider_name text,
        owner text
        );
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS regios (
            regio_name text,
            provider_naam text,
            FOREIGN KEY (provider_naam) REFERENCES provider (provider_name)
        
        );
    """)
    con.execute("""
          CREATE TABLE IF NOT EXISTS network (
            network_name text,
            range text, 
            provider_naam text,
            FOREIGN KEY (provider_naam) REFERENCES provider (provider_name)
            
        );""")
    con.execute("""
          CREATE TABLE IF NOT EXISTS elasticips (
            ipaddress text,
            provider_naam text,
            network_name text,
            FOREIGN KEY (network_name) REFERENCES network (network_name)
            FOREIGN KEY (provider_naam) REFERENCES provider (provider_name)
            
        );""")
    con.execute("""
        CREATE TABLE IF NOT EXISTS instances (
            id text PRIMARY KEY,
            nametag text,
            ip_address text,            
            status text,
            description text,
            regio_name text,
            elasticip_address text,
            network text,
            provider_naam text,
            FOREIGN KEY (regio_name) REFERENCES regios (regio_name),
            FOREIGN KEY (elasticip_address) REFERENCES elasticip (elasticip_address),
            FOREIGN KEY (network) REFERENCES network (network_name),
            FOREIGN KEY (provider_naam) REFERENCES provider (provider_name)
	
);
    """)

con.close()