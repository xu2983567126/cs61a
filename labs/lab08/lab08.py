from __future__ import annotations


def without(s: Link, i: int) -> Link:
    """Return a new linked list like s but without the element at index i.

    >>> s = Link(3, Link(5, Link(7, Link(9))))
    >>> without(s, 0)
    Link(5, Link(7, Link(9)))
    >>> without(s, 2)
    Link(3, Link(5, Link(9)))
    >>> without(s, 4)  # There is no index 4, so all of s is retained.
    Link(3, Link(5, Link(7, Link(9))))
    """
    "*** YOUR CODE HERE ***"
    if s is Link.empty:
        return s
    if i == 0:
        return s.rest
    else:
        return Link(s.first, without(s.rest, i - 1))


def duplicate_link(s: Link, val: int) -> None:
    """改变 s，使得每个等于 val 的元素后面都跟着一个额外的 val（一个重复副本）。

    >>> x = Link(5, Link(4, Link(5)))
    >>> duplicate_link(x, 5)
    >>> x
    Link(5, Link(5, Link(4, Link(5, Link(5)))))
    >>> y = Link(2, Link(4, Link(6, Link(8))))
    >>> duplicate_link(y, 10)
    >>> y
    Link(2, Link(4, Link(6, Link(8))))
    >>> z = Link(1, Link(2, Link(2, Link(3))))
    >>> duplicate_link(z, 2) # ensures that back to back links with val are both duplicated
    >>> z
    Link(1, Link(2, Link(2, Link(2, Link(2, Link(3))))))
    """
    "*** YOUR CODE HERE ***"
    if s is Link.empty:
        return
    rest = s.rest
    if s.first == val:
        next = Link(val, rest)
        s.rest = next
    duplicate_link(rest, val)
    


def slice_link(link: Link, start: int, end: int) -> Link:
    """对给定的链表 link 进行切片。
    
    slice_link 应该从 start 开始切片，到 end 之前的一个元素结束
    
    不必支持负数切片。

    >>> link = Link(3, Link(1, Link(4, Link(1, Link(5, Link(9))))))
    >>> new = slice_link(link, 1, 4)
    >>> print(new)
    (1 4 1)
    >>> print(slice_link(link, 0, 2))
    (3 1)
    >>> print(slice_link(link, 0, 6))
    (3 1 4 1 5 9)
    >>> print(slice_link(link, 2, 2))
    ()
    >>> print(slice_link(link, 2, 3))
    (4)
    >>> print(slice_link(link, 3, 100))
    (1 5 9)
    >>> print(slice_link(link, 10, 12))
    ()
    """
    "*** YOUR CODE HERE ***"
    if end <= start:
        return Link.empty
    for _ in range(start):
        link = link.rest
        if link is Link.empty:
            return Link.empty
    ret_link = Link(0)
    node = ret_link
    while end > start and link is not Link.empty:
        node.rest = Link(link.first)
        node = node.rest
        link = link.rest
        end -= 1
    return ret_link.rest

def has_cycle(link: Link) -> bool:
    """Return whether link contains a cycle.

    >>> s = Link(1, Link(2, Link(3)))
    >>> s.rest.rest.rest = s
    >>> has_cycle(s)
    True
    >>> t = Link(1, Link(2, Link(3)))
    >>> has_cycle(t)
    False
    >>> u = Link(2, Link(2, Link(2)))
    >>> has_cycle(u)
    False
    """
    "*** YOUR CODE HERE ***"

def has_cycle_constant(link: Link) -> bool:
    """Return whether link contains a cycle.

    >>> s = Link(1, Link(2, Link(3)))
    >>> s.rest.rest.rest = s
    >>> has_cycle_constant(s)
    True
    >>> t = Link(1, Link(2, Link(3)))
    >>> has_cycle_constant(t)
    False
    """
    "*** YOUR CODE HERE ***"
    if link is Link.empty:
        return False
    fast, slow = link.rest, link
    while fast is not Link.empty and fast.rest is not Link.empty:
        if fast is slow:
            return True
        fast, slow = fast.rest.rest, slow.rest
    return False


class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    (5 7 (8 9))
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '('
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + ')'

