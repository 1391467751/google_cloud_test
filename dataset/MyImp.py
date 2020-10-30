import MyCloud
from  MyLog import mylog
from Co


class MyImp:
    def __init__(self):
        self.mcd =  MyCloud.MyCloudData()
        self.mcd.init()
        self.table_type = {"stock_price" :{"Date":"DATE NOT NULL UNIQUE" , "Price":"Float" }}
    

    def get_single_stock_info_date(self,code,start_date,end_date=None):
        if(type(code)!= str):
            mylog.log("detail info only support one stock a time",'Warning')
            return None
        if(end_date==!None):
            end_date=datetime.datetime.today().strftime("%Y-%M-%d")
        pass

    def has_table(self,table):
        if(self.mcd.has_table(table)<0):
            mylog.log("Don't have table for {} ,need create it".format(table),"Error")
            return false

    def create_table_type(self,table,type_id):
        if(type_id in self.table_type.keys()):
            info = self.table_type[type_id]
            table_info=",".join(["{} {}".format(i,info[i]) for i in info])
            self.mcd.create_table(table,table_info)
            return True
        else:
            mylog.log("Only create register table for {}".format(table),"Error")
            return False

    def insert_data_into_table(self,table,data):
        '''
            make sure table exists
        '''
        if(not isinstance(data,pd.DataFrame)):
            mylog.log("insert_data_into_table need pandas DataFrame struct","Error")
            return None
        data_item = data.agg(lambda x:"({})".format(" ".join([str(i) for i in x])))
        command = "insert into {} values ({})".format(table,data_item.values)
        self.mcd.exec(command)
        return data_item.size
    

    def get_table_last_date(self,table):
        if(self.has_table(table)):
            date = self.get_table_info(table,info={"Date" :"DATE"},limits="order by Date DESC limit 1")
            if(data!=None  and data.size>0):
                return data.values
            else:
                return '1995-01-01'
        else:
            return None

    def get_stock_price_date(self,codes,start_date=None,end_date=None):
        if(end_date==None):
            end_date = datetime.datetime.today().format("%Y-%M-%d")
        if(start_date == None):
            start_date = "2000-01-01"
        data = None
        if(isinstance(codes,str)):
            code = codes
            table = "{}_code".format(code)
            if(not self.has_table(table)):
                self.create_table_type(table,"stock_price")
                data = self.get_remote_stock_price(code,None,end_date)
                self.insert_data_into_table(table,data)
            last_date = self.get_table_last_date(table)
            if(last_date==None):
                mylog.log("Inpossible to get here",'Error')
                return None
            last_date = datetime.datetime.strptime(last_date,"%Y-%M-%d")
            if(last_date<datetime.datetime.today()):
                # need update table
                data = self.get_remote_stock_price(code,(last_date+datetime.timedelta(1)).strftime("%Y-%M-%d"),end_date)
                self.insert_data_into_table(table,data)
            command  =  "select * from {} where date between '{}' and '{}'" .format(table,start_date,end_date)
            data = self.mcd.exec(command)
        else:
            mylog.log("Only support get one stock a time","Warning")
        return data

    
    def get_stock_price_count(self,code,count,end_date=None):
        if(end_date==!None):
            end_date=datetime.datetime.today().strftime("%Y-%M-%d")
        start_date =  datetime.datetime.today()-datetime.timedelta(count)
        start_date =  start_date.strftime("%Y-%M-%d")
        return get_stock_price_date(code,start_date,end_date)
        
        

    def get_remote_stock_price(self, code,start_date=None,end_date=None):
        if(end_date==None):
            end_date = datetime.datetime.today().format("%Y-%M-%d")
        if(start_date == None):
            start_date = "2000-01-01"
        pass

    
    def get_table_info(self,table,info=None,limits=None):
        """
            return pd.DataFrame struct
            empty means no suit data
            None means no table
        """
        if(not self.has_table(table)):
            return None
        else:
            mylog.log("table {} exists,get info".format(table),"Log")
            if(info==None):
                return pd.DataFrame(())
            info_need = ",".join(info.keys())
            command = " ".join(["select",info_need,"from",table])
            if(limits !=None):
                command += limits
            data = self.mcd.exec(command)
            data =  pd.DataFrame(data,columns=info.keys())
            return data
    
            
            
            
