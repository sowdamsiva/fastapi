from sqlalchemy import create_engine, MetaData, Table,Column,Integer,String, Select,Update,delete

DATABASE_URL = "postgresql://postgres:root@localhost:5432/postgres"
engine  = create_engine(DATABASE_URL,echo = False)
metadata = MetaData()

users = Table(
    "users_raw",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("name",String),
    Column("weight",Integer)
)
metadata.create_all(engine)

with engine.connect() as con:
    #create
    # con.execute(users.insert().values(name="suresh",weight=60))
    # con.execute(users.insert().values(name="rajesh",weight=70))
    # con.commit()

    #read
    all_users=con.execute(Select(users))
    print(all_users.fetchall())