class classproperty:
    def __init__(cls, fget=None, fset=None, fdel=None):
        cls.fget = fget
        cls.fset = fset
        cls.fdel = fdel

    def getter(cls, func):
        cls.fget = func
        return cls

    def setter(cls, func):
        cls.fset = func
        return cls

    def deleter(cls, func):
        cls.fdel = func
        return cls

    def __get__(cls, instance, owner):
        if not cls.fget:
            raise AttributeError("getter não definido")
        # Chamando o método getter como um método de classe
        return cls.fget(owner)

    def __set__(cls, instance, value):
        if not cls.fset:
            raise AttributeError("setter não definido")
        # Chamando o método setter como um método de classe
        cls.fset(instance.__class__, value)

    def __delete__(cls, instance):
        if not cls.fdel:
            raise AttributeError("deleter não definido")
        # Chamando o método deleter como um método de classe
        cls.fdel(instance.__class__)
