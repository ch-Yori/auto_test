import pytest
from auto_test.common.common import read_excel,assert_res,send_request,assert_db
from auto_test.common.handle_extract import extract_res
from auto_test.common.handle_path import Excel_path

datas = read_excel(Excel_path,'下单流程')

@pytest.mark.parametrize('data',datas)
def test_shopcar(data):
    res = send_request(data)
    extract_res(res,data)
    assert_res(res,data)
    assert_db(data)






