from answer_checker import AnswerChecker

# 创建示例题目文件
with open('Exercises.txt', 'w', encoding='utf-8') as f:
    f.write('1. 1 + 2\n')
    f.write('2. 3 * 4\n')
    f.write('3. 10 - 5\n')

# 创建示例答案文件
with open('Answers.txt', 'w', encoding='utf-8') as f:
    f.write('1. 3\n')
    f.write('2. 12\n')
    f.write('3. 5\n')

# 实例化AnswerChecker
checker = AnswerChecker()

# 调用check_answers方法检查答案
checker.check_answers('Exercises.txt', 'Answers.txt')