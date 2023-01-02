from chaining.backward_chaining import BackwardChaining
from converjson import ConvertData
from email.message import EmailMessage
import ssl,smtplib
def searchindexrule(rule,goal):
    """
    Tìm vị trí các rule có bệnh là goal
    """
    index=[]
    for r in range(len(rule)):
        if rule[r][0]==goal:
            index.append(r)
    return index
def get_s_in_d(answer,goal,rule,d,flag):
    """
    Lấy các triệu chứng theo sự suy diễn để giảm thiểu câu hỏi
    và 
    đánh dấu các luật đã được duyệt qua để bỏ qua những luật có cùng cùng câu hỏi vào
    """
    result=[]
    index=[]
    if flag==1:
        for i in range(len(rule)):
            # if (rule[i][0]==goal) and (answer not in rule[i]): index.append(i)
            if (rule[i][0]==goal) and (answer in rule[i]) and (i in d):
                # print(f"D in function {i}")
                # print(f"rule: {rule[i][0]}")
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)
                        # result=set()
    else:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]): index.append(i)
            if (rule[i][0]==goal) and (answer not in rule[i]) and (i in d):
                # index.append(i)
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)        

    return sorted(set(result)),index
def send_email(id_benh,person):
    """
    Gửi email cho người dùng
    """
    password=None
    
    with open("password.txt",'r') as f:
        password=f.read()
    email_sender = 'guzamo60@gmail.com'
    email_password = 'paltghsckxotraim'
    email_receiver = person

    db=ConvertData()
    db.getbc()
    db.convertbenh()
    db.converttrieuchung()
    benh=db.get_benh_by_id(id_benh)
    nguyen_nhan=benh['nguyennhan']
    loi_khuyen=benh['loikhuyen']
    subject='Medical records'
    body=f"""
        Nguyên nhân: {nguyen_nhan}
        Lời khuyên: {loi_khuyen}
    """
    em=EmailMessage()
    em['From']=email_sender
    em['To']=email_receiver
    em['Subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp: 
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())

    
def backward():
    # R1: S01,S02,S03,S04->D01
    # R2: S01,S02,S05->D01
    # R3: S01,S09,S13,S18->D01
    predictD=['D01','D02','D03']
    # predictS=['S']
    data=ConvertData()
    data.getbc()
    rule=data.groupbc()
    tt=data.converttrieuchung()
    all_rule=data.gettrieuchung()
    data.convertbenh()
    data.converttrieuchung()
    fact_real=['S01','S02','S04','S09']
    benh=0
    email='Guzamo59@gmail.com'
    for g in predictD:
        goal=g
        D=data.get_benh_by_id(goal) #Chứa thông tin của bảng bệnh có id == goal
        print(f"Chúng tôi đã có các triệu chứng ban đầu và có thể bạn mắc bệnh {D['tenBenh']}({goal}), sau đây chúng tôi muốn hỏi bạn một vài câu hỏi để tìm hiểu về bệnh bạn đang mắc phải")
        all_s_in_D=all_rule[goal]
        file_name = r"ex"
        all_s_in_D=sorted(set(all_s_in_D)-set(fact_real))
        d=searchindexrule(rule,goal)
        while(len(all_s_in_D)>0):
            # print(f"all s in D {all_s_in_D} không :)")
            # if all_s_in_D[0]=="": continue
            s=data.get_trieuchung_by_id(all_s_in_D[0])
            question=f"Bạn có bị triệu chứng {s['noidung']}({all_s_in_D[0]}) không?"
            print(question)
            answer=None
            while(True):
                answer=(input("Trả lời (1:có, 0:không, x: kết thúc hội thoại): "))
                if answer!=1 and answer!=0:
                    print("Vui lòng nhập lại để chúng tôi tiếp tục tư vấn cho bạn (1: có, 0:không, x: kết thúc hội thoại) ")
                if answer.lower()=='x':
                    print("Hẹn gặp lại :))")
                    return
                else: break
            
            print(f"answer: {answer}")
            if answer=="1":
                fact_real.append(all_s_in_D[0])
                # print(f'fact_read {fact_real}')
                b=BackwardChaining(rule,fact_real,goal,file_name)
                list_no_result,lsD=get_s_in_d(all_s_in_D[0],goal,rule,d,1)
                d=sorted(set(d)-set(lsD))
                # print(f"list no result {list_no_result}, lsD: {lsD}")
                # print(f"D: {d}")
                # print(f"fact real {fact_real}")
                all_s_in_D=sorted(set(list_no_result)-set(fact_real))
                # print(f"all s in D after {all_s_in_D}")
                if b.result1==True:
                    # print(f"Bạn mắc bệnh {goal}")
                    benh=1
                    break
            if answer=="0":
                # fact_real.append(all_s_in_D[0])
                # print(f'fact_read {fact_real}')
                # b=BackwardChaining(rule,fact_real,goal,file_name)
                list_no_result,lsD=get_s_in_d(all_s_in_D[0],goal,rule,d,0) #S01 S02 S03 S04 S05
                d=sorted(set(d)-set(lsD))
                # print(f"list no result {list_no_result}, lsD: {lsD}")
                # print(f"D: {d}")
                # print(f"fact real {fact_real}")
                all_s_in_D=sorted(set(list_no_result)-set(fact_real))
                # print(f"all s in D after {all_s_in_D}")
                # if b.result1==True:
                #     # print(f"Bạn mắc bệnh {goal}")
                #     benh=1
                #     break
                # fact_real.remove(all_s[0])
                # all_s=sorted(list(b.ls_fact_use-set(fact_real)))
                # fact_real.remove(all_s[0])
            if len(d)==0: 
                print(f"Có vẻ như bạn không mắc bệnh {goal}")
                break
        if benh==1:
            print(f"Bạn mắc bệnh {goal} và chúng tôi sẽ gửi thêm thông tin về bệnh này cho bạn qua mail")
            send_email(goal,email)
            print(f"Lời khuyên")
            D['loikhuyen']=D['loikhuyen'].replace("/n","\n")
            print(f"{D['loikhuyen']}")
            print("")
            break
    if benh==0:
        print(f"Bạn không bị bệnh nào đou :))")
def main():
    result=backward()
if __name__=="__main__":
    main()
