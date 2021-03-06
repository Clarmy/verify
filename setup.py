#!/usr/bin/env python
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='verify',
    version='0.0.1.dev1',
    description='A package to perform verifying NWP',
    url='https://github.com/Clarmy/verify',
    author='Clarmy Lee',
    author_email='liwentao@mail.iap.ac.cn',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='verify NWP',
    py_modules=['verify'],
    data_files=[('regions',['regions/Anhui.geojson',
                            'regions/Beijing.geojson',
                            'regions/Chongqing.geojson',
                            'regions/Fujian.geojson',
                            'regions/Gansu.geojson',
                            'regions/Guangdong.geojson',
                            'regions/Guangxi.geojson',
                            'regions/Guizhou.geojson',
                            'regions/Hainan.geojson',
                            'regions/Hebei.geojson',
                            'regions/Heilongjiang.geojson',
                            'regions/Henan.geojson',
                            'regions/HongKong.geojson',
                            'regions/Hubei.geojson',
                            'regions/Hunan.geojson',
                            'regions/InnerMongolia.geojson',
                            'regions/Jiangsu.geojson',
                            'regions/Jiangxi.geojson',
                            'regions/Jilin.geojson',
                            'regions/Liaoning.geojson',
                            'regions/Macao.geojson',
                            'regions/NationalBoundary.geojson',
                            'regions/Ningxia.geojson',
                            'regions/Qinghai.geojson',
                            'regions/Shaanxi.geojson',
                            'regions/Shandong.geojson',
                            'regions/Shanghai.geojson',
                            'regions/Shanxi.geojson',
                            'regions/Sichuan.geojson',
                            'regions/Taiwan.geojson',
                            'regions/Tianjin.geojson',
                            'regions/Tibet.geojson',
                            'regions/Xinjiang.geojson',
                            'regions/Yunnan.geojson',
                            'regions/Zhejiang.geojson']),
                ('config',['config/config.json'])],
    install_requires=required
)
