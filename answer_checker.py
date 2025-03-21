class AnswerChecker:
    def check_answers(self, exercise_file, answer_file):
        """检查答案文件中的答案是否正确，并将结果输出到Grade.txt文件中

        Args:
            exercise_file (str): 题目文件路径
            answer_file (str): 答案文件路径
        """
        # 读取题目文件
        with open(exercise_file, 'r', encoding='utf-8') as f:
            exercises = f.readlines()
        
        # 读取答案文件
        with open(answer_file, 'r', encoding='utf-8') as f:
            answers = f.readlines()
        
        # 检查答案数量是否匹配
        if len(exercises) != len(answers):
            print('错误：题目数量与答案数量不匹配')
            return
        
        correct_indices = []
        wrong_indices = []
        total_count = len(exercises)
        
        # 逐题检查答案
        for i, (exercise, answer) in enumerate(zip(exercises, answers)):
            # 获取题号
            question_num = i + 1
            
            # 去除题号和空白字符
            exercise = exercise.split('.', 1)[1].strip()
            answer = answer.split('.', 1)[1].strip()
            
            # 计算正确答案
            try:
                correct_answer = str(eval(exercise))
                if correct_answer == answer:
                    correct_indices.append(question_num)
                else:
                    wrong_indices.append(question_num)
            except:
                print(f'警告：第{question_num}题无法计算')
                wrong_indices.append(question_num)
        
        # 将结果写入Grade.txt文件
        with open('Grade.txt', 'w', encoding='utf-8') as f:
            f.write(f'Correct: {len(correct_indices)} {str(tuple(correct_indices)).replace(" ", "")}\n')
            f.write(f'Wrong: {len(wrong_indices)} {str(tuple(wrong_indices)).replace(" ", "")}')
        
        # 输出统计结果
        print(f'结果已写入Grade.txt文件')