# coding : utf-8
'''
测试误差计算功能
'''
import os
import sys
sys.path.insert(0,
        os.path.abspath(os.path.join(os.path.dirname(__file__), '../verify')))
import numpy as np
from pprint import pprint
from verify import AnalysError
from verify import VerifyHandler

def main():
    # 对伪造数组的简单测试
    print('-----------伪造数据测试-----------')
    array1 = np.array([[1,1],[1,1]])
    array2 = np.array([[2,2],[2,2]])
    errors = AnalysError(array1,array2)
    print('array1:')
    pprint(array1)
    print('array2:')
    pprint(array2)

    print('mean error: %s' % errors.mean_error)
    print('abs mean error: %s' % errors.abs_mean_error)
    print('rms error: %s' % errors.rms_error)
    print('std error: %s' % errors.std_error)
    print('\n')

    # 对实际数据的测试
    print('-----------实际数据测试-----------')
    print('\n')
    print("vfh.load_arrays('2018122420','2018122508','rh')")
    vfh = VerifyHandler('EC')
    vfh.load_arrays('2018122420','2018122508','rh')
    pprint(vfh.errors)
    print('\n')

    print("vfh.load_arrays('2018122420','2018122508','rh',area='Jiangsu')")
    vfh.load_arrays('2018122420','2018122508','rh',area='Jiangsu')
    pprint(vfh.errors)
    print('\n')

    print("vfh.load_arrays('2018122420','2018122508','rh',area='Beijing')")
    vfh.load_arrays('2018122420','2018122508','rh',area='Beijing')
    pprint(vfh.errors)
    print('\n')

    print("vfh.load_arrays('2018122420','2018122508','q',area='Beijing')")
    vfh.load_arrays('2018122420','2018122508','q',area='Beijing')
    pprint(vfh.errors)
    print('\n')

    print("vfh.load_arrays('2018122420','2018122508','q',area='Beijing',level=500)")
    vfh.load_arrays('2018122420','2018122508','q',area='Beijing',level=500)
    pprint(vfh.errors)
    print('\n')

    print("vfh.load_arrays('2018122420','2018122508','q',area='Beijing',level=1000)")
    vfh.load_arrays('2018122420','2018122508','q',area='Beijing',level=1000)
    pprint(vfh.errors)
    print('\n')

    print("vfh.load_arrays('2018122420','2018122508','rh',area='Beijing',level=300)")
    vfh.load_arrays('2018122420','2018122508','rh',area='Beijing',level=300)
    pprint(vfh.errors)
    print('\n')



if __name__ == '__main__':
    main()
