# 装饰器
# 装饰器的本质就是个函数，将函数做为参数传入到装饰器的函数中，来强化函数
from flask import g,redirect,url_for
from functools import wraps

def login_required(func):
    # @wraps这个装饰器不能忘记写！！！
    @wraps(func)
    def wrapper(*args,**kwargs):
        if hasattr(g,'user'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("user.login"))
    return wrapper