import schedule
import time
import random
from urllib.request import urlopen
from urllib.parse import urlencode
import yaml
import os

''''
Poster.py 为疫情防控程序，自动在每天的固定时间完成一次表单提交，避免被导员点名。
不会占用很大的内存，杀次改进程的话提醒一下-。-

使用nohup命令常驻于后台，关闭终端时命令仍会运行

留下一些常用命令，方便操作：
* 运行文件
        nohup python3 -u Poster.py > poster.log 2>&1 &
* 查看进程、查看是否正在运行
        ps -ef|grep python3
* 删除进程
        kill -9 进程号
'''

# 加载用户配置
def load_config(filepath):
    KEYS = ['wid', 'userId', 'DATETIME_CYCLE', 'DWMC_698799', 'XGH_273694', 'XM_941836', 'PICKER_817983', 'TEXTAREA_941289', 'PICKER_917327', 'TEXTAREA_224871', 'PICKER_670104', 'TEXTAREA_823223', 'RYLB_840581', 'RADIO_587182', 'TEXT_230226', 'TEXT_76579', 'TEXT_1961', 'TEXTAREA_355679', 'TEXT_814184', 'TEXTAREA_529533', 'TEXTAREA_592090']
    with open(filepath, "r", encoding="utf-8") as f:
        tempList = yaml.safe_load(f)
    return [dict(zip(KEYS, data.values())) for data in tempList]

# 填报主体，发送请求填报，未对失败情况进行处理。
# 足够完善的话可以调用API集成短信提醒之类的
def post(forms):
    url='http://yqtb.sdnu.edu.cn/pdc/formDesignApi/dataFormSave'
    for data in forms:
        # 每天需修改时间
        data['DATETIME_CYCLE'] = time.strftime("%Y/%m/%d", time.localtime())

        s = urlencode(data)
        res = urlopen(url,s.encode()).read().decode('utf-8')
        # 判断是否填报成功，填报失败则发送邮件提醒。
        curdate = time.strftime("%Y/%m/%d %H:%M", time.localtime())
        if('true' in res):
            print(curdate, data['XM_941836'], "填报成功")
        else:
            print('warning:',curdate, data['XM_941836'], "填报失败")
    
    print("-"*10, "total:", len(forms) , "-"*10)

# 循环执行主体
def run():
    path = "./config.yml"
    # path = os.path.join(".", "config.yml")
    forms = load_config(path)
    post(forms)

if __name__=="__main__":
    run()
    # 随机时间
    # RANDOM_TIME = f"07:{random.randint(10,59)}"
    POST_TIME ='08:00'
    schedule.every().day.at(POST_TIME).do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
