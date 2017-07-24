from setuptools import setup, find_packages

setup(name='asciimon',
      version='0.1.0',
      description='ASCII Art Monster battle game',
      url='https://github.com/lauryndbrown/Monster_ASCII_Game',
      author='Lauryn Brown',
      author_email='lauryndbrown@gmail.com',
      license='GNU GPLv3',
      packages=find_packages(),
      install_requires=[
        'pillow',
        'colorama',
        'ascii_game'
      ],
      entry_points={
        'console_scripts':[
            'asciimon = Monster_ASCII_Game.game:start'
        ]
      }, 
      include_package_data=True,
      zip_safe=False)
