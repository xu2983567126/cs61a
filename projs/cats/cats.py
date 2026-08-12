"""Typing test implementation"""

from utils import (
    lower,
    split,
    remove_punctuation,
    lines_from_file,
    count,
    deep_convert_to_tuple,
)
from ucb import main, interact, trace
from datetime import datetime
import random


###########
# Phase 1 #
###########


def pick(paragraphs: list[str], select, k: int) -> str:
    """返回 paragraphs 中第 k 个使 select 函数返回 True 的段落。
    如果不存在这样的段落（因为 k 大于或等于符合条件的段落数），则 pick 返回空字符串。

    Arguments:
        paragraphs: a list of strings representing paragraphs
        select: a function that returns True for paragraphs that meet its criteria
        k: an integer representing which paragraph to return

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    for p in paragraphs:
        if select(p):
            if k == 0:
                return p
            k -= 1
    return ''
    # END PROBLEM 1


def about(keywords: list[str]):
    """返回一个函数，该函数在接受一个段落时，检查该段落是否包含 keywords 中的任何单词。

    为确保准确比较，您需要：

    忽略大小写（将大写和小写字母视为等效）。

    忽略段落中的标点符号。

    只检查 keywords 列表中单词的完全匹配，而不是子串。例如，段落中的 "dogs" 不应匹配 keywords 中的 "dog"。
    
    提示：使用 utils.py 中的 split、lower 和 remove_punctuation 函数。

    Arguments:
        keywords: a list of keywords

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in keywords]), "keywords should be lowercase."

    # BEGIN PROBLEM 2
    def contains(paragraphs):
        paragraphs = split(lower(remove_punctuation(paragraphs)))
        
        for word in paragraphs:
            if word in keywords:
                return True
        return False
    return contains
    # END PROBLEM 2


def accuracy(entered: str, source: str) -> float:
    """返回 entered 中与 source 中对应单词完全匹配的单词百分比。大小写和标点也必须匹配。

    Arguments:
        entered: a string that may contain typos
        source: a model string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    entered_words = split(entered)
    source_words = split(source)
    # BEGIN PROBLEM 3
    len_e = len(entered_words)
    len_s = len(source_words)
    if len_e == 0 and len_s == 0:
        return 100.0
    elif len_e == 0 or len_s == 0:
        return 0.0
    match_words = 0
    for i in range(min(len_e, len_s)):
        if entered_words[i] == source_words[i]:
            match_words += 1
    return 100.0 * match_words / len_e
    # END PROBLEM 3


def wpm(entered: str, elapsed: int) -> float:
    """计算每分钟字数，基于 5 个字符的组数

    Arguments:
        entered: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, "Elapsed time must be positive"
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return len(entered) * 60 /elapsed / 5.0
    # END PROBLEM 4


################
# Phase 4 (EC) #
################


def memo(f):
    """A general memoization decorator."""
    cache = {}

    def memoized(*args):
        immutable_args = deep_convert_to_tuple(args)  # convert *args into a tuple representation
        if immutable_args not in cache:
            result = f(*immutable_args)
            cache[immutable_args] = result
            return result
        return cache[immutable_args]

    return memoized


def memo_diff(diff_function):
    """A memoization function."""
    cache = {}

    def memoized(entered, source, limit):
        # BEGIN PROBLEM EC
        immutable_args = entered, source  # convert *args into a tuple representation
        if immutable_args not in cache:
            result = diff_function(entered, source, limit)
            cache[immutable_args] = result, limit
            return result
        result, cached_limit = cache[immutable_args]
        if limit <= cached_limit:
            return result
        result = diff_function(entered, source, limit)
        cache[immutable_args] = result, limit
        return result
        # END PROBLEM EC

    return memoized


###########
# Phase 2 #
###########

@memo
def autocorrect(entered_word: str, word_list: list[str], diff_function, limit: int) -> str:
    """
    返回 word_list 中与所提供的 entered_word 最接近的单词，该接近程度由 diff_function 确定。
    
    如果 entered_word 包含在 word_list 中，则 autocorrect 返回该单词。

    否则，autocorrect 返回 word_list 中与 entered_word 差异最小的单词。该差异是 diff_function 返回的数字。

    但是，如果 entered_word 与 word_list 中任何单词的最低差异大于 limit，则返回 entered_word 本身。

    Arguments:
        entered_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    if entered_word in word_list:
        return entered_word
    match_word = None
    small_diff = limit + 1
    for word in word_list:
        diff = diff_function(entered_word, word, limit)
        if diff > limit:
            continue
        if diff < small_diff:
            small_diff, match_word = diff, word
    if match_word == None:
        return entered_word
    return match_word
    # END PROBLEM 5


def furry_fixes(entered: str, source: str, limit: int) -> int:
    """返回为了将输入单词转换为源单词而必须更改的最少字符数。
    
    如果字符串长度不等，则长度差将添加到总更改计数中。

    Arguments:
        entered: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> furry_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> furry_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> furry_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> furry_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> furry_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    if limit < 0:
        return 1
    if not entered or not source:
        return abs(len(entered) - len(source))
    modify = entered[0] != source[0]
    return modify + furry_fixes(entered[1:], source[1:], limit - modify)
    # END PROBLEM 6

@memo_diff
def minimum_mewtations(entered: str, source: str, limit: int) -> int:
    """A diff function for autocorrect that computes the edit distance from ENTERED to SOURCE.
    This function takes in a string ENTERED, a string SOURCE, and a number LIMIT.

    Arguments:
        entered: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    # 基本情形
    if abs(len(entered) - len(source)) > limit:
        return limit + 1
    # 全部为空或者相等，不需要编辑
    if not entered and not source or entered == source:
        return 0
    if limit < 0:
        return 1
    # 只有一个为空，编辑次数就是非空的长度（全为插入/删除）
    if not entered:
        return len(source)
    if not source:
        return len(entered)
    # 相同位置字符相同，匹配，不需要编辑
    if entered[0] == source[0]:
        return minimum_mewtations(entered[1:], source[1:], limit)
    len_e, len_s = len(entered), len(source)
     # 1. 替换：修改 entered[0] 为 source[0]
    modify = 1 + minimum_mewtations(entered[1:], source[1:], limit - 1)
    # 2. 插入：在 entered 前插入 source[0]
    # 只有当 entered 长度不大于 source 时才考虑插入
    min_mew = modify
    insert = 1 + minimum_mewtations(entered, source[1:], min(limit - 1, min_mew - 2)) if len_e <= len_s else limit + 1
     # 3. 删除：删除 entered[0]
    # 只有当 entered 长度不小于 source 时才考虑删除
    min_mew = min(min_mew, insert)
    delete = 1 + minimum_mewtations(entered[1:], source, min(limit - 1, min_mew - 2)) if len_e >= len_s else limit + 1
    min_mew = min(min_mew, delete)
    return min_mew
    
        
        


# Ignore the line below
minimum_mewtations = count(minimum_mewtations)


def final_diff(entered: str, source: str, limit: int) -> int:
    """A diff function that takes in a string ENTERED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    return minimum_mewtations(entered, source, limit)


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(entered: list[str], source: list[str], user_id: int, upload) -> float:
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        entered: a list of the words entered so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> entered = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(entered, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    complete = 0
    for i in range(len(entered)):
        if entered[i] == source[i]:
            complete += 1
        else:
            break
    progress = complete / len(source)
    upload({'id': user_id, 'progress': progress})
    return progress
    # END PROBLEM 8


def time_per_word(words: list[str], timestamps_per_player: list[list[int]]) -> dict:
    """Return a dictionary {'words': words, 'times': times} where times
    is a list of lists that stores the durations it took each player to type
    each word in words.

    Arguments:
        words: a list of words, in the order they are entered.
        timestamps_per_player: A list of lists of timestamps including the time
                          each player started typing, followed by the time each
                          player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> result = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> result['words']
    ['collar', 'plush', 'blush', 'repute']
    >>> result['times']
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    ts_by_player = timestamps_per_player  # A shorter name (for convenience)
    # BEGIN PROBLEM 9
    times = []  # You may remove this line
    for timestamp in timestamps_per_player:
        time = []
        for i in range(1, len(timestamp)):
            time.append(timestamp[i] - timestamp[i - 1])
        times.append(time)
    # END PROBLEM 9
    return {'words': words, 'times': times}


def fastest_words(words_and_times: dict) -> list[list[str]]:
    """Return a list of lists indicating which words each player entered fastest.
    In case of a tie, the player with the lower index is considered to be the one who entered it the fastest.

    Arguments:
        words_and_times: a dictionary {'words': words, 'times': times} where
        words is a list of the words entered and times is a list of lists of times
        spent by each player typing each word.

    >>> p0 = [5, 1, 3]  # 玩家0的时间
    >>> p1 = [4, 1, 6]
    >>> fastest_words({'words': ['Just', 'have', 'fun'], 'times': [p0, p1]})
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    check_words_and_times(words_and_times)  # verify that the input is properly formed
    words, times = words_and_times['words'], words_and_times['times']
    pl_idxs = range(len(times))  # contains an *index* for each player
    w_idxs = range(len(words))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    fastest_words_list = [[] for _ in pl_idxs]
    for i in w_idxs:
        min_time = None
        min_pl = -1
        for j in pl_idxs:
            time = get_time(times, j, i)
            if not min_time or time < min_time:
                min_time = time
                min_pl = j
        fastest_words_list[min_pl].append(words[i])
    return fastest_words_list
    # END PROBLEM 10


def check_words_and_times(words_and_times):
    """Check that words_and_times is a {'words': words, 'times': times} dictionary
    in which each element of times is a list of numbers the same length as words.
    """
    assert 'words' in words_and_times and 'times' in words_and_times and len(words_and_times) == 2
    words, times = words_and_times['words'], words_and_times['times']
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all([isinstance(i, (int, float)) for t in times for i in t]), "times lists should contain numbers"
    assert all([len(t) == len(words) for t in times]), "There should be one word per time."


def get_time(times, player_num, word_index):
    """Return the time it took player_num to type the word at word_index,
    given a list of lists of times returned by time_per_word."""
    num_players = len(times)
    num_words = len(times[0])
    assert word_index < len(times[0]), f"word_index {word_index} outside of 0 to {num_words-1}"
    assert player_num < len(times), f"player_num {player_num} outside of 0 to {num_players-1}"
    return times[player_num][word_index]


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    random.shuffle(paragraphs)
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(source)
        print()

        start = datetime.now()
        entered = input()
        if not entered:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(entered, elapsed))
        print("Accuracy:        ", accuracy(entered, source))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)