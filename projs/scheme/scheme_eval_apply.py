import sys

from link import *
from scheme_utils import *
from scheme_reader import read_line
from scheme_builtins import create_global_frame
from ucb import main, trace

##############
# 求值/应用（Eval/Apply） #
##############

def scheme_eval(expr, env: Frame, tail=False): # 可选的第三个参数会被忽略
    """在 Frame ENV 中对 Scheme 表达式 EXPR 求值。

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Link('+', Link(2, Link(2)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # 求值原子
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # 所有非原子表达式都是列表（组合式）
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest # 操作符和操作数

    from scheme_forms import SPECIAL_FORMS # 在此处导入，避免模块加载时的循环依赖
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](rest, env, tail)
    else:
        # BEGIN PROBLEM 3
        procedure = scheme_eval(first, env)
        # 宏
        if isinstance(procedure, MacroProcedure):
            macro_frame = procedure.env.make_child_frame(procedure.formals, rest)
            expansion = scheme_eval(procedure.body, macro_frame)
            return scheme_eval(expansion, env, tail)
        # 普通表达式
        args = map_link(lambda x: scheme_eval(x, env), rest)
        if tail:
            return complete_apply(procedure, args, env, tail)
        else:
            return scheme_apply(procedure, args, env)
        # END PROBLEM 3

def scheme_apply(procedure, args, env, tail=False):
    """在 Frame ENV（当前环境）中将 Scheme 过程 PROCEDURE 应用于实参值
    ARGS（一个 Scheme 列表），返回运算的结果。
    
    如果遇到错误，报SchemeError。
    """
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        # 把 scheme 参数列表转换为 python 列表形式
        arg_list = []
        while args is not nil:
            arg_list.append(args.first)
            args = args.rest
        if procedure.need_env:
            arg_list.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            # 执行内置过程
            return procedure.py_func(*arg_list)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        # 执行 lambda 过程
        # 继承定义时的环境
        procedure_frame = procedure.env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, procedure_frame, tail)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        # 继承调用时的环境
        procedure_frame = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, procedure_frame, tail)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env, tail=False):
    """在 Frame ENV（当前环境）中依次求值 Scheme 列表 EXPRESSIONS 中的
    每个表达式，并返回最后一个表达式的值。

    >>> eval_all(read_line("(1)"), Frame(None))
    1
    >>> eval_all(read_line("(1 2)"), Frame(None))
    2
    """
    # BEGIN PROBLEM 6
    value = None
    while expressions is not nil:
        value = scheme_eval(expressions.first, env, tail and expressions.rest is nil)
        expressions = expressions.rest
    return value
    # END PROBLEM 6

###################################
# 附加挑战：尾递归优化 #
###################################

class Unevaluated:
    """一个待求值的表达式及其所在的环境。"""

    def __init__(self, expr, env):
        """将在 Frame ENV 中求值表达式 EXPR。"""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env, tail=False):
    """在 env 中将过程应用于 args；确保返回结果不是 Unevaluated。"""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env, tail)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env, tail)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """返回一个正确实现尾递归的 eval 函数版本。"""
    def optimized_eval(expr, env, tail=False):
        """在 Frame ENV 中对 Scheme 表达式 EXPR 求值。若 TAIL 为真，
        则返回一个包含待继续求值的表达式的 Unevaluated。
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 2
        while isinstance(result, Unevaluated):
            result = unoptimized_scheme_eval(result.expr, result.env, True)
        return result
        # END OPTIONAL PROBLEM 2
    return optimized_eval






################################################################
# 取消下面一行的注释即可启用尾调用优化 #
################################################################

scheme_eval = optimize_tail_calls(scheme_eval)
