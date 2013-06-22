# -*- coding: utf-8 -*-

"""
/* Copyright 2012, Fan Wang(Parai). All rights reserved.
 *
 * This file is part of GaInOS-Studio.
 */
"""
import re, string, os
from config.gainos_tk_cfg import gainos_tk_cfg
from common.Common import *
from config.gainos_tk_os_cfg import *
#定义所有正则表达式
# 1: for comment 
re_comment_type1 = re.compile(r'/\*[^/]*\*/');
re_comment_type2 = re.compile(r'//.*');
## include 
re_include = re.compile(r'\s*#include\s+["<]([^\s]+)[">]');

# 2: for os obj
re_oil_os_obj = re.compile(r'^\s*OS|^\s*TASK|^\s*ALARM|^\s*COUNTER|^\s*RESOURCE')
re_oil_os_obj_type_name = re.compile(r"""
    ^\s*(OS)\s*(\w+)
    |^\s*(TASK)\s*(\w+)
    |^\s*(ALARM)\s*(\w+)
    |^\s*(COUNTER)\s*(\w+)
    |^\s*(RESOURCE)\s*(\w+)
    """, re.VERBOSE)
## for os <general>    
re_oil_os_general = re.compile(r'^\s*(OS)\s*(\w+)')
## for task
re_oil_os_task = re.compile(r'^\s*(TASK)\s*(\w+)')
re_task_SCHEDULE = re.compile(r'SCHEDULE\s*=\s*(\w+)\s*;')
re_task_PRIORITY = re.compile(r'PRIORITY\s*=\s*(\w+)\s*;')
re_task_ACTIVATION = re.compile(r'ACTIVATION\s*=\s*(\w+)\s*;')
re_task_AUTOSTART = re.compile(r'AUTOSTART\s*=\s*(\w+)\s*;')
re_task_StackSize = re.compile(r'StackSize\s*=\s*(\w+)\s*;')

def filter_out_comment(text):
    """text should be just a line"""
    #过滤形如 “/* .. */” 的注释
    grp = re_comment_type1.split(text)
    result = string.join(grp);
    #过滤形如 “//....” 的注释
    grp = re_comment_type2.split(result);
    result = string.join(grp);
    result = string.join(result.split('\n')) #remove the line break
    return(' '+result);

def oil_process_task(item, oscfg):
    grp = re_oil_os_task.search(item).groups();
    if(grp[0] != 'TASK'):
        return
    name = grp[1];
    if(gcfindObj(oscfg.cfg.taskList, name)):
        tsk = gcfindObj(oscfg.cfg.taskList, name)
    else:
        id = len(oscfg.cfg.taskList)
        tsk = Task(name, 10, 512); #use default value
        oscfg.cfg.taskList.append(tsk)
    #now start to process it
    if(re_task_SCHEDULE.search(item)):
        schedule = re_task_SCHEDULE.search(item).groups()[0];
        if(schedule == 'FULL'):
            tsk.preemtable = True;
        else:
            tsk.preemtable = False;
    if(re_task_PRIORITY.search(item)):
        tsk.prio = int(re_task_PRIORITY.search(item).groups()[0]);
    if(re_task_ACTIVATION.search(item)):
        tsk.maxactcnt = int(re_task_ACTIVATION.search(item).groups()[0]) - 1;
    if(re_task_AUTOSTART.search(item)):
        tsk.autostart = bool(re_task_AUTOSTART.search(item).groups()[0]);
    if(re_task_StackSize.search(item)):
        tsk.stksz = int(re_task_StackSize.search(item).groups()[0]);
        
def oil_process(item, oscfg):
    if(re_oil_os_task.search(item)):
        oil_process_task(item, oscfg);
        
def to_oscfg(oilfile, oscfg):
    """convert the standard osek oil file to or merge to oscfg
    return True:convert successfully,else failed
    oscfg -> gainos_tk_os_cfg
    """
    fp = open(oilfile, 'r');
    oneitem = ''; #one item is minimum object such as TASK,ALARM ...
    barcenum = 0; #remember the brace number，when encounter " { ", +1; when " } " -1.
    brace_flag = False; #has " { " encountered or not
    process_one_item_start = False #has match an obj start or not
    for el in fp.readlines():
        #firstly, filter out the comment on this line
        el = filter_out_comment(el);
        if(process_one_item_start == False):
        #{
            #print el
            oneitem = ''; 
            barcenum = 0;
            brace_flag = False;
            if(re_oil_os_obj.search(el)):
                process_one_item_start = True;
                oneitem += el;
                if(el.count('{') > 0):  #so at comment should not include '{}'
                    brace_flag = True;
                    barcenum += el.count('{');
                elif(el.count('}') > 0):
                    barcenum -= el.count('}');
            elif(re_include.search(el)): #include file
                basep = os.path.dirname(oilfile)
                file = re_include.search(el).groups()[0];
                file = basep+file;
                to_oscfg(file, oscfg);
        #}
        else:
        #{
            if(re_include.search(el)): #include file
                basep = os.path.dirname(oilfile)
                file = re_include.search(el).groups()[0];
                file = basep+file;
                print file
                continue;
            if(el.count('{') > 0):  #so at comment should not include '{}'
                brace_flag = True;
                barcenum += el.count('{');
            if(el.count('}') > 0):
                barcenum -= el.count('}');
            oneitem += el;
            if((brace_flag == True) and (barcenum == 0)):
                #filter out the multi-line comment
                oneitem = filter_out_comment(oneitem)
                oil_process(oneitem, oscfg);
                process_one_item_start = False
        #}
    fp.close();
    return True;