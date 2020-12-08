import pyodbc

# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15
import pandas
import os

def ToMsSql(YaoPinName:list, gongsiid:int):
    """

    :param YaoPinName: xpath 过滤后的目标数据
    :param gongsiid: 目标公司名称对应的 id 号
    :return:
    """
    driver = "{ODBC Driver 17 for SQL Server}"
    server = "192.168.0.84"
    username = "sa"
    password = "0impus"
    database = "BI_2"
    port = 1433
    conn = pyodbc.connect('DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format(driver, server, database, username, password))
    cursor = conn.cursor()
    if len(YaoPinName) < 4:
        for _ in range(4 - len(YaoPinName)):
            YaoPinName.append("缺")
    elif len(YaoPinName) > 4:
        for _ in range(len(YaoPinName) - 4):
            YaoPinName.pop()

    ShangPinName, ShengChanChangJia, JiaGe, XiaoLiang = [i for i in YaoPinName]
    cursor.execute("insert into DaiFenxi_SourceData (ShangPinName,ShengChanChangJia,JiaGe,XiaoLiang,GongSiMingCheng) values('{}','{}','{}','{}','{}')".format(ShangPinName, ShengChanChangJia, JiaGe, XiaoLiang, int(gongsiid)))
    cursor.commit()
    conn.close()




def ToCsv(YaoPinName:list, name):
    """
    天猫
    :param YaoPinName:
    :param name: excel 文件名称
    :return:
    """
    if len(YaoPinName) < 3:
        for _ in range(3 - len(YaoPinName)):
            YaoPinName.append("缺")
    elif len(YaoPinName) > 3:
        for _ in range(len(YaoPinName) - 3):
            YaoPinName.pop()

    datafrname = pandas.DataFrame(
        {
        "Info0": YaoPinName[0],
        "Info1": YaoPinName[1],
        "Info2": YaoPinName[2],
        }, index=[0])
    datafrname.to_csv("{}{}-YaoJingCai.csv".format(os.path.join(os.path.expanduser("~"), 'Desktop') + '\\', name), header=False, mode='a',index=False)

def ToCsv_JingDong(YaoPinName:list, name):
    """
    药京采
    :param YaoPinName:
    :param name: excel 文件名称
    :return:
    """
    if len(YaoPinName) < 4:
        for _ in range(4 - len(YaoPinName)):
            YaoPinName.append("缺")
    elif len(YaoPinName) > 4:
        for _ in range(len(YaoPinName) - 4):
            YaoPinName.pop()

    datafrname = pandas.DataFrame(
        {
        "Info0": YaoPinName[0],
        "Info1": YaoPinName[1],
        "Info2": YaoPinName[2],
        "Info3": YaoPinName[3],
        }, index=[0])
    datafrname.to_csv("{}{}-YaoJingCai.csv".format(os.path.join(os.path.expanduser("~"), 'Desktop') + '\\', name), header=False, mode='a',index=False)