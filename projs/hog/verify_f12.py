import time
import hog

t = time.time()
print("final_strategy(53,60)=", hog.final_strategy(53, 60))
print("final_strategy(10,10)=", hog.final_strategy(10, 10))
print("final_strategy(0,0)=", hog.final_strategy(0, 0))
print("建表耗时 %.2fs" % (time.time() - t))

# 复刻 tests/12.py 的 setup：确保不调用 max_scoring_num_rolls，且全部返回 0~10 整数
def check_strategy(strat):
    for score in range(100):
        for opp in range(100):
            num_rolls = strat(score, opp)
            if not isinstance(num_rolls, int):
                raise ValueError("final_strategy(%d, %d) 返回 %r 不是整数" % (score, opp, num_rolls))
            if not (0 <= num_rolls <= 10):
                raise ValueError("final_strategy(%d, %d) 返回 %r 越界" % (score, opp, num_rolls))

def max_scoring_num_rolls(dice=lambda: 1):
    raise RuntimeError("final_strategy 不应该调用 max_scoring_num_rolls")

old = hog.max_scoring_num_rolls
hog.max_scoring_num_rolls = max_scoring_num_rolls
try:
    check_strategy(hog.final_strategy)
    print("check_strategy 通过：全部组合返回 0~10 整数，且未触发 max_scoring_num_rolls 异常")
finally:
    hog.max_scoring_num_rolls = old
