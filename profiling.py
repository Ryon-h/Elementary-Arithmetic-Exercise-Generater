import cProfile
import pstats
from arithmetic_generator import ArithmeticGenerator

def profile_exercise_generation(count: int, range_limit: int):
    """对习题生成过程进行性能分析"""
    generator = ArithmeticGenerator(range_limit)
    
    # 使用cProfile进行性能分析
    profiler = cProfile.Profile()
    profiler.enable()
    
    # 生成习题
    exercises = generator.generate_exercises(count)
    
    profiler.disable()
    
    # 创建性能统计对象
    stats = pstats.Stats(profiler)
    
    # 按累计时间排序并打印前10个最耗时的函数
    stats.sort_stats('cumulative').print_stats(10)
    
    return exercises

def main():
    # 测试不同规模的习题生成性能
    test_cases = [
        (100, 10),    # 小规模测试
        (1000, 20),   # 中等规模测试
        (10000, 50)   # 大规模测试
    ]
    
    for count, range_limit in test_cases:
        print(f"\n生成{count}道题目（数值范围：{range_limit}）的性能分析：")
        profile_exercise_generation(count, range_limit)

if __name__ == '__main__':
    main()