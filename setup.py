'''
essential part of packaging and distribution of python code
'''
from setuptools import setup,find_packages  
from typing import List
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    req_list:List[str]=[]
    try:
        with open(file_path) as file_obj:
         lines=file_obj.readlines()
         for line in lines:
                line=line.strip()
                if line and line!='-e .':
                    req_list.append(line)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        req_list = []
    return req_list
    
print(get_requirements('requirements.txt'))

setup(
    name="Network_Security",
    version="0.0.1",
    author="Raj",
    author_email="raj22f069@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)