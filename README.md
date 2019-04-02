# verify

## 安装模块
克隆或者下载本项目  

`$ git https://github.com/Clarmy/verify.git`

进入模块保存目录后，执行

`$ python setup.py install`

测试是否安装成功，在终端启动Python交互命令行`$ python`，然后导入`verify`模块，若无报错，则安装成功

```
>>> import verify
>>>
```

## 配置EC数值预报路径信息
编辑 `config/config.json`文件，设置ECMWF数值预报存放的文件根目录，其格式为：
```json
{
  "ECMWF":{
    "path":"/mnt/data3/DATA/EC_interp"
  }
}
```

## 查找起报时次与预报时次的文件路径
对单次预报的查询，查询2019年3月5日20时起报的2019年3月7日20点的预报结果路径对。
```python
>>> from verify import Ties
>>> from pprint import pprint
>>> myties = Ties('ECMWF')
>>> pprint(myties.fetch_tie('2019030520','2019030720'))
{'forecast_time': '2019030720',
 'initial_time': '2019030520',
 'path_tie': ('/mnt/data3/DATA/EC_interp/2019030520/G_2019030720.nc',
              '/mnt/data3/DATA/EC_interp/2019030720/G_2019030720.nc')}
```

对某一个起报时间的所有预报结果路径的查询
```python
>>> pprint(myties.fetch_ties('2019030520'))
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
```
其中每个元组都是一个(预报-真值)对，其中前一个是预报结果路径，后一个是真值（分析场）路径。

## 计算误差参数

**abs_mean_error : 平均绝对误差**   
**mean_error : 平均误差**   
**rms_error : 均方根误差**   
**std_error : 误差标准差**   

指定起报时间、预报时间、变量名，但不指定区域和层次
```python
>>> from verify import VerifyHandler
>>> vfh = VerifyHandler('ECMWF')
>>> vfh.load_arrays('2018122420','2018122508','rh')
>>> pprint(vfh.errors)
{'abs_mean_error': 9.056163576980465,
 'forecast_time': '2018122508',
 'initial_time': '2018122420',
 'mean_error': -1.4344456,
 'rms_error': 12.610096,
 'std_error': 12.528242,
 'variable': 'rh'}
```
指定区域为北京
```python
>>> vfh.load_arrays('2018122420','2018122508','rh',area='Beijing')
>>> pprint(vfh.errors)
{'abs_mean_error': 7.114058254076087,
 'area': 'Beijing',
 'forecast_time': '2018122508',
 'initial_time': '2018122420',
 'mean_error': -6.107779947916667,
 'rms_error': 7.992441161221001,
 'std_error': 5.155011654107632,
 'variable': 'rh'}
```
指定层次为500hPa
```python
>>> vfh.load_arrays('2018122420','2018122508','q',area='Beijing',level=500)
>>> pprint(vfh.errors)
{'abs_mean_error': 0.0001063942261364149,
 'area': 'Beijing',
 'forecast_time': '2018122508',
 'initial_time': '2018122420',
 'level': 500,
 'mean_error': 0.0001063942261364149,
 'rms_error': 0.00010739850948972174,
 'std_error': 1.4652926017713578e-05,
 'variable': 'q'}
```

## 计算二分变量

根据二分变量的边界坐标点列表获取TS评分、ETS评分、Bias评分

```python
>>> from verify import DichotVar

>>> fct = [[0,0],[1,0],[1,1],[0,1]]   # 伪造的预报区域范围边界点
>>> obs = [[0,0],[2,0],[2,0.5],[0,0.5]]    # 伪造的观测区域范围边界点
>>> region = [[0,0],[3,0],[3,3],[0,3]]   # 伪造的整个作用区域范围边界点

>>> dv = DichotVar(fct,obs,region)

# 获取基本面积参数
>>> dv.areas
{'observation': 1.0,
 'forecast': 1.0,
 'hits': 0.5,
 'false_alarms': 0.5,
 'misses': 0.5,
 'total': 9.0}

 # 计算TS评分
 >>> dv.ts
 0.3333333333333333

 # 计算ETS评分
 >>> dv.ets
 0.42

# 计算Bias评分
 >>> dv.bias
 1.0
```
