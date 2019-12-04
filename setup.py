from setuptools import setup

__version__ = "1.0"

setup(name='TATOO_code',
      version=__version__,
      description='Inferring stellar ages using tidal-chronology',
      url='https://github.com/GalletFlorian/TATOO',
      author='Florian Gallet',
      author_email='florian.gallet@gmail.com',
      license='CNES/CNRS',
      packages=['TATOO'],
      install_requires=['numpy', 'scipy', 'matplotlib', 'random', 'math', 'stats'],
      zip_safe=False)
