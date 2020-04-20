from functools import wraps, partial


def patch_resource(resource, pre=None, post=None):

    def get_wrapper(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            
            if pre:
                pre(resource)
            ret = func(*args, **kwargs)

            if post:
                post(resource)
            
            return ret
        return wrapper


