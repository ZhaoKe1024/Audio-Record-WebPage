import pandas as pd
from sqlalchemy import create_engine


# from sqlalchemy.ext.declarative import declarative_base

def sqlalchemy_test():
    ENGINE = create_engine("mysql+pymysql://root:zkGcx_0703@127.0.0.1:3306/cough_schema")
    sql = """
        select * from cough_main;
        """
    df = pd.read_sql(sql, ENGINE)
    print(df)


if __name__ == "__main__":
    sqlalchemy_test()
