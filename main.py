import argparse
from arithmetic_generator import ArithmeticGenerator
# 导入答案检查模块
from answer_checker import AnswerChecker

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='四则运算题目生成程序')
    parser.add_argument('-n', type=int, default=10, help='要生成的题目数量')
    parser.add_argument('-r', type=int, default=10, help='数值范围')
    parser.add_argument('-e', type=str, help='题目文件')
    parser.add_argument('-a', type=str, help='答案文件')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # 如果提供了题目文件和答案文件，则进行答案校验
    if args.e and args.a:
        checker = AnswerChecker()
        checker.check_answers(args.e, args.a)
    # 否则生成新的题目
    else:
        generator = ArithmeticGenerator(args.r)
        exercises = generator.generate_exercises(args.n)
        
        # 将题目和答案写入文件
        with open('Exercises.txt', 'w', encoding='utf-8') as f:
            for i, exercise in enumerate(exercises, 1):
                f.write(f'{i}. {exercise["question"]}\n')
        
        with open('Answers.txt', 'w', encoding='utf-8') as f:
            for i, exercise in enumerate(exercises, 1):
                f.write(f'{i}. {exercise["answer"]}\n')
        
        print(f'已生成{args.n}道题目，数值范围为{args.r}')
        print('题目已保存到 Exercises.txt')
        print('答案已保存到 Answers.txt')

if __name__ == '__main__':
    main()