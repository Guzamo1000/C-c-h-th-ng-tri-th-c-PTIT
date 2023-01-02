from converjson import ConvertData
class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.flag1 = False
        self.flag2 = False
        # self.r=r

    def follows(self, facts):# facts là các triệu chứng đã có
        for fact in self.left: # cho từng luật ở vế trái
            if fact not in facts: # nếu như luật đó ko tồn tại trong facts ban đầu
                return fact # thì trả về cái luật đó
        return None

    def __str__(self):
        return "%s->%s" % (",".join(self.left), self.right)

class BackwardChaining:
    def __init__(self,rule,fact,goal,file_name):
        self.output = ""
        self.output_file_name = None
        self.iteration = 0
        self.current_goals = [] # các goal mới được hình thành trong quá trình suy diễn
        self.found_facts = []
        self.road = []
        # self.trieuchung=ConvertData()
        # self.total_tt=self.trieuchung.gettrieuchung()
        self.output += "PART 1. Data\n"
        # lấy luật , lấy fact thực tế , lấy Goal từ filename
        # self.rules, self.target_facts, self.goal = self.read_data(file_name)
        self.rules=self.read_rule(rule)
        self.target_facts=self.read_facts(fact)
        self.goal=goal
        # rule là 1 list các Rule(left, right) , facts là 1 dòng , goal là 1 ký tự
        self.print_data(self.rules, self.target_facts, self.goal)# in part1

        self.output += "PART 2. Execution\n"
        result = self.do_backward_chaining(self.goal) # => true / false
        self.result1=result
        # self.result1=result
        self.output += "\n" + "PART 3. Results\n"
        self.print_result(result)
        # print(result)

        self.write_output(file_name)

    # def do_backward_chaining(self, goal, indent=""):# trả về giá trị true false caajp0 nhật cho result
    #     # if goal in 
    #     if goal in self.target_facts:# đích mà có trong facts rồi thì chắc chắc yes
    #         self.print_step(goal, indent,
    #                         "Fact (được chứng minh), bởi vì đã có trong các facts %s. Trả về thành công." % ", ".join(self.target_facts))
    #         return True

    #     if goal in self.current_goals:# vòng lặp vô hạn
    #         self.print_step(goal, indent, "Vòng lặp vô hạn. Trả về thất bại")
    #         return False

    #     if goal in self.found_facts:# đích nằm trong các fact được tìm thấy
    #         self.print_step(goal, indent, "Fact (was given), because facts %s and %s. Returning, success." % (
    #             ", ".join(self.target_facts), ", ".join(self.found_facts)))
    #         return True

    #     results_count = len(self.road)# độ dài của đường đi

    #     for rule in self.rules:# lấy từng Rule(left, right)
    #         if rule.right == goal:# nếu right mà là goal
    #             is_satisfied = False
    #             #in ra rule và in ra vế left
    #             self.print_step(goal, indent, "Tìm thấy luật %s. Các goals mới cần chứng mình là %s." % (
    #                 "R" + str(self.rules.index(rule) + 1) + ":" + str(rule), ", ".join(rule.left)))

    #             #lúc này từng phần trong về left lại là một cái goal mới
    #             for new_goal in rule.left:
    #                 self.current_goals.append(goal)# thêm vào goal mới
    #                 print(rule.left)
    #                 print(self.iteration,"trc",self.current_goals)
                    
    #                 is_satisfied = self.do_backward_chaining(new_goal, indent + "-") # tiếp tục thực hiện quá trình suy diễn goal mới
    #                 if is_satisfied == False: return False
                    
    #                 self.current_goals.pop() # xóa goal vừa làm đi
    #                 print(self.iteration,self.current_goals)
    #                 if self.goal in self.found_facts :# NẾU ĐÍCH CUỐI CÙNG NẰM TRONG FACT suy diễn ra
    #                     # self.output += ("statisfied")
    #                     return True

    #             if is_satisfied: # hoàn thành thì cập nhật road
                    
    #                 self.road.append("R" + str(self.rules.index(rule) + 1))
    #                 self.found_facts.append(rule.right)# fail ...........
    #                 # => nguyên tắc là phải để cái dễ trước và khó sau
    #                 # print(self.found_facts)
    #                 self.print_step(goal, indent, "Fact (bây giờ được cập nhật). Facts %s and %s. Trả về thành công." % (
    #                     ", ".join(self.target_facts), ", ".join(self.found_facts)))
    #                 return True

    #         while len(self.road) > results_count:
    #             self.road.pop()
            

    #     # khi mà nguyên thủy mà ko có trong facts thì k.luan bị lỗi tại nhánh suy diễn đó
    #     self.print_step(goal, indent, "Không có luật nào để suy diễn/ không có fact này ban đầu. Trả về thất bại.")
    #     return False# CHỈ CẦN 1 GOAL FALSE THÌ NGAY LẬP TỨC FALSE
    # # def do_backward_chaining(self, goal, indent=""):
    # #     for rule in self.rules:
    # #         if rule.right==goal:
    def do_backward_chaining(self, goal, indent=""):# trả về giá trị true false caajp0 nhật cho result
        ls=0
        ls_fact_use=[]
        # print(self.target_facts)
        end=False
        for rule in self.rules:
            # ls=0
            dk=1
            
            if rule.right==goal:
                self.print_step(goal, indent, "Tìm thấy luật %s. Các goals mới cần chứng mình là %s." % ("R" + str(self.rules.index(rule) + 1) + ":" + str(rule), ", ".join(rule.left)))
                # print(f"rule {rule.left}")
                for f in range(len(rule.left)):
                    fact_guess=str(rule.left[f])
                    # print(f"type fact {type(fact_guess)} {fact_guess}")
                    # if f<len(self.target_facts):
                    if fact_guess not in self.target_facts:
                        # print(f"-{fact_guess} not in {self.target_facts}")
                        self.print_step(fact_guess, indent + '-', "Không có luật nào để suy diễn/ không có fact này ban đầu. Trả về thất bại.")
                        dk=0
                        break
                    else:
                        self.print_step(fact_guess, indent +"-", "Fact (bây giờ được cập nhật). Facts %s and %s. Trả về thành công." % (
                                        ", ".join(self.target_facts), ", ".join(self.found_facts)))
                        # print(f"-Co {fact_guess}")
                        
                        # dk=1
                self.road.append("R" + str(self.rules.index(rule) + 1))
                self.found_facts.append(rule.right)

                # print(f"-dk {dk}")
                
                if dk==1: #Kiểm tra nếu đúng hết các triệu chứng thì dừng vòng lặp
                    ls=1 #Kiểm tra xem có fact nào có trong tập luật ban đầu không
                    break 
                # print(f"-ls fact use {sorted(set(ls_fact_use))}")
        # print(f"ls fact use {sorted(set(ls_fact_use))}")
        if ls==0: #Nếu không có luật nào trả lời đùng theo fact thì dừng
            self.print_step(goal, indent, "Không có luật nào để suy diễn/ không có fact này ban đầu. Trả về thất bại.")
            return False
        # if end==True:
        #     return True
        else:
            return True
    # def get_s_in_fact(self):

    def print_step(self, goal, indent, msg):#indent : dấu gạch ngang
        self.iteration += 1
        self.output += str(self.iteration).rjust(3, " ") + ") %sGoal %s. " % (indent, goal) + msg + "\n"

    def read_data(self, file_name):
        rules = []
        facts = []
        goal = None

        file = open(file_name, "r")
        read_state = 0

        for line in file:# lấy từng dòng
            line = line.replace("\n", "")
            if line == "":# kiểm tra dòng rỗng => phần sau chính là fact hoặc goal 
                read_state += 1
                continue
            line = line.split(" ") # ko rỗng thì chặt ra list

            if line[0] == '#': # dấu thăng thì bỏ qua
                continue

            if read_state == 0:
                right = line[0]# vế trái cùng là đích
                left = line[1:]# vế phải là các luật suy diễn
                # vd L A B thì ta hiểu là A+B => L
                rules.append(Rule(left, right)) # thêm luật đó vào mảng rules

            if read_state == 1:
                facts = line # đây là các triệu chứng thực tế đã gặp

            if read_state == 2:
                goal = line[0]

        return rules, facts, goal# rule là 1 list các Rule(left, right), facts là 1 dòng , goal là 1 ký tự
    def read_rule(self,rule):
        new_rule=[]
        id=0
        for i in rule:
            right=i[0]
            left=i[1:]
            # id+=1

            new_rule.append(Rule(left,right))
        # print(new_rule)
        return new_rule
    def read_facts(self,line):
        ad=[]
        for i in line:
            ad.append(i)
        return ad
    def print_data(self, rules, facts, goal):
        self.output += "  1) Productions\n"
        for rule in rules:
            self.output += "    R%i: %s\n" % (rules.index(rule) + 1, str(rule))
        self.output += "\n  2) Facts\n    %s.\n\n" % ", ".join(facts)
        self.output += "  3) Goal\n    %s.\n\n" % goal

    def print_result(self, result): # part 3
        if result is not False:

            if len(self.road) == 0:
                self.output += "  1) Goal %s among facts.\n" % self.goal
                self.output += "  2) Empty road.\n"
            else:
                self.output += "  1) Goal %s derived.\n" % self.goal
                self.output += "  2) Road: %s.\n" % ", ".join(self.road)
        else:
            self.output += "  1) Goal %s unreachable.\n" % self.goal

    def write_output(self, file_name):
        self.output_file_name = "BC_OUTPUT_%s.txt" % file_name.replace("/", ".")
        file = open(self.output_file_name, "w", encoding='utf8')
        file.write(self.output)