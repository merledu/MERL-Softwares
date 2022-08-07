import re
import statistics
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
from termcolor import colored
from pathlib import *
import csv


class Per_Gate_Info():
    
    def __init__(self,cell_name,path):
        self.cell_name = cell_name
        self.path=path
        self.dic={}
        
    def construct(self):
        # 'all' means all cells are extracted 
        if self.cell_name == "all":
            cell_names=self.extract_cell_name(self.path)

        # specific cells are extracted
        else:
            cell_names = self.extract_gateList(self.cell_name)

        for i in cell_names:
            self.filter1(i,self.path)
            func=self.extract_function_of_cell()
            area=self.area_of_cell()
            leakage=self.extract_leakage_power()
            name=self.extract_pin_name()
            direction=self.extract_direction_of_pins()
            max_trans=self.extract_max_transition_of_pins()
            max_cap=self.extract_max_capacitance()
            sort_of_input_pins=self.sort_the_input_output_pin(name,max_trans,direction)
            name=sort_of_input_pins[0]
            max_trans=sort_of_input_pins[1]
            direction=sort_of_input_pins[2]
            
            input_trans_fall=self.extract_input_transition_of_input_pins_fall()
            out_cap_fall=self.extract_output_capacitance_of_input_pins_fall()
            delay_fall=self.extract_delay_of_input_pins_fall()
            input_trans_rise=self.extract_input_transition_of_input_pins_rise()
            out_cap_rise=self.extract_output_capacitance_of_input_pins_rise()
            delay_rise=self.extract_delay_of_input_pins_rise()
            input_trans_power_fall=self.extract_input_transition_of_input_pins_power_fall()
            out_cap_power_fall=self.extract_output_capacitance_of_input_pins_power_fall()
            delay_power_fall=self.extract_delay_of_input_pins_power_fall()
            input_trans_power_rise=self.extract_input_transition_of_input_pins_power_rise()
            out_cap_power_rise=self.extract_output_capacitance_of_input_pins_power_rise()
            delay_power_rise=self.extract_delay_of_input_pins_power_rise()

            # ******************* CONSTRAINTS ******************************
            if len(input_trans_fall)==0 or len(input_trans_rise)==0 or len(out_cap_fall)==0 or len(out_cap_rise)==0 or len(delay_fall)==0 or len(delay_rise)==0:
                print(colored(f"EXTRACTION OF THE DATA FROM CELL ({i}) IS UNSUCCESSFULL",'red'))
                continue

            elif direction.count('output') > 1:
                print(colored(f"EXTRACTION OF THE DATA FROM CELL ({i}) IS UNSUCCESSFULL",'red'))
                continue

            print(colored(f"EXTRACTION OF THE DATA FROM CELL ({i}) IS SUCCESSFULL",'green'))
            self.dic[i]=dict()
            self.dic[i]['pin name']=name
            self.dic[i]['Max_Transition']=max_trans
            self.dic[i]['Max_Capacitance']=max_cap
            self.dic[i]['Direction']=direction
            self.dic[i]['function']=func
            self.dic[i]['Area']=area
            self.dic[i]['leakage']=leakage
            self.dic[i]['Input Transition Fall']=input_trans_fall
            self.dic[i]['Output Capacitance Fall']=out_cap_fall
            self.dic[i]['Input Transition Rise']=input_trans_rise
            self.dic[i]['Output Capacitance Rise']=out_cap_rise
            self.dic[i]['Input Transition Power Fall']=input_trans_power_fall
            self.dic[i]['Output Capacitance Power Fall']=out_cap_power_fall
            self.dic[i]['Input Transition Power Rise']=input_trans_power_rise
            self.dic[i]['Output Capacitance Power Rise']=out_cap_power_rise
            index_of_max_delay_fall=self.Max(input_trans_fall,out_cap_fall,delay_fall)
            index_of_max_delay_rise=self.Max(input_trans_rise,out_cap_rise,delay_rise)
            self.dic[i]['pin max delay fall']=name[index_of_max_delay_fall]
            self.dic[i]['pin max delay rise']=name[index_of_max_delay_rise]
            index_of_max_delay_power_fall=self.Max(input_trans_power_fall,out_cap_power_fall,delay_power_fall)
            
            index_of_max_delay_power_rise=self.Max(input_trans_power_rise,out_cap_power_rise,delay_power_rise)
        
            self.dic[i]['pin max delay power fall']=name[index_of_max_delay_power_fall]
            self.dic[i]['pin max delay power rise']=name[index_of_max_delay_power_rise]
            col1=self.max_value(out_cap_fall[index_of_max_delay_fall],delay_fall[index_of_max_delay_fall])
            self.dic[i]['max delay col fall']=col1
            col2=self.max_value(out_cap_rise[index_of_max_delay_rise],delay_rise[index_of_max_delay_rise])
            self.dic[i]['max delay col rise']=col2
            col3=self.max_value(out_cap_power_fall[index_of_max_delay_power_fall],delay_power_fall[index_of_max_delay_power_fall])
            self.dic[i]['max delay col power fall']=col3
            col4=self.max_value(out_cap_power_rise[index_of_max_delay_power_rise],delay_power_rise[index_of_max_delay_power_rise])
            self.dic[i]['max delay col power rise']=col4
            #self.delay_vs_output_capacitance_graph(i,out_cap_fall[index_of_max_delay_fall],out_cap_rise[index_of_max_delay_rise],col1,col2,'Output Capacitance','Delay')

        open1=open('cell_info.csv','w').close()
        open1=open('cell_info.csv','a')
        write1=csv.writer(open1)
        write1.writerow(['Cell Name','Pin name','Max Transition','Max Capacitance','Direction','function','Area','Leakage','Input Transition Fall','Output Capacitance Fall','Input Transition Rise','Output Capacitance Rise','Input Transition Power Fall','Output Capacitance Power Fall','Inupt Transition Power Rise','Ouput Capacitance Power Rise','Pin Max Delay Fall','Pin Max Delay Rise','Pin Max Delay Power Fall','Pin Max Delay Power Rise','Delay Col Fall','Delay Col Rise','Delay Power Col Fall','Delay Power Col Rise'])
        for i in self.dic.keys():
            write1.writerow([i,self.dic[i]['pin name'],self.dic[i]['Max_Transition'],self.dic[i]['Max_Capacitance'],self.dic[i]['Direction'],self.dic[i]['function'],self.dic[i]['Area'],self.dic[i]['leakage'],self.dic[i]['Input Transition Fall'],self.dic[i]['Output Capacitance Fall'],self.dic[i]['Input Transition Rise'],self.dic[i]['Output Capacitance Rise'],self.dic[i]['Input Transition Power Fall'],self.dic[i]['Output Capacitance Power Fall'],self.dic[i]['Input Transition Power Rise'],self.dic[i]['Output Capacitance Power Rise'],self.dic[i]['pin max delay fall'],self.dic[i]['pin max delay rise'],self.dic[i]['pin max delay power fall'],self.dic[i]['pin max delay power rise'],self.dic[i]['max delay col fall'],self.dic[i]['max delay col rise'],self.dic[i]['max delay col power fall'],self.dic[i]['max delay col power rise']])

    def extract_gateList(self,cell_name):
        z=self.extract_cell_name(self.path)
        filter_object = filter(lambda a: f"_{cell_name}" in a, z)
        return list(filter_object)
       

    def extract_cell_name(self,path):
        file  = open(path,'r')
        content = file.readlines()

        #for cell names
        countt = 0
        cell_names = []

        for a in content:
            ab= re.search("^\    cell\ \(.*\)\ {$",a)
            if ab:
                countt +=1
                chhh = a.strip('cell ("')
                ppp = chhh[:-5]
                cell_names.append(ppp)
        file.close()
        return cell_names

    def extract_leakage_power(self):
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        leakage=re.search('\        cell_leakage.*',r1)
        if leakage:
            leakage=leakage[0]
            leakage=re.search('[0-9].*[.][0-9].*[0-9]',leakage)
            f1.close()
            return float(leakage[0])

    def area_of_cell(self):
        #for area of the cell
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        area=re.search("\        area.*",r1)
        area=area[0]
        area=re.search('[0-9].*[.][0-9].*[0-9]',area)
        f1.close()
        if area :
            return float(area[0])



    def extract_function_of_cell(self):
        f=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        func1=re.findall('\            function.*',r1)
        if func1:
            for i in func1:
                i=re.sub('\ {12}function [:] ["]','',i)
                i=re.sub('["][;]','',i)
                f.append(i)
            return f

    def extract_pin_name(self):
        pin_name=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        pin=re.findall("\ {8}pin.*",r1)
        for i in pin:
            refine = re.sub('\s.*pin\ .*[(]["]','',i)
            refine = re.sub('["][)]\ .*[{]','',refine)
            if refine in pin_name:
                continue
            else:
                pin_name.append(refine)
        return pin_name

    def extract_direction_of_pins(self):
        direction=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        dir = re.findall('\ {12}direction.*',r1)
        for i in dir:
            refine = re.sub('\s.*direction\ [:]\ ["]','',i)
            refine = re.sub('["][;]','',refine)
            direction.append(refine)
        return direction

    def extract_max_transition_of_pins(self):
        max_transition=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        trans=re.findall(".*max_transition.*",r1)
        for i in trans:
            i1=re.search("[0-9].*[.][0-9].*[^;]",i)
            if i1:
                max_transition.append(i1[0])
        return max_transition
    
    def extract_max_capacitance(self):
        max_cap=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        trans=re.findall("\s{12}capacitance.*",r1)
        for i in trans:
            i1=re.search("[0-9].*[.][0-9].*[^;]",i)
            if i1:
                max_cap.append(i1[0])
        return max_cap

    def extract_input_transition_of_input_pins_fall(self):
        input_transition=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        in_trans=re.findall('(.*timing.*\n\s{16}cell_fall.*)(\n\s{20}inde.*)(\n\s{20}inde.*)',r1)
        for i in range(len(in_trans)):
            in_trans[i]=in_trans[i][1:2]

        for i in in_trans:
            l1=[]
            for j in i:
                refine=re.sub('\s.*index_1[(]["]','',j)
                refine=re.sub('["][)][;]','',refine)
                l1=re.split(',',refine)
            for k in l1:
                l1[l1.index(k)]=float(k)
            input_transition.append(l1)
        return input_transition
    
    def extract_input_transition_of_input_pins_power_fall(self):
        input_transition=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        in_trans= re.findall('(.*internal_power.*\n\s{16}.*fall.*)(\n\s{20}inde.*)(\n\s{20}inde.*)',r1)
        if in_trans:
            for i in range(len(in_trans)):
                in_trans[i]=in_trans[i][1:2]

            for i in in_trans:
                l1=[]
                for j in i:
                    refine=re.sub('\s.*index_1[(]["]','',j)
                    refine=re.sub('["][)][;]','',refine)
                    l1=re.split(',',refine)
                for k in l1:
                    l1[l1.index(k)]=float(k)
                input_transition.append(l1)
            
            return input_transition
        
    def extract_input_transition_of_input_pins_rise(self):
        input_transition=[]
        f1=open(f'{Path.cwd()}/filter.text','r')
        r1=f1.read()
        in_trans=re.findall('(.*timing.*\n\s{16}cell_fall.*)(\n.*){12}(.*index.*)',r1)
        if in_trans:
            for i in range(len(in_trans)):
                in_trans[i]=in_trans[i][2:]

            for i in in_trans:
                l1=[]
                for j in i:
                    refine=re.sub('.*index_1[(]["]','',j)
                    refine=re.sub('["][)][;]','',refine)
                    l1=re.split(',',refine)
                for k in l1:
                    l1[l1.index(k)]=float(k)
                input_transition.append(l1)
            return input_transition
    
    def extract_input_transition_of_input_pins_power_rise(self):
        input_transition=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        in_trans= re.findall('(.*internal_power.*\n\s{16}.*fall.*)(\n.*){13}(.*index.*)',r1)

        if in_trans:
            for i in range(len(in_trans)):
                in_trans[i]=in_trans[i][2:]
            
            for i in in_trans:
                l1=[]
                for j in i:
                    refine=re.sub('.*index_1[(]["]','',j)
                    refine=re.sub('["][)][;]','',refine)
                    l1=re.split(',',refine)
                for k in l1:
                    l1[l1.index(k)]=float(k)
                input_transition.append(l1)
            return input_transition

    def extract_output_capacitance_of_input_pins_fall(self):
        output_capacitance=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        out_cap = re.findall('(.*timing.*\n\s{16}cell_fall.*)(\n.*)(\n\s{20}inde.*)',r1)

        for i in range(len(out_cap)):
            out_cap[i]=out_cap[i][2:]

        for i in out_cap:
            l1=[]
            for j in i:
                refine=re.sub('\s.*index_2[(]["]','',j)
                refine=re.sub('["][)][;]','',refine)
                l1=re.split(',',refine)
            for k in l1:
                l1[l1.index(k)]=float(k)
            output_capacitance.append(l1)
        return output_capacitance
    
    def extract_output_capacitance_of_input_pins_power_fall(self):
        output_capacitance=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        out_cap = re.findall('(.*internal_power.*\n\s{16}.*fall.*)(\n.*)(\n\s{20}inde.*)',r1)
        if out_cap:
            for i in range(len(out_cap)):
                out_cap[i]=out_cap[i][2:]
            
            for i in out_cap:
                l1=[]
                for j in i:
                    refine=re.sub('\s.*index_2[(]["]','',j)
                    refine=re.sub('["][)][;]','',refine)
                    l1=re.split(',',refine)
                for k in l1:
                    l1[l1.index(k)]=float(k)
                output_capacitance.append(l1)
            return output_capacitance

    def extract_output_capacitance_of_input_pins_rise(self):
        output_capacitance=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        out_cap=re.findall('(.*timing.*\n\s{16}cell_fall.*)(\n.*){13}(.*index.*)',r1)

        if out_cap:
            for i in range(len(out_cap)):
                out_cap[i]=out_cap[i][2:]

            for i in out_cap:
                l1=[]
                for j in i:
                    refine=re.sub('index_2[(]["]','',j)
                    refine=re.sub('["][)][;]','',refine)
                    l1=re.split(',',refine)
                for k in l1:
                    l1[l1.index(k)]=float(k)
                output_capacitance.append(l1)
            return output_capacitance
    
    def extract_output_capacitance_of_input_pins_power_rise(self):
        output_capacitance=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        out_cap=re.findall('(.*internal_power.*\n\s{16}.*fall.*)(\n.*){14}(.*index.*)',r1)

        if out_cap:
            for i in range(len(out_cap)):
                out_cap[i]=out_cap[i][2:]
            
            for i in out_cap:
                l1=[]
                for j in i:
                    refine=re.sub('index_2[(]["]','',j)
                    refine=re.sub('["][)][;]','',refine)
                    l1=re.split(',',refine)
                for k in l1:
                    l1[l1.index(k)]=float(k)
                output_capacitance.append(l1)
            return output_capacitance

    def extract_delay_of_input_pins_fall(self):
        delay=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        match = re.findall('(.*timing.*\n\s{16}cell_fall.*)(\n.*){3}(\s{20}value.*)(\n(\s{24}.*){6})',r1)
        for i in range(len(match)):
           match[i]=match[i][2:]
           match[i]=match[i][:-1]

        for i in match:
            l1=[]
            for j in i:
                if i.index(j)==0:
                    refine=re.sub('\s.*values[(](["])','',j)
                    refine=re.sub('["].*','',refine)
                    l1=re.split(',',refine)
                else:
                    refine=re.sub('\s{25}["]','',j)
                    refine=re.sub('[^.*]["][)][;]','',refine)
                    l1+=re.split(',',refine)
            for k in l1:
                if '\\' in k:
                    l1[l1.index(k)]=float(k.replace('\\',''))

                elif '"' in k:
                    l1[l1.index(k)]=float(k.replace('"',''))
                else:
                    l1[l1.index(k)]=float(k)
            delay.append(l1)
        return delay
    
    def extract_delay_of_input_pins_power_fall(self):
        delay=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        match = re.findall('(.*internal_power.*\n\s{16}.*fall.*)(\n.*){3}(\s{20}value.*)(\n(\s{24}.*){6})',r1)
        if match:
            for i in range(len(match)):
                match[i]=match[i][2:]
                match[i]=match[i][:-1]

            for i in match:
                l1=[]
                for j in i:
                    if i.index(j)==0:
                        refine=re.sub('\s.*values[(](["])','',j)
                        refine=re.sub('["].*','',refine)
                        l1=re.split(',',refine)
                    else:
                        refine=re.sub('\s{25}["]','',j)
                        refine=re.sub('[^.*]["][)][;]','',refine)
                        l1+=re.split(',',refine)
                for k in l1:
                    if '\\' in k:
                        l1[l1.index(k)]=float(k.replace('\\',''))

                    elif '"' in k:
                        l1[l1.index(k)]=float(k.replace('"',''))
                    else:
                        l1[l1.index(k)]=float(k)
                delay.append(l1)
            return delay

    def extract_delay_of_input_pins_rise(self):
        delay=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        match = re.findall('(.*timing.*\n\s{16}cell_fall.*)(\n.*){14}(\s{20}value.*)(\n(\s{24}.*){6})',r1)
        if match:
            for i in range(len(match)):
                match[i]=match[i][2:]
                match[i]=match[i][:-1]
            for i in match:
                l1=[]
                for j in i:
                    if i.index(j)==0:
                        refine=re.sub('\s.*values[(](["])','',j)
                        refine=re.sub('["].*','',refine)
                        l1=re.split(',',refine)
                    else:
                        refine=re.sub('\s{25}["]','',j)
                        refine=re.sub('[^.*]["][)][;]','',refine)
                        l1+=re.split(',',refine)
                for k in l1:
                    if '\\' in k:
                        l1[l1.index(k)]=float(k.replace('\\',''))

                    elif '"' in k:
                        l1[l1.index(k)]=float(k.replace('"',''))
                    else:
                        l1[l1.index(k)]=float(k)
                delay.append(l1)
            return delay

    def extract_delay_of_input_pins_power_rise(self):
        delay=[]
        f1=open(f"{Path.cwd()}/filter.text","r")
        r1=f1.read()
        match = re.findall('(.*internal_power.*\n\s{16}.*fall.*)(\n.*){15}(\s{20}value.*)(\n(\s{24}.*){6})',r1)
        if match:
            for i in range(len(match)):
                match[i]=match[i][2:]
                match[i]=match[i][:-1]
            for i in match:
                l1=[]
                for j in i:
                    if i.index(j)==0:
                        refine=re.sub('\s.*values[(](["])','',j)
                        refine=re.sub('["].*','',refine)
                        l1=re.split(',',refine)
                    else:
                        refine=re.sub('\s{25}["]','',j)
                        refine=re.sub('[^.*]["][)][;]','',refine)
                        l1+=re.split(',',refine)
                for k in l1:
                    if '\\' in k:
                        l1[l1.index(k)]=float(k.replace('\\',''))

                    elif '"' in k:
                        l1[l1.index(k)]=float(k.replace('"',''))
                    else:
                        l1[l1.index(k)]=float(k)
                delay.append(l1)
            return delay

    def sort_the_input_output_pin(self,pin_name,max_transition,direction):
        if len(pin_name)!=len(max_transition):
            pin_name.remove(pin_name[-1])
            direction.remove(direction[-1])
        
    
        for i in pin_name:
            if direction[pin_name.index(i)]=='output':
                max_tran=max_transition[pin_name.index(i)]
                max_transition.remove(max_tran)
                max_transition.append(max_tran)
                direct=direction[pin_name.index(i)]
                direction.pop(pin_name.index(i))
                direction.append(direct)
                pin_name.remove(i)
                pin_name.append(i)
        return [pin_name,max_transition,direction]




    def filter1(self,cell_name,path):
        current= Path.cwd()
        f = open(path,"r")
        r1 = f.readlines()
        f1=open(f"{current}/filter.text","w").close()
        f1 = open(f"{current}/filter.text","a")
        interrupt=0
        home=cell_name
    
        for i in r1:
            if re.search(f"\    cell.*{home}.*",i):
                if interrupt == 1:
                    interrupt=0
                    break
                elif interrupt ==0:
                    interrupt=1
                    f1.write(i)
            elif interrupt ==1:
                if re.search("^\    cell\ \(.*\)\ {$",i):
                    if interrupt == 1:
                        interrupt=0
                        break
                    elif interrupt ==0:
                        interrupt=1
                        f1.write(i)

                elif interrupt==1:
                    f1.write(i)

        
        f1.close()


    def Max(self,input_trans_list,output_cap_list,delay_list):
        max_val=float(0)
        max_index=int(0)
        for i in range(len(input_trans_list)):
            delay_array=np.array(delay_list[i])
            delay_array=np.reshape(delay_array,(7,7))
            in_index=input_trans_list[i].index(statistics.median(input_trans_list[i]))
            out_index=output_cap_list[i].index(statistics.median(output_cap_list[i]))
            if delay_array[out_index][in_index] >max_val:
                max_val=delay_array[out_index][in_index]
                max_index=(max_index+i)-max_index
        return max_index
    
    def max_value(self,cap,delay):
        delay_array=np.array(delay)
        delay_array=np.reshape(delay_array,(7,7))
        column_index=cap.index(statistics.median(cap))
        l1=[]

        for i in delay_array[:,[column_index]].tolist():
            l1.append(i[0])
        return l1

    def across_cell_func(self,ob1):
        l1=[]
        for i in ob1.dic.keys():
            if ob1.dic[i]['function'] is not None:
                if ob1.dic[i]['function'][0] not in l1:
                    l1.append(ob1.dic[i]['function'][0])
        
        return l1


    #def delay_vs_output_capacitance_graph(self,name_of_cell,cap_fall,cap_rise,del_fall,del_rise,label1,label2):
    #
    #    f = plt.figure()
    #    plt.title(name_of_cell)
    #    f.set_figwidth(10)
    #    f.set_figheight(10)
    #    plt.plot(cap_fall,del_fall,color='blue',label='Cell Fall',marker='o',linestyle='dashed',markersize=12)
    #    plt.plot(cap_rise,del_rise,color='green',label='Cell Rise',marker='o',linestyle='dashed',markersize=12)
#
    #    plt.legend(['CELL FALL','CELL RISE'],loc='upper left')
    #    plt.xlabel(label1)
    #    plt.ylabel(label2)
    #    plt.show()
    #    plt.savefig('Delay vs Output Capacitance.jpeg')

         #for i,j in zip(cap_fall[max_delay_fall],variable1):
        #    plt.annotate(f'{(i,j)}',(i,j))
        #
        #for i,j in zip(cap_rise[max_delay_rise],variable2):
        #    plt.annotate(f'{(i,j)}',(i,j))



#MAIN
#ob1=Per_Gate_Info('and2_1',f'{Path.cwd()}/sky130_fd_sc_hd__tt_025C_1v80.lib')











#FOR GUI
#def browse(self):
#            fileName = QtWidgets.QFileDialog.getOpenFileName(MainWindow,'Open file',f'{Path.cwd()}','lib files (*.lib)')
#            self.lineEdit.setText(fileName[0])
#            self.lineEdit.setReadOnly(1)



       