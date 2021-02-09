import schedule
import time
from urllib.request import urlopen
from urllib.parse import urlencode

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class Poster():
    
    # post数据，wid可能是固定校验字段，其余数据为表单数据
    dataList = [{'wid':'','userId':'',
               'DATETIME_CYCLE':'','DWMC_698799':'',
               'XGH_273694':'','XM_941836':'',
               'PICKER_817983':'','TEXTAREA_941289':'',
               'PICKER_917327':'','TEXTAREA_224871':'',
               'PICKER_670104':'','TEXTAREA_823223':'',
               'RYLB_840581':'','RADIO_587182':'',
               'TEXT_230226':'','TEXT_76579':'',
               'TEXT_1961':'','TEXTAREA_355679':'',
               'TEXT_814184':'','TEXTAREA_529533':'',
               'TEXTAREA_592090':''}]
    
    def postForm(self):
        # 接口
        url='http://yqtb.sdnu.edu.cn/pdc/formDesignApi/dataFormSave'
        # 以后可能需要添加多个用户字段，执行多个任务
        for data in self.dataList:
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
                sendEmail('{} 填报失败 请及时处理'.format(data['XM_941836']))
                
    def sendEmail(message, self):
        msg = MIMEText(message, 'plain', 'utf-8')  # 发送内容
        msg['From'] = formataddr(['自动填报系统','******@163.com'])  # 发件人
        msg['To'] = formataddr(['','******@qq.com'])  # 收件人
        msg['Subject'] = "自动填报系统"  # 主题

        server = smtplib.SMTP("smtp.163.com", 25) # SMTP服务
        server.login("******@163.com", '******') # 邮箱用户名和密码  把密码改成授权码就行了
        server.sendmail('******@163.com', ['******@qq.com'], msg.as_string()) # 发送者和接收者
        server.quit()
            
        
    def run(self, posttime='08:00'):
        schedule.every().day.at(posttime).do(self.postForm)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__=="__main__":
    # 启动填报程序，posttime为填报时间，默认为早上八点~
    Poster().run(posttime="08:00")
