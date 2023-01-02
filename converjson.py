import mysql.connector
import json
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="258000",
  database="chttt"
)

# benh+trieuchung
class ConvertData:
# convert db
    def __init__(self):
        self.resultbenh=[]
        self.resulttrieutrung=[]
        self.resultfc=[]
        self.resultbc=[]
        self.resulttt=[]
    def convertbenh(self):
        """
        Lấy dữ liệu bệnh
        """
        dbbenh=mydb.cursor()
        dbbenh.execute("SELECT * FROM chttt.benh;")
        benh=dbbenh.fetchall()
        # print(benh)
        dirbenh={}
        # resultbenh=[]
        for i in benh:
            dirbenh['idbenh']=i[0]
            dirbenh['tenBenh']=i[1]
            dirbenh["nguyennhan"]=i[2]
            dirbenh['loikhuyen']=i[3]
            self.resultbenh.append(dirbenh)
            dirbenh={}
        # print(resultbenh)
        return self.resultbenh
    def converttrieuchung(self):  
        """
        Lấy dữ liệu triệu chứng
        """ 
        dbtrieuchung=mydb.cursor()
        dbtrieuchung.execute("SELECT * FROM chttt.trieuchung;")
        trieuchung=dbtrieuchung.fetchall()
        dirtrieuchung={}
        # resulttrieuchung=[]
        for i in trieuchung:
            dirtrieuchung['idtrieuchung']=i[0]
            dirtrieuchung['noidung']=i[1]
            self.resulttrieutrung.append(dirtrieuchung)
            dirtrieuchung={}
        # print(resulttrieuchung)
        return self.resulttrieutrung
    def getfc(self):
        """
        Lấy luật suy diễn tiến
        """
        dbfc=mydb.cursor()
        dbfc.execute("select idsuydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='1'")
        fc=dbfc.fetchall()
        # rule=[]
        s=[]
        d=[]
        for i in range(len(fc)):
            # rule=fc[i][1]
            s.append(fc[i][2])
            d.append(fc[i][3])
        # vt=rule[0]
        # return s,d
        tt=s[0]
        benh=[]
        dicfc={}
        # resultfc=[]
        for i in range(len(s)):
            if s[i]==tt:
                benh.append(d[i])
                # print(benh)
            else:
                dicfc['trieuchung']=tt
                dicfc['benh']=benh
                tt=s[i]
                self.resultfc.append(dicfc)
                benh=[]
                benh.append(d[i])
                dicfc={}
        dicfc['trieuchung']=tt
        dicfc['benh']=benh
        self.resultfc.append(dicfc)
        return self.resultfc
    def getbc(self):
        """
        Lấy luật suy diễn lùi
        
        """
        dbbc=mydb.cursor()
        dbbc.execute("select idsuydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='0' order by idbenh")
        fc=dbbc.fetchall()
        rule=[]
        s=[]
        d=[]
        for i in range(len(fc)):
            rule.append(fc[i][1])
            s.append(fc[i][2])
            d.append(fc[i][3])
        # print(rule)
        vtrule=rule[0]
        tt=[]
        benh=None
        # result=[]
        dicbc={}
        for i in range(len(rule)):
            if rule[i]==vtrule:
                tt.append(s[i])
                benh=d[i]
            else:
                dicbc['rule']=vtrule
                dicbc['benh']=benh
                dicbc['trieuchung']=tt
                vtrule=rule[i]
                self.resultbc.append(dicbc)
                
                benh=d[i]
                tt=[]
                tt.append(s[i])
                dicbc={}
        dicbc['rule']=vtrule
        dicbc['benh']=benh
        dicbc['trieuchung']=tt
        self.resultbc.append(dicbc)
        return self.resultbc
    def groupbc(self):
        """
        Nhóm các triệu chứng trong 1 luật
        """
        p=[]
        vt=self.resultbc[0]['benh']
        temp=[]
        for i in self.resultbc:
            t=[]
            t.append(i['benh'])
            # t=str(i['benh'])+" "
            for j in i['trieuchung']:
                t.append(j)
            # if i['benh']!=vt:
            #     vt=i['benh']
            #     temp+=t+"\n"
            # else: temp+=t
            temp.append(t)
        return temp
    def gettrieuchung(self):
        """
        Nhóm tất cả triệu chứng trong 1 bệnh
        """
        dbtrieuchung=mydb.cursor()
        dbtrieuchung.execute("SELECT * FROM chttt.suydien order by idbenh")
        dttt=dbtrieuchung.fetchall()
        benh=[]
        tt=[]
        rule=[]
        for i in dttt:
            benh.append(i[3])
            tt.append(i[2])
            rule.append(i[1])
        vtbenh=benh[0]
        lstt=[]
        dirtt={}
        
        for i in range(len(benh)):
            if benh[i]==vtbenh:
                lstt.append(tt[i])
            else:
                # print(type(dirtt))
                # dirtt['benh']=vtbenh
                dirtt[vtbenh]=sorted(set(lstt))
                # self.resulttt.append(dirtt) 
                # dirtt={}
                lstt=[]
                vtbenh=benh[i]
                lstt.append(tt[i])
        # dirtt['benh']=vtbenh
        dirtt[vtbenh]=sorted(set(lstt))
        # self.resulttt.append(dirtt)
        self.resulttt=dirtt
        return self.resulttt