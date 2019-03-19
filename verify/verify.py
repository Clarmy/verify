# coding : utf-8
from pprint import pprint as print
import os
import numpy as np
import netCDF4 as nc
import json as js
# import ipdb



class UnknownDatasetError(Exception):
    def __init__(self,message):
        self.message = message



class FetchError(Exception):
    def __init__(self,message):
        self.message = message



class LevelError(Exception):
    def __init__(self,message):
        self.message = message



class Ties():
    """路径打结器"""
    def __init__(self,dataset):
        if dataset in ['ECMWF','EC']:
            self.dataset = 'ECMWF'

            with open('../config/config.json') as f:
                config = js.load(f)
            self.rootpath = config[self.dataset]['path']
        else:
            raise UnknownDatasetError('Unknown dataset')

    @property
    def raw_ties(self):
        """获取预报和真值路径对

        返回值
        -----
        `dict` : 真值路径对
        """
        if not self.rootpath.endswith('/'):
            self.rootpath = self.rootpath + '/'

        if self.dataset == 'ECMWF':
            init_dirs = sorted(os.listdir(self.rootpath))

            tvpaths = {}
            for idir in init_dirs:
                forecast_path = self.rootpath + idir
                forecast_files = sorted(os.listdir(forecast_path))
                refers = []
                for fn in forecast_files:
                    if fn.endswith('08.nc') or fn.endswith('20.nc'):
                        refers.append((self.rootpath+idir+'/'+fn,
                                       self.rootpath+fn[2:-3]+'/'+fn))

                tvpaths[idir] = refers

            return tvpaths
        else:
            raise UnknownDatasetError('Unknown dataset')


    def fetch_tie(self,init_time,forecast_time):
        """获取单次预报路径结

        参数
        ----
        init_time : `str`
            起报时间字符串，例如'2018122420'
        forecast_time : `str`
            指定起报时间下的预报时次，例如'2018122508'

        示例
        ----
        >>> myties = Ties('EC')
        >>> myties.fetch_tie('2019030520','2019030720')
        {'forecast_time': '2019030720',
         'initial_time': '2019030520',
         'path_tie': ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030720.nc',
                      '/mnt/data3/DATA/EC_interp/2019030720/G_2019030720.nc')}

        """
        at = self.raw_ties
        try:
            search_list = at[init_time]
        except KeyError:
            raise FetchError('Can\'t find initial time.')
        for cp in search_list:
            if forecast_time in cp[0].split('/')[-1]:
                return {'initial_time':init_time,
                        'forecast_time':forecast_time,
                        'path_tie':cp}
                break
        else:
            raise FetchError('Can\'t find forecast time.')


    def fetch_ties(self,init_time):
        """获取某个起报时间下所有预报时次的路径结

        参数
        ----
        init_time : `str`
            起报时间字符串，例如'2018122420'

        示例
        ----
        >>> myties = Ties('EC')
        >>> myties.fetch_ties('2019030520')
        {'initial_time': '2019030520',
         'path_ties': [('/mnt/data3/DATA/EC_interp/2019030520/G_2019030520.nc',
                        '/mnt/data3/DATA/EC_interp/2019030520/G_2019030520.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030608.nc',
                        '/mnt/data3/DATA/EC_interp/2019030608/G_2019030608.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030620.nc',
                        '/mnt/data3/DATA/EC_interp/2019030620/G_2019030620.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030708.nc',
                        '/mnt/data3/DATA/EC_interp/2019030708/G_2019030708.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030720.nc',
                        '/mnt/data3/DATA/EC_interp/2019030720/G_2019030720.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030808.nc',
                        '/mnt/data3/DATA/EC_interp/2019030808/G_2019030808.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030820.nc',
                        '/mnt/data3/DATA/EC_interp/2019030820/G_2019030820.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030908.nc',
                        '/mnt/data3/DATA/EC_interp/2019030908/G_2019030908.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030920.nc',
                        '/mnt/data3/DATA/EC_interp/2019030920/G_2019030920.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019031008.nc',
                        '/mnt/data3/DATA/EC_interp/2019031008/G_2019031008.nc'),
                       ('/mnt/data3/DATA/EC_interp/2019030520/G_2019031020.nc',
                        '/mnt/data3/DATA/EC_interp/2019031020/G_2019031020.nc')]}

        """
        at = self.raw_ties
        try:
            ties_list = at[init_time]
        except KeyError:
            raise FetchError('Can\'t find initial time.')
        return {'initial_time':init_time,
                'path_ties':ties_list}



class AnalysError():
    """误差分析对象

    输入参数
    --------
    array1 : `list` | `ndarray`
        待检验数组（预报）
    array2 : `list` | `ndarray`
        检验标准数组（真值）

    """
    def __init__(self,array1,array2):
        self._array1 = np.array(array1)
        self._array2 = np.array(array2)

    @property
    def mean_error(self):
        """平均误差"""
        return np.mean(self._array1 - self._array2)

    @property
    def abs_mean_error(self):
        """绝对平均误差"""
        return np.mean(np.abs(self._array1 - self._array2))

    @property
    def rms_error(self):
        """均方根误差"""
        return np.sqrt(np.mean((self._array1 - self._array2)**2))

    @property
    def std_error(self):
        """误差标准差"""
        error = self._array1 - self._array2
        return np.sqrt(np.mean((error - np.mean(error))**2))



class AreaError():
    """区域误差"""
    pass



class VerifyHandler():
    """检验处理器"""
    def __init__(self,dataset):
        self.dataset = dataset

    def load_arrays(self,init_time,forecast_time,variable,level,area):
        """加载数据

        输入参数
        -------
        init_time : `str`
            起报时间，例如2019年1月1日08时：'2019010108'
        forecast_time : `str`
            预报时间，该起报时间所对应的某一预报时间，例如2019年1月3日20时：'2019010320'
        variable : `str`
            变量名，例如高空温度't'。
        level : `int`
            高度层变量，如700hPa则该参数输入700
        area : `str` | `tuple` | `list`
            区域参数，若按经纬范围输入参数，则其格式为(lon_left, lon_right, lat_lower,
            lat_upper)。若按地区名称输入参数， 则其为一个地名（省、直辖市、自治区）的拼音。
            例如北京市为'Beijing'。注意：陕西为'Shaanxi'，山西为'Shanxi'。
            全国为'NationalBoundary'

        示例
        ----
        >>> vfh = VerifyHandler('EC')
        >>> vfh.load_arrays('2018122420','2018122620','t',700,'Beijing')
        """
        tie = Ties(self.dataset)
        tie_dict = tie.fetch_tie(init_time,forecast_time)
        forecast_pfn = tie_dict['path_tie'][0]
        truevalue_pfn = tie_dict['path_tie'][1]

        try:
            fctobj = nc.Dataset(forecast_pfn)
        except FileNotFoundError:
            print('Can\'t find forecast file.')
            exit()
        try:
            trvobj = nc.Dataset(truevalue_pfn)
        except FileNotFoundError:
            print('Can\'t find true value file.')
            exit()
        try:
            fct_array = fctobj.variables[variable][:]
        except KeyError:
            print('Can\'t find variable name.')
            exit()

        trv_array = trvobj.variables[variable][:]
        lon = fctobj.variables['lon'][:]
        lat = fctobj.variables['lat'][:]

        if type(area) in [tuple, list] and len(area) == 4:
            left,right,lower,upper = area
            def nearist_index(array,value):
                dist = []
                for i,a in enumerate(array):
                    dist.append((abs(a-value),i))
                nearist = min(dist)
                return nearist[1]
            ileft = nearist_index(lon,left)
            iright = nearist_index(lon,right)
            ilower = nearist_index(lat,lower)
            iupper = nearist_index(lat,upper)

            fct_array = fct_array[:,ilower:iupper,ileft:iright]
            trv_array = trv_array[:,ilower:iupper,ileft:iright]

        elif type(area) == str:
            # 根据用户指定的区域名称获取该区域内的数据
            from matplotlib.path import Path

            # 编制全区域坐标网及其列表
            lons, lats = np.meshgrid(lon,lat)
            coords = list(zip(lons.flatten(),lats.flatten()))

            # 加载区域边界
            with open('../config/regions/%s.geojson' % area) as f:
                boundary = js.load(f)['geometry']['coordinates'][0][0]

            # 边界路径对象
            path = Path(boundary)

            # 识别边界内外
            flatten_mask = path.contains_points(coords)

            # 将边界内外的布尔值颠倒作为遮罩标志数组
            mask = np.invert(flatten_mask.reshape((len(lat),len(lon))))

            # 根据实际数据的层次对遮罩数组进行叠层处理
            mask = np.stack([mask] * fct_array.shape[0])

            # 对预报和真值数组进行遮罩
            fct_array = np.ma.masked_where(mask,fct_array)
            trv_array = np.ma.masked_where(mask,trv_array)

        else:
            print('Parameter area is incorrect')
            exit()

        if variable in ['t','q','r']:
            # tlev : [850., 700., 500.]
            tlev = list(fctobj.variables['tlev'][:])
            try:
                lev_index = tlev.index(level)
            except ValueError:
                raise LevelError('%s is not in tlevel range, '
                                 'please choose level in [850, 700, 500]'%level)
        elif variable in ['u','v','at']:
            # ulev : [500., 400., 300., 250., 200., 150.]
            ulev = list(fctobj.variables['ulev'][:])
            try:
                lev_index = ulev.index(level)
            except ValueError:
                raise LevelError('%s is not in ulevel range, '
                             'please choose level in '
                             '[500, 400, 300, 250, 200, 150]'%level)

        self._arrays = {'initial_time':init_time,
                        'forecast_time':forecast_time,
                        'variable':variable,
                        'level':level,
                        'area':area,
                        'fct_array':fct_array[lev_index],
                        'trv_array':trv_array[lev_index]}

    @property
    def errors(self):
        try:
            self._arrays
        except AttributeError:
            print('Please load arrays firstly.')
        error = AnalysError(self._arrays['fct_array'],
                            self._arrays['trv_array'])
        return {'initial_time':self._arrays['initial_time'],
                'forecast_time':self._arrays['forecast_time'],
                'variable':self._arrays['variable'],
                'level':self._arrays['level'],
                'area':self._arrays['area'],
                'mean_error':error.mean_error,
                'abs_mean_error':error.abs_mean_error,
                'rms_error':error.rms_error,
                'std_error':error.std_error}



if __name__ == '__main__':
    vfh = VerifyHandler('EC')
    vfh.load_arrays('2018122420','2018122508','t',700,'Heilongjiang')

    print(vfh._arrays)
