#!/usr/bin/python3
import os
from rich.text import Text
from rich.console import Console
from rich.prompt import Prompt
import json


console = Console()


def cp(string):
    console.print(Text(string, style='bold #00FF00'))


def rp(string):
    console.print(Text(string, style='bold red'))


def run_cmd(str):
    return os.popen(str).read()


# defining error handler decorator
def Error_Handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            rp(f'exception flew by! , {func.__name__} use sudo instead ')
        else:
            cp('commands executed ....')
        finally:
            cp('execution over !!!!')
    return wrapper


# define decorator
def decorate(func):

    def wrap_func():
        cp('*'*100)
        func()
        cp('*'*100)

    return wrap_func


@decorate
def main_menu():
    cp('[1].Status of containers')
    cp('[2].Download new Image')
    cp('[3].Run container')
    cp('[4].Delete Container')
    cp('[5].Network details of container')
    cp('[6].Modify Network details of contaniner')
    rp('[7].Exit')


@Error_Handler
def docker_cn_status():
    # checking docker container status
    cmd = 'docker container stats'
    os.system(cmd)


@Error_Handler
def docker_dwn_image():
    # download images from docker repo
    image_nm_tag = input("Enter image_name:tag ")
    cmd = f'docker pull {image_nm_tag}'
    cp(run_cmd(cmd))


@Error_Handler
def run_container():
    # run container
    image_nm_tag = Prompt.ask("Enter image_name:tag ")
    container_name = Prompt.ask('Enter container name ')
    option = Prompt.ask('enter option : ', choices=['-i', '-it', '-d'])
    cmd = f'docker run {option} --name {container_name} {image_nm_tag}'
    cp(run_cmd(cmd))
    cmd2 = 'docker ps -a |head -n 2'
    cp(run_cmd(cmd2))


@Error_Handler
def delete_container():
    # delete container
    container_name = input('Enter container name ')
    cmd = f'docker rm {container_name}'
    cp(f'{run_cmd(cmd)} container deleted successfully ')


@Error_Handler
def network_detail_container():
    # network details of a container
    cmd = 'docker network inspect bridge'
    l = run_cmd(cmd)
    l = json.loads(l)[0]
    for i in l["Containers"].values():
        cp(
            f'Name => {i["Name"]} | Mac address => {i["MacAddress"]} | ipv4 address =>{i["IPv4Address"]}')


def disconnect_nw(container_name):
    cmd = f'docker network disconnect bridge {container_name}'
    run_cmd(cmd)
    cp(
        f'{container_name} container disconnect from bridge network')


def create_nw():
    cp('creating...... network')
    network = input('enter a new network name : ')
    ip = input('enter ip for network/cidr :')
    cmd = f' sudo docker network create -d bridge --subnet={ip}  {network}'
    run_cmd(cmd)
    cp(f'{network} Network created successfully')


def connect_new_nw(container_name):
    network = input('enter a new network name : ')
    cp(f'connecting..... the container to newly created  {network} network')
    cmd = f'docker network connect {network} {container_name}'
    run_cmd(cmd)
    cp(f'{container_name} container connected to {network} Network')


@Error_Handler
def docker_modify_network():
    cp('Available netwok list :')
    cmd = 'docker network ls | cut -d " " -f4 '
    rp(run_cmd(cmd))
    container_name = input(
        f'Enter container name for disconnect from bridge network : ')
    # disconnect from network
    disconnect_nw(container_name)

    # creating new network
    create_nw()

    # connecting to newly created network
    connect_new_nw(container_name)


def Exit():
    exit()


operations = {
    '1': docker_cn_status,
    '2': docker_dwn_image,
    '3': run_container,
    '4': delete_container,
    '5': network_detail_container,
    '6': docker_modify_network,
    '7': Exit
}

while True:
    main_menu()
    ch = Prompt.ask('Enter choice ', choices=[
                    str(x) for x in range(1, 8)], default='1')
    operations[ch]()
