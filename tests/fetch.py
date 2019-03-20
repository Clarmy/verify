# coding : utf-8
'''
测试路径结功能
'''
import os
import sys
sys.path.insert(0,
        os.path.abspath(os.path.join(os.path.dirname(__file__), '../verify')))
from pprint import pprint
from verify import Ties

def main():
    # 测试对单次预报的查询
    myties = Ties('EC')
    print('fetch tie:')
    pprint(myties.fetch_tie('2019030520','2019030720'))

    # 测试单次预报查询超出界限，将抛出异常信息
    # print('fetch tie (overflow):')
    # pprint(myties.fetch_tie('2019030520','2019032020'))

    # 测试对某个起报时间下所有预报的查询
    print('fetch ties:')
    pprint(myties.fetch_ties('2019030520'))

    # 测试对某个起报时间下所有预报的查询，超出界限，抛出异常信息
    # print('fetch ties (overflow):')
    # pprint(myties.fetch_ties('2020030520'))

if __name__ == '__main__':
    main()
