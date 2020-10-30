import datetime


class MyLog():
    def __init__(self):
        self.type=['Log','Warning','Error']

    def log(self,info,type_id='Error'):
        if(type_id not in self.type):
            return
        if(type(info)!=str):
            return 
        if(type_id == 'Log'):
            self.log("Log: {} {}".format(datetime.datetime.now().strftime("%Y-%M-%d %H:%m:%S"),info))
        elif(type_id=='Warning'):
            self.warning("Warning: {} {}".format(datetime.datetime.now().strftime("%Y-%M-%d %H:%m:%S"),info))
        elif(type_id=='Error'):
            self.error("Error: {}{}".format(datetime.datetime.now().strftime("%Y-%M-%d %H:%m:%S"),info))

    def log(self,info):
        print(info)

    def warning(self,info):
        print(info)

    def error(self,info):
        print(info)


mylog =  Mylog()
