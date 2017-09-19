#!/usr/bin/env python3

import sys, getopt, datetime
import os
import configparser
import argparse
from multiprocessing import Process, Queue

queue = Queue()

yuangong_filename = ''
peizhi_filename = ''
shuchu_filename = ''
chengshi_name = ''

try:
   opts, args = getopt.getopt(sys.argv[1:],"C:c:d:o:")
except getopt.GetoptError:
   print ('test.py erro')
   sys.exit(2)
for opt, arg in opts:
   if opt == '-c':
      peizhi_filename = arg
   elif opt == "-d":
      yuangong_filename = arg
   elif opt == "-o":
      shuchu_filename = arg
   elif opt == '-C':
      chengshi_name =arg
    
if os.path.isfile(yuangong_filename) == False:
    print("yuangong_filename bucunzai.")
    exit()
     
if os.path.isfile(peizhi_filename) == False:
    print("peizhi_filename bucunzai.")
    exit()

filename = peizhi_filename
cf = configparser.ConfigParser()
cf.read(filename)
if chengshi_name == '':
    chengshi_name = 'default'.upper()
    JiShuL = float(cf.get(chengshi_name,"JiShuL"))
    JiShuH = float(cf.get(chengshi_name,"JiShuH"))
    YangLao = float(cf.get(chengshi_name,"YangLao"))
    YiLiao = float(cf.get(chengshi_name,"YiLiao"))
    ShiYe = float(cf.get(chengshi_name,"ShiYe"))
    GongShang = float(cf.get(chengshi_name,"GongShang"))
    ShengYu = float(cf.get(chengshi_name,"ShengYu"))
    GongJiJin = float(cf.get(chengshi_name,"GongJiJin"))
    SheBaoJiShu = YangLao + YiLiao + ShiYe + GongShang + ShengYu + GongJiJin
else:
    chengshi_name = chengshi_name.upper()
    JiShuL = float(cf.get(chengshi_name,"JiShuL"))
    JiShuH = float(cf.get(chengshi_name,"JiShuH"))
    YangLao = float(cf.get(chengshi_name,"YangLao"))
    YiLiao = float(cf.get(chengshi_name,"YiLiao"))
    ShiYe = float(cf.get(chengshi_name,"ShiYe"))
    GongShang = float(cf.get(chengshi_name,"GongShang"))
    ShengYu = float(cf.get(chengshi_name,"ShengYu"))
    GongJiJin = float(cf.get(chengshi_name,"GongJiJin"))
    SheBaoJiShu = YangLao + YiLiao + ShiYe + GongShang + ShengYu + GongJiJin   



def shebao(gongzi):
    #a = Config(chengshi_name)
    if gongzi > JiShuH:
        shebao = JiShuH * SheBaoJiShu
    elif gongzi > JiShuL:
        shebao = gongzi * SheBaoJiShu
    elif gongzi > 0:
        shebao = JiShuL * SheBaoJiShu
    else:
        shebao = 0
    return shebao

def jisuan_ynse(ynssdr):
    if ynssdr > 80000:
        ynse = ynssdr * 0.45 -13505
    elif ynssdr > 55000:
        ynse = ynssdr * 0.35 - 5505
    elif ynssdr > 35000:
        ynse = ynssdr * 0.30 -2755
    elif ynssdr > 9000:
        ynse = ynssdr * 0.25 -1005
    elif ynssdr > 4500:
        ynse = ynssdr * 0.20 -555
    elif ynssdr > 1500:
        ynse = ynssdr * 0.10 -105
    elif ynssdr > 0:
        ynse = ynssdr * 0.03
    else:
        ynse = 0
    return ynse
    

def user_info():
    try:

        # yuangong_filename = '/home/shiyanlou/user.csv'
        with open(yuangong_filename, 'r') as f:
            alist = f.readlines()

        blist = []
        clist = []
        for i in alist:
            gonghao = i.split(",")[0]
            # print(gonghao)
            gzje = int(float(i.split(",")[1]))
            # print(gzje)
            SheBao = shebao(gzje)
            # print(SheBao)
            # gzje = gzje * (1 - wuxianyijin)
            ynssdr = gzje - 3500 - SheBao

            ynse = jisuan_ynse(ynssdr)
            shgz = gzje - ynse - SheBao
            blist.append('{},{},{:.2f},{:.2f},{:.2f}'.format(gonghao, gzje, SheBao, ynse, shgz)) 
        clist.append(blist)
        #print(clist[0][0])
        queue.put(clist)
        #print(len(clist[0]))
            # print(ynse)
            # print(shgz)
            # print('{} : {:.2f}'.format(gonghao,(gzje - ynse )))
            # print('{},{},{:.2f},{:.2f},{:.2f}'.format(gonghao,gzje,SheBao,ynse,shgz))
            #with open(shuchu_filename, 'a') as f:
                #f.write(('{},{},{:.2f},{:.2f},{:.2f}'.format(gonghao, gzje, SheBao, ynse, shgz)) + '\n')
    except:
        print("Parameter Error")


def write_info():
    alist = queue.get()
    with open(shuchu_filename, 'a') as f:
       # writer= csv.writer(f)
        for i in range(len(alist[0])):
            f.write(alist[0][i] +','+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +  '\n')

def main():
   
    Process(target=user_info).start()
    Process(target=write_info).start()
    


if __name__=='__main__':
    main()

