import numbers

from scheme_classes import *
from scheme_reader import read_line

#################
# 类型检查 #
#################

def scheme_procedurep(x):
    return isinstance(x, Procedure)

def scheme_listp(x):
    """判断 x 是否为结构良好的列表（假定无环）。"""
    while x is not nil:
        if not isinstance(x, Link):
            return False
        x = x.rest
    return True

def scheme_booleanp(x):
    return x is True or x is False

def scheme_numberp(x):
    return isinstance(x, numbers.Real) and not scheme_booleanp(x)

def is_scheme_true(val):
    """Scheme 中所有值都为真，只有 False 为假。"""
    return val is not False

def is_scheme_false(val):
    """在 scheme_reader 中，只有 False 为假。"""
    return val is False

def scheme_stringp(x):
    return isinstance(x, str) and x.startswith('"')

def scheme_symbolp(x):
    return isinstance(x, str) and not scheme_stringp(x)

def scheme_nullp(x):
    return x == nil

def scheme_atomp(x):
    return (scheme_booleanp(x) or scheme_numberp(x) or scheme_symbolp(x) or
            scheme_nullp(x) or scheme_stringp(x))

def self_evaluating(expr):
    """判断 EXPR 是否求值为其自身。"""
    return (scheme_atomp(expr) and not scheme_symbolp(expr)) or expr is None


#######################
# 参数校验 #
#######################

def validate_type(val, predicate, k, name):
    """返回 VAL。若不满足 PREDICATE(VAL)，则抛出 SchemeError，
    并用 "argument K of NAME" 来描述出错的值。"""
    if not predicate(val):
        msg = "argument {0} of {1} has wrong type ({2})"
        type_name = type(val).__name__
        if scheme_symbolp(val):
            type_name = "symbol"
        raise SchemeError(msg.format(k, name, type_name))
    return val

def validate_procedure(procedure):
    """检查 PROCEDURE 是否为合法的 Scheme 过程。"""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), repl_str(procedure)))

def validate_form(expr, min, max=float('inf')):
    """检查 EXPR 是否为一个合法的列表，其长度至少为 MIN、至多为
    MAX（默认值：无上限）。若不满足则抛出 SchemeError。

    >>> validate_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + repl_str(expr))
    length = len_link(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif length > max:
        raise SchemeError('too many operands in form')

def validate_formals(formals):
    """检查 FORMALS 是否为合法的形参列表——即由互不相同的符号组成的
    Scheme 列表。若形参列表不是符号列表，或存在重复符号，则抛出 SchemeError。

    >>> validate_formals(read_line('(a b c)'))
    """
    symbols = set()
    def validate_and_add(symbol, is_last):
        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Link):
        validate_and_add(formals.first, formals.rest == nil)
        formals = formals.rest
