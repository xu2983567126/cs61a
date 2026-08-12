"""猪猪游戏（The Game of Hog）。"""

from functools import lru_cache

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100  # 猪猪游戏的目标分数：先达到 100 分者获胜。
GOAL_SCORE = GOAL  # 别名：兼容 tests/check_strategy.py 中 from hog import GOAL_SCORE 的导入

# ============================== 调用示例 ==============================
# 以下为各主要函数的调用示例（仅作说明，导入本模块时不会自动执行）：
#
# roll_dice(3)                      # 投 3 个六面骰，返回点数之和；若含 1 则返回 1
# boar_brawl(0, 10)                 # 不投骰时的野猪冲撞得分：(1 - 0) * 3 = 3
# take_turn(3, 16, 28)              # 玩家 16 分、对手 28 分，投 3 个骰子
# simple_update(5, 0, 0)            # 忽略 Sus Fuss 的得分更新
# sus_update(5, 0, 0)               # 包含 Sus Fuss 的得分更新
# play(always_roll_5, always_roll_5, simple_update)                # 完整一局（默认目标 100）
# play(always_roll_5, always_roll_5, sus_update, goal=50)          # 目标 50 分
#
# 自定义策略示例：
# def my_strategy(score, opponent_score):
#     return 6 if score < opponent_score else 5
# play(my_strategy, my_strategy, sus_update, score0=15, score1=10, goal=32)
#
# 使用确定性骰子（便于调试，按给定序列循环返回）：
# from dice import make_test_dice
# test_dice = make_test_dice(3, 4, 1)
# roll_dice(3, test_dice)           # 返回 1（第三个结果是 1，整轮作废）
# =====================================================================

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """模拟恰好投掷 NUM_ROLLS（>0）次骰子，返回点数之和。若任意一次投出 1，则整轮作废，返回 1（Pig Out 规则）。

    num_rolls:      投掷骰子的次数。
    dice:           模拟单次投骰结果的函数，默认使用六面骰。
    """
    # 以下断言确保 num_rolls 为正整数。
    assert type(num_rolls) == int, "num_rolls 必须是整数。"
    assert num_rolls > 0, "至少要投掷一次。"
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    ret = 0
    is_one = False
    for _ in range(num_rolls):
        num = dice()
        if num == 1:
            is_one = True
        ret += num
    if is_one:
        ret = 1
    return ret
    # END PROBLEM 1


def boar_brawl(player_score, opponent_score):
    """当当前玩家投掷 0 个骰子时，根据「野猪冲撞（Boar Brawl）」规则返回得分：
    对手分数的十位数与当前玩家分数的个位数之差的绝对值 × 3，再与 1 取最大值。

    player_score:     当前玩家的总分。
    opponent_score:   对手的总分。
    """
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    ret = (opponent_score // 10) % 10 - player_score % 10
    ret *= 3
    if ret < 0:
        ret *= -1
    if ret < 1:
        ret = 1
    return ret

    # END PROBLEM 2


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """返回当前玩家本回合的得分：投掷 NUM_ROLLS 个骰子（若次数不为 0），
    或在不投骰时按 Boar Brawl 规则计算得分。

    num_rolls:       本回合投掷的骰子数。
    player_score:    当前玩家的总分。
    opponent_score:  对手的总分。
    dice:            模拟单次投骰结果的函数。
    """
    # 保留这些断言，有助于排查错误。
    assert type(num_rolls) == int, "num_rolls 必须是整数。"
    assert num_rolls >= 0, "take_turn 中不能投掷负数个骰子。"
    assert num_rolls <= 10, "最多只能投掷 10 个骰子。"
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if num_rolls == 0:
        return boar_brawl(player_score, opponent_score)
    return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """返回玩家本回合开始时有 PLAYER_SCORE 分、随后投掷 NUM_ROLLS 个骰子后的总分（忽略 Sus Fuss 规则）。

    即：在自身当前得分基础上加上本回合得分。
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score


def is_prime(n):
    """判断 N 是否为质数。"""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True


def num_factors(n):
    """返回 N 的因数个数（包含 1 和 N 本身）。"""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    ret = 0
    for i in range(n):
        if n % (i + 1) == 0:
            ret += 1
    return ret
    # END PROBLEM 4


def sus_points(score):
    """考虑 Sus Fuss 规则后，返回玩家当前分数的新值。

    若得分的因数个数为 3 或 4，则将其提升到最近的质数。
    """
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    if num_factors(score) == 3 or num_factors(score) == 4:
        while not is_prime(score):
            score += 1
    return score
    # END PROBLEM 4


def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """返回玩家本回合开始时有 PLAYER_SCORE 分、随后投掷 NUM_ROLLS 个骰子后的总分（包含 Sus Fuss 规则）。"""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return sus_points(simple_update(num_rolls, player_score, opponent_score, dice))
    # END PROBLEM 4


def always_roll_5(score, opponent_score):
    """一种固定策略：无论当前分数和对手分数如何，总是投掷 5 个骰子。"""
    return 5


def play(strategy0, strategy1, update, score0=0, score1=0, dice=six_sided, goal=GOAL):
    """模拟一局游戏，返回两名玩家的最终得分，玩家 0 的分数在前，玩家 1 的分数在后。

    例如，play(always_roll_5, always_roll_5, sus_update) 模拟一局游戏，
    其中两名玩家每回合都固定投掷 5 个骰子，并且启用 Sus Fuss 规则。

    策略函数（如 always_roll_5）接收当前玩家的分数与对手的分数，
    返回当前玩家本回合选择投掷的骰子数。

    更新函数（如 sus_update 或 simple_update）接收投掷的骰子数、当前玩家的分数、
    对手的分数以及用于模拟投骰的 dice 函数，返回该玩家行动后的更新得分。

    strategy0:  玩家 0 的策略。
    strategy1:  玩家 1 的策略。
    update:     更新函数（两名玩家共用）。
    score0:     玩家 0 的起始分数。
    score1:     玩家 1 的起始分数。
    dice:       无参函数，用于模拟一次投骰。
    goal:       当某位玩家达到该分数时，游戏结束并分出胜负。
    """
    who = 0  # 即将行动的玩家：0（先手）或 1（后手）
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    while score0 < goal and score1 < goal:
        strategy, score, opponent_score = strategy0, score0, score1
        if who == 1:
            strategy = strategy1
            score, opponent_score = opponent_score, score
        score = update(strategy(score, opponent_score), score, opponent_score, dice)
        if who == 0:
            score0 = score
        else:
            score1 = score
        who = 1 - who
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """返回一个玩家策略：无论得分情况如何，始终投掷 N 个骰子。

    玩家策略是一个函数，接收两个总分（当前玩家分数、对手分数）作为参数，
    返回当前玩家本回合要投掷的骰子数。

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10

    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    def strategy(x, y):
        return n
    return strategy
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """一种玩家策略：除非对手分数更高，否则总是投掷 5 个骰子；若落后则多投 1 个以追赶。

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # 多投一个以追赶
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """判断 STRATEGY 是否对每一组（当前分数, 对手分数）组合都返回相同的骰子数
    （假设游戏进行到 GOAL 分）。

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    always = strategy(0, 0)
    for i in range(0, goal):
        for j in range(0, goal):
            if strategy(i, j) != always:
                return False
    return True
    # END PROBLEM 7


def make_averaged(original_function, times_called=1000):
    """返回一个函数，该函数返回 ORIGINAL_FUNCTION 被调用 TIMES_CALLED 次的平均结果。

    original_function: 要重复调用的函数（如 roll_dice），接收投掷次数与骰子作为参数。
    return:            一个平均后的新函数。

    实现时需使用 *args 语法。

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # 10 个 4、10 个 2、10 个 5、10 个 1 的平均值
    3.0
    """

    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def averaged_roll_dice(*args):
        ret = 0;
        for i in range(times_called):
            ret += original_function(*args)
        ret /= times_called
        return ret
    return averaged_roll_dice
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, times_called=1000):
    """返回能使单回合平均得分最高的骰子数（1 到 10）。
    假设骰子总是返回正数点数。

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    max_scoring_num = -1
    max_score = 0
    for i in range(1, 11):
        averaged_dice = make_averaged(roll_dice, times_called)
        score = averaged_dice(i, dice)
        if score > max_score:
            max_scoring_num = i
            max_score = score
    return max_scoring_num
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """若 strategy0 战胜 strategy1 则返回 0，否则返回 1。"""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """返回 STRATEGY 对阵 BASELINE 的平均胜率。
    平均时分别以玩家 0 和玩家 1 的身份开局。"""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """运行一系列策略实验并报告结果。"""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print("Max scoring num rolls for six-sided dice:", six_sided_max)

    print("always_roll(6) win rate:", average_win_rate(always_roll(6)))  # 约 0.5
    print("catch_up win rate:", average_win_rate(catch_up))
    print("always_roll(3) win rate:", average_win_rate(always_roll(3)))
    print("always_roll(8) win rate:", average_win_rate(always_roll(8)))

    print("boar_strategy win rate:", average_win_rate(boar_strategy))
    print("sus_strategy win rate:", average_win_rate(sus_strategy))
    print("final_strategy win rate:", average_win_rate(final_strategy))
    "*** 你可以在此处自行添加更多实验 ***"



def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """若 Boar Brawl 能提供至少 THRESHOLD 分，则返回 0 个骰子；否则返回 NUM_ROLLS。
    忽略 Sus Fuss 规则。"""
    # BEGIN PROBLEM 10
    if boar_brawl(score, opponent_score) >= threshold:
        return 0
    return num_rolls  # 实现后请删除此行。
    # END PROBLEM 10


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """若投掷 0 个骰子能让分数至少提升 THRESHOLD 分，则返回 0 个骰子；否则返回 NUM_ROLLS。
    需同时考虑 Boar Brawl 与 Sus Fuss 规则。"""
    # BEGIN PROBLEM 11
    if sus_update(0, score, opponent_score, dice=six_sided) - score >= threshold:
        return 0
    return num_rolls  # 实现后请删除此行。
    # END PROBLEM 11


# ==================== 1. 概率生成器（顶层） ====================
def throw(max_num=10, dice_maxval=6):
    # Mem[cnt][tot_point]: 掷cnt个骰子，得到tot_point点的概率
    Mem = [[0.0] * (max_num * dice_maxval + 1) for _ in range(max_num + 1)]
    for i in range(1, 7):
        Mem[1][i] = 1.0 / 6.0
    for i in range(2, max_num + 1):
        for pre in range((i - 1) * 2, (i - 1) * dice_maxval + 1):
            for dice in range(2, dice_maxval + 1):
                Mem[i][pre + dice] += Mem[i - 1][pre] / dice_maxval
        Mem[i][1] = Mem[i - 1][1] + (1 - Mem[i - 1][1]) / 6.0
        assert abs(sum(Mem[i]) - 1) <= 1e-9, "概率总和不等于100%"
    print("Mem build finished!")
    def f(cnt, tot_point):
        assert tot_point == 1 or (cnt * 2 <= tot_point <= cnt * dice_maxval), "无法掷出该点数"
        return Mem[cnt][tot_point]
    return f


# ==================== 2. 全局 DP 表（顶层，与 roll_and_sus 平级） ====================
win_p = [[0] * 100 for _ in range(100)]      # 每个比分下，当前行动方的获胜概率
choose = [[-1] * 100 for _ in range(100)]    # 达到最大胜率时，应该掷的骰子数


# ==================== 3. 占位函数（对应你的图片，函数体为空） ====================
def roll_and_sus(score):
    # 仅需要你自己的分数...
    pass   # 这个函数实际上没用到，只为了保留你图片中的样子


# ==================== 4. 核心建表函数（顶层，与 roll_and_sus 平级） ====================
def Preparation(max_num=10, dice_maxval=6):
    f = throw()
    
    def Prob(score, opposcore, num_rolls):
        if num_rolls == 0:
            new_score = sus_update(0, score, opposcore)
            return 1 - Win_prob(opposcore, new_score)
        ans = f(num_rolls, 1) * (1 - Win_prob(opposcore, sus_points(score + 1)))
        for i in range(num_rolls * 2, dice_maxval * num_rolls + 1):
            ans += f(num_rolls, i) * (1 - Win_prob(opposcore, sus_points(score + i)))
        return ans

    def Win_prob(score, opposcore):
        if score >= 100:
            return 1.0
        if opposcore >= 100:
            return 0.0
        # 查全局缓存表
        if choose[score][opposcore] != -1:
            return win_p[score][opposcore]
        max_winp = 0.0
        best_rolls = 0
        for i in range(11):
            t = Prob(score, opposcore, i)
            if t > max_winp:
                max_winp = t
                best_rolls = i
        # 存入全局表
        choose[score][opposcore] = best_rolls
        win_p[score][opposcore] = max_winp
        return max_winp

    # 双重循环填充所有状态（0~99）
    for i in range(100):
        for j in range(100):
            Win_prob(i, j)


# ==================== 5. 模块加载时自动建表 ====================
Preparation()   # 执行后 choose 和 win_p 被填满


# ==================== 6. 最终策略（问题12） ====================
def final_strategy(score, opponent_score):
    """直接查全局 choose 表"""
    return choose[score][opponent_score]
##########################
# Command Line Interface #
##########################

# 注意：本节函数无需修改。它使用了课程尚未涉及的高级 Python 特性。


@main
def run(*args):
    """读取命令行参数并调用相应函数。"""
    import argparse

    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument(
        "--run_experiments", "-r", action="store_true", help="运行策略实验"
    )

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
