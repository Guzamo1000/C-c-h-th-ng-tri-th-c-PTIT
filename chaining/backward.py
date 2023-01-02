
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
    def __init__(self,rule,fact,goal):
        self.rule=self.read_rule(rule)
        # print(f"rule: {self.rule[0].right}")
        self.listD=self.searchgoal(goal)
        print(self.listD)
        self.fact=fact
        self.goal=goal
        print(f"goal {goal}")
    def read_rule(self,rule):
        new_rule=[]
        for i in rule:
            right=i[0]
            left=i[1:]
            new_rule.append(Rule(left,right))
        return new_rule
    def searchgoal(self,goal):
        """
        Lấy vị trí các role
        """
        rule_overcome=[]
        # print(len(self.rule))
        for i in range(len(self.rule)):
            if self.rule[i].right==goal:
                rule_overcome.append(i)
        return rule_overcome
    def do_backward(self):
        ttremove=[]
        for r in range(len(self.rule)):
            if self.rule[r].right==self.goal and (r in self.listD):
                for j in self.fact:
                    if j not in self.rule[r].left:
                        for point in self.rule[r].left:
                            ttremove.append(point)
                        self.listD.remove(r)
                        break
        return set(ttremove)