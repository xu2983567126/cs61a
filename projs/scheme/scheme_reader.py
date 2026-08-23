"""本模块实现了 Scheme 语言的内建数据类型，以及一个 Scheme 表达式的解析器。

除了本文件中定义的类型外，Scheme 中的某些数据类型由其对应的 Python 类型表示：
    number:       int 或 float（整数或浮点数）
    symbol:       string（字符串）
    boolean:      bool（布尔值）
    unspecified:  None

在可能的情况下，Scheme 值的 __repr__ 方法会返回一个求值后能得到该值的
Python 表达式。

在可能的情况下，Scheme 值的 __str__ 方法会返回一个读取后能得到该值的
Scheme 表达式。
"""

import builtins

from ucb import main
from scheme_tokens import tokenize_lines, DELIMITERS

from buffer import Buffer, InputReader, LineReader
from link import Link, nil

quotes = {"'":  'quote', '`':  'quasiquote', ',@': 'unquote-splicing', ',':  'unquote'} # 引用标记（仅用于官方解答）

# Scheme 列表解析器
def scheme_read(src):
    """从 SRC（一个由 token 组成的 Buffer）中读取下一个表达式。

    >>> scheme_read(Buffer(tokenize_lines(['nil'])))
    ()
    >>> scheme_read(Buffer(tokenize_lines(['1'])))
    1
    >>> scheme_read(Buffer(tokenize_lines(['true'])))
    True
    >>> scheme_read(Buffer(tokenize_lines(['(+ 1 2)'])))
    Link('+', Link(1, Link(2)))
    """
    if src.current() is None:
        raise EOFError
    val = src.pop_first() # 取出并移除第一个 token
    if val == 'nil':
        return nil
    elif val == '(':
        if src.current() == ".":
            raise SyntaxError(". cannot be the first token in a list")
        # 第二个参数不应出现在学生解答中
        return read_tail(src)
    elif val in quotes:
        return Link(quotes[val], Link(scheme_read(src), nil))
    elif val not in DELIMITERS:
        return val
    else:
        raise SyntaxError('unexpected token: {0}'.format(val))

def read_tail(src):
    """返回 SRC 中列表的剩余部分，从某个元素或 ) 之前开始。

    >>> read_tail(Buffer(tokenize_lines([')'])))
    ()
    >>> read_tail(Buffer(tokenize_lines(['2 3)'])))
    Link(2, Link(3))
    """
    try:
        if src.current() is None:
            raise SyntaxError('unexpected end of file')
        elif src.current() == ')':
            src.pop_first()
            return nil
        else:
            first = scheme_read(src)
            rest = read_tail(src)
            return Link(first, rest)
    except EOFError:
        raise SyntaxError('unexpected end of file')

# 便捷方法

def buffer_input(prompt='scm> '):
    """返回一个包含交互式输入的 Buffer 实例。"""
    return Buffer(tokenize_lines(InputReader(prompt)))

def buffer_lines(lines, prompt='scm> ', show_prompt=False):
    """返回一个遍历 LINES 的 Buffer 实例。"""
    if show_prompt:
        input_lines = lines
    else:
        input_lines = LineReader(lines, prompt)
    return Buffer(tokenize_lines(input_lines))

def read_line(line):
    """将单个字符串 LINE 作为一个 Scheme 表达式读取。"""
    buf = Buffer(tokenize_lines([line]))
    result = scheme_read(buf)
    if buf.more_on_line():
        raise SyntaxError("read_line's argument can only be a single element, but received multiple")
    return result

# 交互式循环
def read_print_loop():
    """为 Scheme 表达式运行一个读-打印循环。"""
    while True:
        try:
            src = buffer_input('read> ')
            while src.more_on_line():
                expression = scheme_read(src)
                if expression == 'exit':
                    print()
                    return
                print('str :', expression)
                print('repr:', repr(expression))
        except (SyntaxError, ValueError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D 等（Ctrl+D，文件结束）
            print()
            return

@main
def main(*args):
    if len(args) and '--repl' in args:
        read_print_loop()
