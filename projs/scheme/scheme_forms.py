from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# 特殊形式 #
#################

# 以下各 do_xxx_form 函数都以某个特殊形式的 cdr 作为第一个参数——
# 即不含最前面标识符号（if、lambda、quote 等）的 Scheme 列表。其第二个参数
# 是该形式被求值所在的环境。

def do_define_form(expressions, env, tail=False):
    """求值一个 define 形式。返回被绑定的符号。
    
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env) # evaluating (define x 2)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env) # evaluating (define x (+ 2 8))
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # problem 10
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env) # evaluating (define (f x) (+ x 8))
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2) # 检查 expressions 是长度至少为 2 的列表
    signature = expressions.first
    if scheme_symbolp(signature):
        # 将一个名字绑定到一个值，例如 (define x (+ 1 2))
        validate_form(expressions, 2, 2) # 检查 expressions 是长度恰好为 2 的列表
        # BEGIN PROBLEM 4
        # expressions 是 Link(A, Link(B, nil)) 形式，如 Link(Link('+', Link(2, Link(2))), nil)
        env.define(signature, scheme_eval(expressions.rest.first, env))
        return signature
        # END PROBLEM 4
    elif isinstance(signature, Link) and scheme_symbolp(signature.first):
        # 定义一个具名过程，例如 (define (f x y) (+ x y))
        # BEGIN PROBLEM 10
        formals = signature.rest
        validate_formals(formals)
        body =  expressions.rest
        env.define(signature.first, LambdaProcedure(formals, body, env))
        return signature.first
        # END PROBLEM 10
    else:
        bad_signature = signature.first if isinstance(signature, Link) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))

def do_quote_form(expressions, env, tail=False):
    """求值一个 quote 形式。

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env) # evaluating (quote (+ x 2))
    Link('+', Link('x', Link(2)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 5
    return expressions.first
    # END PROBLEM 5

def do_begin_form(expressions, env, tail=False):
    """求值一个 begin 形式。

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env) # evaluating (begin (print 2) 3)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env, tail)

def do_lambda_form(expressions, env, tail=False):
    """求值一个 lambda 形式。
    
    formals 定义为一个普通的链表，body 定义为一个嵌套的链表。

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env) # evaluating (lambda (x) (+ x 2))
    LambdaProcedure(Link('x'), Link(Link('+', Link('x', Link(2)))), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 7
    body = expressions.rest
    return LambdaProcedure(formals, body, env)
    # END PROBLEM 7

def do_if_form(expressions, env, tail=False):
    """求值一个 if 形式。

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # evaluating (if #t (print 2) (print 3))
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # evaluating (if #f (print 2) (print 3))
    3
    """
    validate_form(expressions, 2, 3)
    if is_scheme_true(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env, tail)
    elif len_link(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env, tail)

def do_and_form(expressions, env, tail=False):
    """求值一个（短路的）and 形式。

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env) # evaluating (and #f (print 1))
    False
    >>> # evaluating (and (print 1) (print 2) (print 4) 3 #f)
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    value = True
    while expressions is not nil:
        if expressions.rest is nil:
            return scheme_eval(expressions.first, env, tail)
        value = scheme_eval(expressions.first, env)
        if is_scheme_false(value):
            return False
        expressions = expressions.rest
    return value
    # END PROBLEM 12

def do_or_form(expressions, env, tail=False):
    """求值一个（短路的）or 形式。

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env) # evaluating (or 10 (print 1))
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env) # evaluating (or #f 2 3 #t #f)
    2
    >>> # evaluating (or (begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    value = False
    while expressions is not nil:
        if expressions.rest is nil:
            return scheme_eval(expressions.first, env, tail)
        value = scheme_eval(expressions.first, env)
        if is_scheme_true(value):
            return value
        expressions = expressions.rest
    return False
    # END PROBLEM 12

def do_cond_form(expressions, env, tail=False):
    """求值一个 cond 形式。

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    while expressions is not nil:
        clause = expressions.first
        validate_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.rest != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if is_scheme_true(test):
            # BEGIN PROBLEM 13
            if clause.rest is nil:
                return test
            return eval_all(clause.rest, env, tail)
            # END PROBLEM 13
        expressions = expressions.rest

def do_let_form(expressions, env, tail=False):
    """求值一个 let 形式。

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env, tail)

def make_let_frame(bindings, env):
    """创建 Frame ENV 的一个子帧，其中包含 BINDINGS 中给出的定义。
    BINDINGS 这个 Scheme 列表必须具有 let 表达式中合法绑定列表的形式：
    每一项都必须是一个包含符号与 Scheme 表达式的列表。
    
    例如，(let ((a 1) (b 2)) b) 是合法的，(let ((a 1) (b a)) b) 是不合法的。
    
    """
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names = vals = nil
    # BEGIN OPTIONAL PROBLEM 1
    while bindings is not nil:
        binding = bindings.first
        validate_form(binding, 2, 2)
        name = binding.first
        val = scheme_eval(binding.rest.first, env)
        names, vals = Link(name, names), Link(val, vals)
        bindings = bindings.rest
    validate_formals(names)
    # END OPTIONAL PROBLEM 1
    return env.make_child_frame(names, vals)



def do_quasiquote_form(expressions, env, tail=False):
    """在 Frame ENV 中对带参数 EXPRESSIONS 的 quasiquote 形式求值。"""
    def quasiquote_item(val, env, level):
        """在 Frame ENV 中，对嵌套在 quasiquote 形式内、深度为 LEVEL 的
        Scheme 表达式 VAL 求值。"""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return map_link(lambda elem: quasiquote_item(elem, env, level), val)

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)

def do_unquote(expressions, env, tail=False):
    raise SchemeError('unquote outside of quasiquote')



#################
# 动态作用域 #
#################

def do_mu_form(expressions, env, tail=False):
    """求值一个 mu 形式。"""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 11
    body = expressions.rest
    return MuProcedure(formals, body)
    # END PROBLEM 11



SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'mu': do_mu_form,
}
