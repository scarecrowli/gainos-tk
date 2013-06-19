/* Copyright(C) 2013, GaInOS-TK by Fan Wang. All rights reserved.
 * Generated by GaInOS-TK Studio at 2013-06-19:21-10-07.
 * Don't Modify it by hand.
 * Email: parai@foxmail.com
 * URL: https://github.com/parai/gainos-tk  && http://hi.baidu.com/parai
 */


#include "osek_os.h"
#include "osek_cfg.h"
#include "knl_task.h"
#include "knl_alarm.h"
#include "knl_event.h"
#include <stdio.h>
GenTaskStack(vTaskSender);
GenTaskStack(vTaskReceiver);
GenTaskStack(vTaskMainFunction);
EXPORT const T_GTSK	knl_gtsk_table[cfgOSEK_TASK_NUM]=
{
	GenTaskInfo(vTaskSender,OSNONEAPPMODE|PREEMTABLE,ID_vTaskSenderEvent,vTaskSenderPri),
	GenTaskInfo(vTaskReceiver,OSNONEAPPMODE|PREEMTABLE,ID_vTaskReceiverEvent,vTaskReceiverPri),
	GenTaskInfo(vTaskMainFunction,OSNONEAPPMODE|PREEMTABLE,INVALID_EVENT,vTaskMainFunctionPri),
};

EXPORT const AlarmBaseType knl_almbase_table[cfgOSEK_COUNTER_NUM]=
{
	GenAlarmBaseInfo(30000,1,1), /* vSystemCounter */
};

EXPORT const T_GALM knl_galm_table[cfgOSEK_ALARM_NUM]=
{
	GenAlarmInfo(vAlarmSender,vSystemCounter),
	GenAlarmInfo(vAlarmReceiver,vSystemCounter),
	GenAlarmInfo(vAlarmMainFunction,vSystemCounter),
};

EXPORT const PRI knl_gres_table[cfgOSEK_RESOURCE_NUM]=
{
	/* ceilpri */ 1,  /* RES_SCHEDULER */
};

