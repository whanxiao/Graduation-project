import pandastest as pd
import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://root:root@127.0.0.1:3306/pl')

sql='''
select content from question where commodity_id=1;
'''
df = pd.read_sql(sql,engine)
