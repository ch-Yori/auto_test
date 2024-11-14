import json,jsonpath
from loguru import logger
env_data = {}
def extract_res(res,casedata):
    logger.info('\n====================提取响应字段====================')
    '''
    :param res:url响应text
    :param casedata:测试用例中测试数据
    :return: 提取响应字段并存入env_data中
    '''
    extract_data = casedata['提取响应字段']
    if extract_data:
        dic = json.loads(extract_data)
        for k,v in dic.items():
            if v == "text":
                vaules = res.text
                logger.info(f'响应整体文本提取{vaules}')
            else:
                try:
                    vaules = jsonpath.jsonpath(res.json(),v)[0]
                    logger.info(f'json{k}提取到的字段的值是{vaules}')
                except Exception as e:
                    print(f'提取响应字段失败，请确认{v}是否与JSONPATH表达式一致')
                    raise e
            env_data[k] = vaules



