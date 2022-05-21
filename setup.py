from setuptools import setup, find_packages

setup(name='slotminer', # 프로젝트 명
      version='0.9.2', # 프로젝트 버전
      url='https://github.com/bytecell/slotminer', # git 웹 주소
      author='bytecell', # 작성자
      author_email='ysjay@chungbuk.ac.kr', # 작성자 이메일
      packages=find_packages(), # 기본 프로젝트 폴더 외에 추가할 폴더
      description='python package for slot extraction (information extraciton) from texts.', 
      long_description=open('README.md').read(), 
      long_description_content_type='text/markdown', 
      install_requires=['cython'], # 설치시 함께 설치할 라이브러리
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
      ]
)

