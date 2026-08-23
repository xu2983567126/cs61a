"""buffer 模块用于辅助遍历各行与各个 token。"""

import math

class Buffer:
    """Buffer 提供了一种跨行访问 token 序列的方式。

    其构造函数接受一个迭代器（称为“source”），每次被查询时返回一个 token 列表
    作为下一行，或返回 None 表示数据结束。

    Buffer 实际上将其 source 返回的这些序列拼接起来，然后通过 pop_first()
    方法每次从中提供一个元素，仅在需要时才会向 source 索取更多序列。

    此外，Buffer 提供一个 current 方法，用于查看下一个将要提供的元素，
    而不会越过它。

    __str__ 方法会打印到目前为止读取到的所有 token（直到当前行末尾），
    并用 >> 标记当前 token。

    >>> buf = Buffer(iter([['(', '+'], [15], [12, ')']]))
    >>> buf.pop_first()
    '('
    >>> buf.pop_first()
    '+'
    >>> buf.current()
    15
    >>> buf.current()   # Calling current twice should not change buf
    15
    >>> buf.pop_first()
    15
    >>> buf.current()
    12
    >>> buf.pop_first()
    12
    >>> buf.pop_first()
    ')'
    >>> buf.pop_first()  # returns None
    """

    def __init__(self, source):
        """
        基于给定的 source 初始化一个 Buffer 实例。
        """
        self.index = 0
        self.source = source
        self.current_line = ()
        self.current()

    def pop_first(self):
        """从 self 中移除并返回下一个元素。若 self 已耗尽其 source，则返回 None。"""
        current = self.current()
        self.index += 1
        return current

    def current(self):
        """返回当前元素；若不存在则返回 None。"""
        while not self.more_on_line():
            try:
                self.index = 0
                self.current_line = next(self.source)
            except StopIteration:
                self.current_line = ()
                return None
        return self.current_line[self.index]

    def more_on_line(self):
        return self.index < len(self.current_line)

    def end_of_line(self):
        return self.current() is None


# 尝试导入 readline 以获得交互式历史记录
try:
    import readline
except:
    pass

class InputReader:
    """InputReader 是一个可迭代对象，用于提示用户输入。"""
    def __init__(self, prompt):
        self.prompt = prompt

    def __iter__(self):
        while True:
            yield input(self.prompt)
            self.prompt = ' ' * len(self.prompt)

class LineReader:
    """LineReader 是一个可迭代对象，会在提示符之后打印各行。"""
    def __init__(self, lines, prompt, comment=";"):
        self.lines = lines
        self.prompt = prompt
        self.comment = comment

    def __iter__(self):
        while self.lines:
            line = self.lines.pop(0).strip('\n')
            if (self.prompt is not None and line != "" and
                not line.lstrip().startswith(self.comment)):
                print(self.prompt + line)
                self.prompt = ' ' * len(self.prompt)
            yield line
        raise EOFError
