class Poster():
    
    # post数据，wid可能是微信ID，其余数据为表单数据
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
            # 这里可以针对填报失败做出通知处理，如发邮件等。
            if('true' in res):
                print(data['XM_941836'], "填报成功")
            else:
                print('warning:', data['XM_941836'], "填报失败")
            
        
    def run(self, posttime='08:00'):
        schedule.every().day.at(posttime).do(self.postForm)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__=="__main__":
    Poster().run(posttime="08:00")
