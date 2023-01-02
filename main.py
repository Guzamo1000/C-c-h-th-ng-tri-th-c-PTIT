from chaining.backward_chaining import BackwardChaining
from converjson import ConvertData
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
            if (rule[i][0]==goal) and (answer not in rule[i]): index.append(i)
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
def main():
    data=ConvertData()
    data.getbc()
    rule=data.groupbc()
    tt=data.converttrieuchung()
    all_rule=data.gettrieuchung()
    goal='D02'
    all_s_in_D=all_rule[goal]
    file_name = r"ex"
    fact_real=[]
    d=searchindexrule(rule,goal)
    while(len(all_s_in_D)>0):
        # print(f"all s in D {all_s_in_D} không :)")
        if all_s_in_D[0]=="": continue
        question=f"Bạn có bị triệu chứng {all_s_in_D[0]} không?"
        print(question)
        answer=int(input("Trả lời: "))
        print(f"answer {answer}")
        if answer==1:
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
                print(f"Bạn mắc bệnh {goal}")
                break
        if answer==0:
            # fact_real.append(all_s_in_D[0])
            # print(f'fact_read {fact_real}')
            b=BackwardChaining(rule,fact_real,goal,file_name)
            list_no_result,lsD=get_s_in_d(all_s_in_D[0],goal,rule,d,0) #S01 S02 S03 S04 S05
            d=sorted(set(d)-set(lsD))
            # print(f"list no result {list_no_result}, lsD: {lsD}")
            # print(f"D: {d}")
            # print(f"fact real {fact_real}")
            all_s_in_D=sorted(set(list_no_result)-set(fact_real))
            # print(f"all s in D after {all_s_in_D}")
            if b.result1==True:
                print(f"Bạn mắc bệnh {goal}")
                break
            # fact_real.remove(all_s[0])
            # all_s=sorted(list(b.ls_fact_use-set(fact_real)))
            # fact_real.remove(all_s[0])
        if len(d)==0: 
            print(f"Bạn không mắc bệnh {goal}")
            break
        
if __name__=="__main__":
    main()
