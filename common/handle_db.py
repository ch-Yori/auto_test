import pymysql
from loguru import logger
# 获取MySQL数据库连接对象,并根据sql语句进行查询

def query_db(sql, type="one", num=0):
    '''
    :param sql: 数据库查询指令
    :param type: 查询类型多条、单条、所有
    :param num: 查询多条时查询数量
    :return: 查询结果
    '''
    # logger.info(f'正在查询的sql指令是{sql}')
    conn = pymysql.connect(host='shop.lemonban.com', port=3306, user='lemon_auto',
                           password='lemon!@123', database='yami_shops', charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)                      # 使用游标对象cur来执行SQL语句
    if type == "one":
        result = cur.fetchone()
    elif type == "many":
        result = cur.fetchmany(num)
    elif type == "all":
        result = cur.fetchall()
    else:
        print("type类型指定有误，需要指定以下三种之一：fetchone、fetchmany、fetchall")
        result = None
    # 关闭数据库
    conn.close()
    return result