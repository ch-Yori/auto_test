import json,jsonpath,openpyxl
from requests import request
from string import Template
from auto_test.common.handle_extract import env_data
from auto_test.common.handle_db import query_db
from loguru import logger
#读取Excel表格测试用例数据封装函数
def read_excel(file_name, sheet_name):
    '''
    :param file_name: 测试用例表格文件名
    :param sheet_name: 测试用例sheet名
    :return: 列表嵌套字典格式的测试数据
    '''
    wb = openpyxl.load_workbook(file_name)
    sheet = wb[sheet_name]
    li = list(sheet.values)
    data_list = []
    header = li[0]
    for data in li[1:]:
        dic = dict(zip(header, data))
        data_list.append(dic)
    return data_list
#接口请求封装函数
def send_request(Excel_data):
    '''
    :param Excel_data: 测试用例中测试数据
    :return: GET、POST等请求
    '''
    method = Excel_data['请求方式']
    headers = Excel_data['请求头']
    params = Excel_data['请求参数']
    url =    Excel_data['请求地址']

    url = Template(url).safe_substitute(env_data)                #将res中的数据提取出来并替换到url中
    if headers:
        headers = Template(headers).safe_substitute(env_data)
        headers= json.loads(headers)
    if params:
        params = Template(params).safe_substitute(env_data)
    res = None
    if method.upper()=='GET' or method.upper=='DELECT':
        if params:
            res = request(method,url,headers=headers,params=json.loads(params))
        else:
            res = request(method,url,headers=headers)
    elif method == 'POST' or method.upper() == 'PUT':
        if 'application/json' in headers['Content-Type']:
            res = request(method,url,headers=headers,json=json.loads(params))
        elif 'multipart/form-data' in headers['Content-Type']:
            #文件传参
            res = request(method,url,headers=headers,files=eval(params))
        elif 'application/x-www-form-urlencoded' in headers['Content-Type']:
            res = request(method,url,headers=headers,data=json.loads(params))
    logger.info('\n====================接口请求参数====================')
    logger.info(f'请求地址:{url}')
    logger.info(f'请求参数:{params}')
    logger.info(f'请求方法:{method}')
    logger.info(f'请求头:{headers}')
    if res:
        logger.info('\n====================接口响应参数====================')
        logger.info(f'响应状态码:{res.status_code}')
        logger.info(f'响应体:{res.text}')
        # logger.info(f'响应时间{res.elapsed.total_seconds()}')

    return res
# 接口断言统一封装
def assert_res(res,casedata):
    logger.info('\n====================接口响应断言====================')
    '''
    :param res: 请求响应文本
    :param casedata: 测试用例中测试数据
    :return: 断言结果
    '''
    if casedata['预期结果']:
        for k,v in json.loads(casedata['预期结果']).items():
            if k == 'Status Code':
                logger.info(f'接口响应断言-状态码，指望值{v}，实际值{res.status_code}')
                assert res.status_code == v
            elif k == 'text':
                logger.info(f'接口响应断言-整体文本，指望值{v}，实际值{res.text}')
                assert res.text == v
            elif k[0] == '$':
                logger.info(f'接口响应断言-JSOn提取，指望值{v}，实际值{jsonpath.jsonpath(res.json(),v)}')
                assert jsonpath.jsonpath(res.json(),v) == v
            else:
                print('暂时还没有')


def assert_db(data):
    logger.info('\n====================数据库断言====================')
    if data['数据库断言']:
        dic = json.loads(data['数据库断言'])
        for k,v in dic.items():
            k = Template(k).safe_substitute(env_data)
            v = Template(str(v)).safe_substitute(env_data)
            actul = str(query_db(k,'one')[0])
            logger.info(f'数据库断言，执行的SQL语句{k}期望值{v}，实际值{actul}')
            assert actul == v