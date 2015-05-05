from clld.scripts.util import parsed_args
from clld.scripts.llod import register, llod_func


if __name__ == '__main__':
    llod_func(parsed_args(bootstrap=True))
    register(parsed_args())
