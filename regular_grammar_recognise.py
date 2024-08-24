import re


class Recognise:
    def __init__(self, v, t, p, s, w):
        self.v = v  # str set
        self.t = t  # terminal str set
        self.p = p  # en_expr set
        self.s = s  # s
        self.w = w  # str
        self.len = len(self.w)
        self.v_list = []
        v0 = set()
        v0.add('')
        self.v_list.append(v0)

    '''
    THE CORE CODES ARE AS FOLLOWS
    '''

    def recognise(self) -> bool:
        for i in range(self.len):
            a = self.w[self.len - 1 - i]
            if a not in self.t:
                return False
            v_new = set()
            for item in self.p:
                ante = item.gen_ante(a, self.v_list[i])
                if ante is not None:
                    v_new.add(ante)
            print(f"a_{self.len - 1 - i}:{a}".ljust(20), f"V_{i}:{list(v_new)}")
            self.v_list.append(v_new)
        return self.s in self.v_list[self.len]


class Expr:
    def __init__(self, first: str, second: str):
        self.first = first
        self.second = second

    def can_gen(self, a: str, v: set):
        return self.first == a and self.second in v

    def __str__(self):
        return self.first + self.second


class GenExpr:
    def __init__(self, antecedent: str, consequence: Expr):
        self.antecedent = antecedent
        self.consequence = consequence

    def gen_ante(self, a: str, v: set):
        if self.consequence.can_gen(a, v):
            return self.antecedent
        return None

    def __str__(self):
        return self.antecedent + '->' + self.consequence.__str__()


def parse_gen_expr(str_item: str) -> GenExpr:
    str_list = str_item.split("->")
    if len(str_list) != 2:
        raise RuntimeError(f"Wrong Generation Format:{str_item}")
    antecedent = str_list[0]
    consequence = Expr(str_list[1][0], str_list[1][1]) if len(str_list[1]) > 1 \
        else Expr(str_list[1], '')
    return GenExpr(antecedent, consequence)


def pre_process(input_str: str):
    return re.sub('[ \t\n]', '', input_str).split(',')


def main():
    v = set(pre_process(
        input("1.The start symbol is 'S' all the time.\n  "
              "Please enter the non-terminal set, use ',' to separate items:")))
    v.add('S')
    t = set(pre_process(
        input("2.Please enter the terminal set; use ',' to separate items:")))
    p_str = pre_process(input("3.Please enter the generation set, use ',' to separate items\n"
                        "  (Use '->' to separate the antecedent and the consequence):"))
    p = set()
    for str_item in p_str:
        p.add(parse_gen_expr(str_item))
    print(f"Your V set:{list(v)}")
    print(f"Your T set:{list(t)}")
    print(f"Your P set:{[item.__str__() for item in p]}")
    s = 'S'
    w = input("4.Please enter the words to be recognized:")
    recognise = Recognise(v, t, p, s, w)
    print(recognise.recognise())


main()
