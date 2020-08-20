# -*- coding: utf-8 -*-
# Filename: gen_cal.py

"""
Generate calibration image for OpenIMU.
Created on 2020-02-25
@author: dongxiaoguang
"""

import os
import re
import time
import datetime

def gen_cal(sn, device_name='dmu330',\
            nas_addr='\\\\10.0.0.236\\productionbackup\\dmudata\\',\
            cal_tool_dir=None,\
            out_dir=None):
    '''
    Args:
        sn: a list of SNs whose calibration images are to be created.
        device_name: dmu330 means OpenIMU330BI.
        nas_addr: a path to specify where the factory calibration data is located.
        cal_tool_dir: a path to specify where the required binary tools are located.
            If this is not specified, './cal/' is used.
        out_dir: a path to specify where the generated calibration image is stored.
            If this is not specified, 'cal_tool_dir/work/sn/' is used.
    '''
    sn_fail = []
    # record current work directory
    cwd = os.getcwd()
    # change directory to calibration tools
    if cal_tool_dir is None:
        cal_tool_dir = '.\\cal'
    os.chdir(cal_tool_dir)
    # generate calibration image for this SN
    for i in sn:
        i = i.strip()
        if len(i) < 10:
            print('Invalid SN: {}'.format(i))
            continue
        print('\nProcessing SN: {}'.format(i))
        # find calibration data from NAS
        file_dir = nas_addr + device_name + '\\' + i[0:2] + 'XXXXXXXX\\' + i + '\\'
        tc_report, ic_report = find_latest_report(file_dir)
        if tc_report != '' and ic_report != '':
            local_reports_dir = '.\\work\\{}\\'.format(i)
            if not os.path.exists(local_reports_dir):
                os.makedirs(local_reports_dir)
            print('\t...Copying calibration files to local disk.')
            os.popen("copy {0} work\\{1}\\".format(tc_report,i)).read()
            os.popen("copy {0} work\\{1}\\".format(ic_report, i)).read()
            time.sleep(0.5)
        else:
            print('\t...Calibration data for {} cannot be found.'.format(i))
            continue
        # generate calibration image
        print('\t...Generating calibration image.')
        os.popen("copy work\\{0}\\*Oven*.txt work\\{0}\\TempLUT.txt".format(i)).read()
        os.popen("copy work\\{0}\\*RateTable*.txt work\\{0}\\InertialLUT.txt".format(i)).read()
        time.sleep(0.5)
        os.system(".\\CalGen.exe {} temp".format(i))
        time.sleep(0.5)
        os.system(".\\CalGen.exe {} inert".format(i))
        time.sleep(0.5)
        # check if bin file created successfully
        bin_file = local_reports_dir + '\\' + i + '_cal_image.bin'
        if os.path.exists(bin_file):
            print('\t...Sucesss.')
            if out_dir is not None:
                os.popen("copy {0} {1}".format(bin_file, out_dir))
        else:
            print('\t...Fail.')
            sn_fail.append(i)
    # display fail SNs
    if len(sn_fail) > 0:
        print("\nCannot generate calibration images for the following SNs:")
        print(sn_fail)
    else:
        print('\nAll calibration images are generated successfully.')
    # get back to recorded work directory
    os.chdir(cwd)

def find_latest_report(file_dir):
    '''
    '''
    tc_report = ''
    ic_report = ''
    # find latest report
    latest_report_dir = ''
    latest_create_time = 0.0
    for i in os.listdir(file_dir):
        if os.path.isdir(file_dir + i) and 'Reports_' in i:
            create_time = os.path.getctime(file_dir + i)
            if create_time > latest_create_time:
                latest_create_time = create_time
                latest_report_dir = file_dir + i + '\\'
    if latest_create_time > 0:
        for i in os.listdir(latest_report_dir):
            if 'Oven_Calibrate_Report_Consolidated' in i:
                tc_report = latest_report_dir + i
            elif 'RateTable_Calibrate_Report_Consolidated' in i:
                ic_report = latest_report_dir + i
    return tc_report, ic_report

if __name__ == "__main__":
    # sn = []
    # sn_file = 'D:\\MyDocuments\\desktop\\bin_for_lianshi\\sn.txt'
    # with open(sn_file, 'r') as f:
    #     file_contents = f.read()
    #     sn = file_contents.split('\n')
    sn = re.split(r'[;\n]+', input('sn of 330:')) # 1974000923; 1974000924; 1974000925; 
    gen_cal(sn, out_dir = 'C:\\Users\\chenerkuo\\Desktop\\delay\\')
    input('finished')
    print("330 校准区域起始地址： 0x0801d000~0x08020000")
    os._exit(1)

