import time
import pandas as pd
import numpy as np

import fileTouch


class SetHeatAr(object):
    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    start = time.time()
    SHA = SetHeatAr()
    SHA.run()
    end = time.time()
    print("执行时间:%.2f" % (end-start))
