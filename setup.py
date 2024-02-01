from setuptools import setup, find_packages

setup(
    name='FOXFORD_API',
    version='0.1.4-alpha-1',
    description='FOXFORD Student API\nБиблиотека для Работы с Бекэндом Платформы FOXFORD',
    long_description="""
FOXFORD Student API

Библиотека для взаимодействия с бекендом платформы FOXFORD, предназначенная для удобной работы с данными и функциональностью, предоставляемой этой образовательной платформой.

Основные функции:
- Получение информации о студентах, курсах и других объектах системы FOXFORD.
- Взаимодействие с данными бекенда для автоматизации процессов.

Эта библиотека позволяет легко интегрировать возможности FOXFORD в ваши приложения, обеспечивая быстрый и эффективный доступ к данным и функциям этой платформы.
Документация: https://volt-diamond.gitbook.io/foxford-api-docs/
""",
    author="VOLT_DIAMOND",
    packages=find_packages(),
    install_requires=[
        'undetected_chromedriver',
        'selenium',
        'requests',
        'aiohttp',
        'packaging',
        'asyncio'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
    license="MIT License"
)