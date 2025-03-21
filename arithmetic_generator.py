import argparse
import random
import fractions
from typing import List, Set, Tuple, Union

class ArithmeticGenerator:
    def __init__(self, range_limit: int):
        self.range_limit = range_limit
        self.generated_expressions: Set[str] = set()
    
    def generate_number(self) -> Union[int, str]:
        """生成一个随机数（整数或真分数）"""
        # 随机决定生成整数还是分数
        if random.random() < 0.7:  # 70%概率生成整数
            return random.randint(0, self.range_limit - 1)
        else:
            # 生成真分数
            numerator = random.randint(1, self.range_limit - 1)
            denominator = random.randint(numerator + 1, self.range_limit)
            # 如果分子大于分母，转换为带分数格式
            if numerator >= denominator:
                whole = numerator // denominator
                numerator = numerator % denominator
                return f"{whole}'{numerator}/{denominator}" if numerator != 0 else str(whole)
            return f"{numerator}/{denominator}"
    
    def evaluate_expression(self, expr: str) -> Union[int, fractions.Fraction]:
        """计算表达式的值"""
        def parse_number(num_str: str) -> Union[int, fractions.Fraction]:
            if '/' in num_str:
                if "'" in num_str:
                    whole, frac = num_str.split("'")
                    num, den = map(int, frac.split("/"))
                    return fractions.Fraction(int(whole) * den + num, den)
                else:
                    num, den = map(int, num_str.split("/"))
                    return fractions.Fraction(num, den)
            return int(num_str)

        # 将表达式转换为后缀表达式
        def infix_to_postfix(expr: str) -> List[str]:
            precedence = {'+': 1, '-': 1, '×': 2, '÷': 2}
            stack = []
            output = []
            tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()

            for token in tokens:
                if token in '+-×÷':
                    while (stack and stack[-1] != '(' and 
                           precedence[stack[-1]] >= precedence[token]):
                        output.append(stack.pop())
                    stack.append(token)
                elif token == '(':
                    stack.append(token)
                elif token == ')':
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    if stack:
                        stack.pop()
                else:
                    output.append(token)

            while stack:
                output.append(stack.pop())

            return output

        # 计算后缀表达式
        def evaluate_postfix(tokens: List[str]) -> Union[int, fractions.Fraction]:
            stack = []
            for token in tokens:
                if token in '+-×÷':
                    b = stack.pop()
                    a = stack.pop()
                    if token == '+':
                        stack.append(a + b)
                    elif token == '-':
                        if b > a:  # 检查是否会产生负数
                            raise ValueError("产生负数")
                        stack.append(a - b)
                    elif token == '×':
                        stack.append(a * b)
                    elif token == '÷':
                        if b == 0:
                            raise ValueError("除数为零")
                        result = a / b
                        if result >= 1:
                            raise ValueError("除法结果不是真分数")
                        stack.append(result)
                else:
                    stack.append(parse_number(token))
            return stack[0]

        try:
            return evaluate_postfix(infix_to_postfix(expr))
        except Exception as e:
            raise ValueError(f"表达式计算错误: {str(e)}")

    def is_valid_expression(self, expr: str) -> bool:
        """检查表达式是否有效（不产生负数且除法结果为真分数）"""
        try:
            self.evaluate_expression(expr)
            return True
        except ValueError:
            return False

    def generate_expression(self) -> str:
        """生成一个随机算术表达式"""
        operators = ['+', '-', '×', '÷']
        max_operators = random.randint(1, 3)  # 随机决定使用1-3个运算符
        
        # 生成第一个数
        expr = str(self.generate_number())
        
        # 添加运算符和数字
        for _ in range(max_operators):
            op = random.choice(operators)
            num = str(self.generate_number())
            
            # 随机决定是否添加括号
            if random.random() < 0.3 and op in '×÷':  # 30%概率添加括号
                expr = f"({expr})"
            
            expr = f"{expr} {op} {num}"
            
            # 验证当前表达式是否有效
            if not self.is_valid_expression(expr):
                # 如果无效，回退到上一个有效状态
                return self.generate_expression()
        
        return f"{expr} ="
    
    def generate_exercises(self, count: int) -> List[dict]:
        """生成指定数量的习题"""
        exercises = []
        while len(exercises) < count:
            expr = self.generate_expression()
            if expr not in self.generated_expressions:
                try:
                    # 去掉表达式末尾的等号
                    question = expr
                    answer = str(self.evaluate_expression(expr.rstrip(' =')))
                    exercises.append({"question": question, "answer": answer})
                    self.generated_expressions.add(expr)
                except ValueError:
                    continue
        return exercises

def main():
    parser = argparse.ArgumentParser(description='四则运算题目生成器')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', type=int, help='生成题目的数量')
    group.add_argument('-e', type=str, help='练习题文件路径')
    parser.add_argument('-r', type=int, help='数值范围（必需）')
    parser.add_argument('-a', type=str, help='答案文件路径')
    
    args = parser.parse_args()
    
    if args.n:
        if not args.r:
            parser.error('使用-n参数时必须指定-r参数')
        if args.r < 2:
            parser.error('-r参数必须大于1')
            
        generator = ArithmeticGenerator(args.r)
        exercises = generator.generate_exercises(args.n)
        
        # 保存习题到文件
        with open('Exercises.txt', 'w', encoding='utf-8') as f:
            for i, exercise in enumerate(exercises, 1):
                f.write(f'{exercise}\n')
        
        # TODO: 计算答案并保存到文件
        
    elif args.e and args.a:
        # TODO: 实现答案验证功能
        pass

if __name__ == '__main__':
    main()