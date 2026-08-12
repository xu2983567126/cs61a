from __future__ import annotations # This makes the type annotations work


SOURCE_FILE = __file__


def flatten(s: list) -> list:
    """Returns a flattened version of list s.

    >>> flatten([1, 2, 3])
    [1, 2, 3]
    >>> deep = [1, [[2], 3], 4, [5, 6]]
    >>> flatten(deep)
    [1, 2, 3, 4, 5, 6]
    >>> deep                                # input list is unchanged
    [1, [[2], 3], 4, [5, 6]]
    >>> very_deep = [['m', ['i', ['n', ['m', 'e', ['w', 't', ['a'], 't', 'i', 'o'], 'n']], 's']]]
    >>> flatten(very_deep)
    ['m', 'i', 'n', 'm', 'e', 'w', 't', 'a', 't', 'i', 'o', 'n', 's']
    """
    "*** YOUR CODE HERE ***"
    flatten_list = []
    for item in s:
        if type(item) == list:
            flatten_list += flatten(item)
        else:
            flatten_list += [item]
    return flatten_list


def close_list(s: list[int], k: int) -> list[int]:
    """返回 s 中那些与其索引相差在 k 以内的元素。

    >>> t = [6, 2, 4, 3, 5]
    >>> close_list(t, 0)  # Only 3 is equal to its index
    [3]
    >>> close_list(t, 1)  # 2, 3, and 5 are within 1 of their index
    [2, 3, 5]
    >>> close_list(t, 2)  # 2, 3, 4, and 5 are all within 2 of their index
    [2, 4, 3, 5]
    """
    assert k >= 0
    return [s[i] for i in range(len(s)) if abs(s[i] - i) <= k]


def remove_first(lst: list, elem: int) -> list:
    """ This function removes the first appearance of elem in list lst.

    >>> remove_first([3, 4] , 3)
    [4]
    >>> remove_first([3, 4, 3] , 3)
    [4, 3]
    >>> remove_first([2, 4] , 3)
    [2, 4]
    >>> remove_first([] , 0)
    []
    """
    "*** YOUR CODE HERE ***"
    result_lst = []
    moved = False
    for i in range(len(lst)):
        if lst[i] == elem and not moved:
            moved = True
            continue
        result_lst += [lst[i]]
    return result_lst

def sort(lst: list) -> list:
    """This function returns a sorted version of the list lst.

    >>> sort([6, 2, 5])
    [2, 5, 6]
    >>> sort([2, 3])
    [2, 3]
    >>> sort([3])
    [3]
    >>> sort([])
    []
    """
    "*** YOUR CODE HERE ***"
    if len(lst) <= 1:
        return lst
    small = min(lst)
    return [small] + sort(remove_first(lst, small))


def make_onion(f, g):
    """返回一个函数 can_reach(x, y, limit)，
    返回是否可以通过最多 limit 次仅包含 f、g 和 x 的调用表达式得到结果 y。

    >>> up = lambda x: x + 1
    >>> double = lambda y: y * 2
    >>> can_reach = make_onion(up, double)
    >>> can_reach(5, 25, 4)      # 25 = up(double(double(up(5))))
    True
    >>> can_reach(5, 25, 3)      # Not possible
    False
    >>> can_reach(1, 1, 0)      # 1 = 1
    True
    >>> add_ing = lambda x: x + "ing"
    >>> add_end = lambda y: y + "end"
    >>> can_reach_string = make_onion(add_ing, add_end)
    >>> can_reach_string("cry", "crying", 1)      # "crying" = add_ing("cry")
    True
    >>> can_reach_string("un", "unending", 3)     # "unending" = add_ing(add_end("un"))
    True
    >>> can_reach_string("peach", "folding", 4)   # Not possible
    False
    """
    def can_reach(x, y, limit: int) -> bool:
        if limit < 0:
            return False
        elif x == y:
            return True
        else:
            return can_reach(f(x), y, limit - 1) or can_reach(g(x), y, limit - 1)
    return can_reach


def make_func_repeater(f, x: int):
    """
    >>> increment_repeater = make_func_repeater(lambda x: x + 1, 1)
    >>> increment_repeater(2) #same as f(f(x))
    3
    >>> increment_repeater(5)
    6
    """
    def repeat(times):
        if times == 0:
            return x
        else:
            return f(repeat(times - 1))
    return repeat


def ten_pairs(n: int) -> int:
    """Return the number of ten-pairs within positive integer n.

    >>> ten_pairs(7823952) # 7+3, 8+2, and 8+2
    3
    >>> ten_pairs(55055)
    6
    >>> ten_pairs(9641469) # 9+1, 6+4, 6+4, 4+6, 1+9, 4+6 
    6
    >>> # ban iteration
    >>> from construct_check import check
    >>> check(SOURCE_FILE, 'ten_pairs', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n < 10:
        return 0
    return count_digit(n // 10, 10 - n % 10) + ten_pairs(n // 10)


def count_digit(n: int, digit: int) -> int:
    """Return how many times digit appears in n.

    >>> count_digit(55055, 5) # digit 5 appears 4 times in 55055
    4
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(SOURCE_FILE, 'count_digits', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n == 0:
        return 0
    if n % 10 == digit:
        return 1 + count_digit(n // 10, digit)
    else:
        return count_digit(n // 10, digit)

