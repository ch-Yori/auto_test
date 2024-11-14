from faker import Faker
from auto_test.common.handle_db import query_db

faker = Faker(locale='zh-CN')

def get_unregister_phone():
    f = Faker(locale="zh-CN")
    # 随机的手机号码  -- 有可能随机生成的数据已经有被注册过了，得需要保证我们的手机号码不存在于数据库中
    while True:
        # 1、通过faker库构造随机的手机号码
        user_phone = f.phone_number()
        # 2、执行SQL语句检查数据是否被使用过
        sql = f'select count(*) from tz_user where user_mobile = "{user_phone}";'
        result = query_db(sql,"one")[0]
        # 3、判断result，如果result结果为1就代表有被使用过，所以我们需要再一次生成新的手机号码，如果为0则代表数据满足要求
        if result == 0:
            break
    return user_phone

def get_unregister_username():
    while True:
        user_name = faker.user_name()
        # 这里缺少一个使用sql查询
        sql = f'select count(*)from tz_user where user_name = "{user_name}"'
        result = query_db(sql,"one")[0]
        if result == 0 and len(user_name) > 4 and len(user_name) < 16:   #判断用户名是否使用过，如果使用过跳出循环
            break
    return user_name



