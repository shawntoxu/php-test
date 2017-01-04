#!/usr/bin/env python
#coding=utf-8
from datetime import datetime
import urllib2
import json
from os import path
import time
import sys

#zabbix output
OK=0
WARN=1
CRITICAL=2

#storage capacity
S_WARN=60
S_CRITICAL=80

#SERVER_URI='10.2.9.13:8888'
#SESSION_CACHE='/etc/zabbix/scripts/ssid'
SESSION_CACHE='./ssid'

#cassandra api
CASSANDRA_LOGIN='http://{}/login'
CASSANDRA_AGENT='http://{}/agents/{}/'
CASSANDRA_EVENT='http://{}/events?reverse=0&timestamp={}'
CASSANDRA_STORAGE='http://{}/storage-capacity/'

CASSANDRA_USER={"username":"monitor","password":"monitor"}

def login(server_uri):
    session_id=cache_ssid('r')
    if len(session_id) != 0:
        return session_id
    else:
        try:
            headers = {'Content-Type': 'application/json'}
            req = urllib2.Request(url=CASSANDRA_LOGIN.format(server_uri),headers=headers,data=json.dumps(CASSANDRA_USER))
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                recv_json = json.load(response)
                ssid = recv_json['sessionid']
                cache_ssid('w',ssid)
                return ssid
        except:
            raise

def cache_ssid(flag,ssid=None):
    if flag == 'r':
        if path.exists(SESSION_CACHE) and path.isfile(SESSION_CACHE):
            f = open(SESSION_CACHE)
            try:
                session_id = f.read()
                return str(session_id)
            finally:
                f.close()
        else:
            return ''
    else:
        f = open(SESSION_CACHE,'w')
        try:
            f.write(str(ssid))
        finally:
            f.close()
'''
{"rack": "rack1","agent_status": {"storage_cassandra": {"updated_at": 1482139973,"status": "up"},"last_seen": 1482139974,"version": "6.0.5","condition": "ALL_OK","install_status": {"error-message": null,"state": null},"jmx": {"updated_at": 1482139973,"status": "up"},"monitored_cassandra": {"updated_at": 1482139973,"status": "up"},"http": {"updated_at": 1482139973,"status": "up"},"stomp": {"updated_at": 1482139974,"status": "up"}},"name": "AMZ-SIN-Cassandra-9-13","agent_install_type": "tarball","dc": "Cassandra"}
监控要求：  status 都为 up， 监控失败直接触发 critical
'''
def cassandra_agent(server_uri,agent_ip):
    sid = login(server_uri)
    if len(sid) != 0:
        try:
            headers = {'opscenter-session': sid}
            req = urllib2.Request(url=CASSANDRA_AGENT.format(server_uri,agent_ip),headers=headers)
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                 recv_json = json.load(response)
                 check_status(recv_json['agent_status'])
        except:
            raise
        
def check_status(agent_status):
    result=0
    objs=['storage_cassandra','jmx','monitored_cassandra','http','stomp']
    for obj in objs:
        s=agent_status[obj]['status'];
        if s!='up':
            result=2
            break
    if result !=0:
      exit_print(CRITICAL)
    else:
      exit_print(OK)
      
'''
[{"level": 1,"event_source": "OpsCenter","message": "Rolling repair succeeded, starting a new run","target_node": null,"api_source_ip": null,"success": null,"source_node": null,"action": 36,"time": "1482141900524000","level_str": "INFO","user": null}]
监控要求：level_str 为WARNING，ALERT的进行 warning ，critical 报警
'''
def cassandra_event(server_uri):
    sid = login(server_uri)
    if len(sid) != 0:
        try:
            micro=get_microTime()
            headers = {'opscenter-session': sid}
            req = urllib2.Request(url=CASSANDRA_EVENT.format(server_uri,micro),headers=headers)
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                 recv_json = json.load(response)
                 if len(recv_json) < 1:
                     exit_print(OK)
                 else:
                     level=recv_json[0]['level_str']
                     if level == 'WARNING':
                        exit_print(WARN)
                     elif level == 'ALERT':
                        exit_print(CRITICAL)
                     else:
                        exit_print(OK)
        except:
            raise

def  get_microTime():
     micro=long(time.time()*1000*1000)
     return micro 
 
'''
根据  used_gb/( free_gb+used_gb) 计算利用率， 超过60 报 warning， 超过 80 报 critical
'''
def cassandra_storage(server_uri):
    sid = login(server_uri)
    if len(sid) != 0:
        try:
            headers = {'opscenter-session': sid}
            req = urllib2.Request(url=CASSANDRA_STORAGE.format(server_uri),headers=headers)
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                 recv_json = json.load(response)
                 used=float(recv_json['used_gb'])
                 free=float(recv_json['free_gb'])
                 r=used*100/(used+free)
                 if r > S_CRITICAL:
                     exit_print(CRITICAL)
                 elif r > S_WARN:
                     exit_print(WARN)
                 else:
                     exit_print(OK)
        except:
            raise
        
def exit_print(level):
    print level
    exit()
    
def usage():
    print "Usage: cassandra server_uri [agent_ip]"
    print "example: \n 10.x.13:8888 agent 10.x.9.13 \n 10.x.9.13:8888 event \n 10.x.9.13:8888 storage "
    exit()
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
    else:    
        server_uri=sys.argv[1]
        monitor_item=sys.argv[2]
        if monitor_item == 'agent':
            agent_ip=sys.argv[3]
            cassandra_agent(server_uri,agent_ip)
        elif monitor_item == 'event':
            cassandra_event(server_uri)
        elif monitor_item == 'storage':
            cassandra_storage(server_uri)
        else:
            print "paramater error"
