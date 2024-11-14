import pytest
from auto_test.common.handle_db import query_db
from auto_test.common.common import read_excel,assert_res,send_request
from auto_test.common.handle_extract import extract_res
from auto_test.common.handle_data import get_unregister_phone,get_unregister_username
from auto_test.common.handle_extract import env_data
from auto_test.common.handle_path import Excel_path

datas = read_excel(Excel_path,'注册流程')

user_name = get_unregister_username()
user_phone = get_unregister_phone()
env_data["user_phone"] = user_phone
env_data["user_name"] = user_name

@pytest.mark.parametrize('data',datas)
def test_region(data):
    res = send_request(data)
    if data['用例编号'] == 1:
        #从数据库中获取验证码
        sql = f'select mobile_code from tz_sms_log where user_phone = "{user_phone}" order by rec_date desc limit 1;'
        mobile_code = query_db(sql, 'one')[0]
        env_data["mobile_code"] = mobile_code
    extract_res(res,data)
    assert_res(res,data)






