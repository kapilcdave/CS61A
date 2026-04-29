import sys

from link import *
from scheme_utils import *
from scheme_reader import read_line
from scheme_builtins import create_global_frame
from ucb import main, trace

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Link('+', Link(2, Link(2)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest

    from scheme_forms import SPECIAL_FORMS # Import here to avoid a cycle when modules are loaded
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        # First, recursively evaluate the operator to get the actual Procedure object
        operator = scheme_eval(first, env)
        # Then, recursively evaluate all the operands (arguments) in the rest of the list
        args = map_link(lambda operand: scheme_eval(operand, env), rest)
        # Finally, apply the evaluated procedure to the evaluated arguments in the current environment
        return scheme_apply(operator, args, env)
        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        args_list = []
        # Convert the Scheme list (Link) of arguments into a normal Python list
        while isinstance(args, Link):
            args_list.append(args.first)
            args = args.rest
        # If the builtin procedure requires the environment, add it to the end of the arguments list
        if procedure.need_env:
            args_list.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            # Call the actual Python function with the unpacked list of arguments
            return procedure.py_func(*args_list)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        # Create a new local frame (environment) for the procedure call.
        # Its parent is the environment where the procedure was DEFINED (procedure.env), giving it lexical scope.
        child_frame = procedure.env.make_child_frame(procedure.formals, args)
        # Evaluate all expressions in the body of the procedure within this new child frame
        return eval_all(procedure.body, child_frame)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        # Create a new local frame for the procedure call.
        # Its parent is the environment where the procedure is CALLED (env), making it dynamically scoped.
        new_frame = env.make_child_frame(procedure.formals, args)
        # Evaluate the body of the mu procedure within this new dynamically-scoped frame
        return eval_all(procedure.body, new_frame)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), Frame(None))
    1
    >>> eval_all(read_line("(1 2)"), Frame(None))
    2
    """
    # BEGIN PROBLEM 6
    result = None
    # Loop through each expression in the Scheme list
    while isinstance(expressions, Link):
        # Evaluate the current expression and store the result
        result = scheme_eval(expressions.first, env)
        # Move to the next expression in the list
        expressions = expressions.rest
    # Return the result of the LAST expression evaluated (or None if the list was empty)
    return result
    # END PROBLEM 6

###################################
# Extra Challenge: Tail Recursion #
###################################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 2
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 2
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
