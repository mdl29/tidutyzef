"""Some utils functions, decorators for tidutizef"""
from functools import wraps
from inspect import signature

def singleton(cls):
    """make the class as singleton"""
    @wraps(cls)
    def fct():
        """
        create a new object if no one exit
        """
        if not fct.instance:
            fct.instance = cls()
        return fct.instance
    fct.instance = None

    return fct

def check_types(fct):
    """
    decorator which check the type of args of the fonction, based on the annotations
    if type don't match, try to cast
    ex :
    @check_types
    f(a: int, b: dict) -> list
    raise TypeError if annotations are not respected and cast is impossible
    """
    #based on CF https://zestedesavoir.com/tutoriels/954/notions-de-python-avancees/6-decorators/

    sig = signature(fct)
    args_types = {p.name: p.annotation for p in sig.parameters.values()
                  if p.annotation != p.empty}
    @wraps(fct)
    def decorated(*args, **kwargs):
        """check for typing error and return the function if no problem"""
        bind = sig.bind(*args, **kwargs)
        args = []

        for name, value in bind.arguments.items():
            typ = args_types.get(name, object)
            if typ and not isinstance(value, typ):
                try:
                    bind.arguments[name] = typ(value) # try cast to the good type
                except:
                    raise TypeError('{0} must be of type {1} or must be castable into {1}'\
                            .format(name, typ.__name__))

        return fct(*bind.args, **bind.kwargs)

    return decorated
