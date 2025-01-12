from setuptools import setup, find_packages

setup(
    name='Integral_flask_project',
    version='0.0.1',
    description="A powerful Flask extension that provides an integrated solution for building robust web applications with WebSocket support, JWT authentication, database management, email handling, and CORS configuration.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Conectar Wali SAS',
    author_email='dev@conectarwalisas.com.co',
    url='https://github.com/ConectarWali/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
