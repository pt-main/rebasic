from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()


setup(
    name='rebasic',
    author='Pt',
    description='An opensource project for create language translators/compilers/interpreters.',
    author_email='kvantorium73.int@gmail.com',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.10',
    install_requires=[],
    license='Apache 2.0',
    url='https://github.com/pt-main/rebasic',
)
