# Pre-requisites

## Linux

For linux, using the windows linux subsystem (WSL-2) is good enough. This can be installed through the Microsoft store.
Suggest to install the Ubuntu linux flavor

## Python

Install pip package manager:
$ sudo su 
$ apt update 
$ apt install python3-pip
$ apt install python3.8-venv

## Python virtual environment
See https://realpython.com/python-virtual-environments-a-primer/

Create a python virtual environment, e.g. 'http-api' in the home directory
$ mkdir ~/http-api
$ python3 -m vevn ~/http-api

Select the python virtual environment
$ source ~/http-api/bin/activate

## Fast API
See https://fastapi.tiangolo.com/#requirements

Install the fastapi package
$ pip install "fastapi[standard]"
