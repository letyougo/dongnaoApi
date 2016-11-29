#coding:utf-8



import os



import subprocess

'''
run方法执行某条shell命令
info和err是两个可直接访问的属性
'''
class Shell:


    @property
    def err(self):
        return self.__err

    @property
    def info(self):
        return self.__info


    def __init__(self):
        self.__err = ''
        self.__info = ''

    def run(self,commander):
        p = subprocess.Popen(commander.split(' '),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.__info,self.__err = p.communicate()


