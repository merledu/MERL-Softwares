

import matplotlib.pyplot as plt
import statistics
import mplcursors





def plot_area_vs_leakage(func,ob1):
    name=[]
    area=[]
    leakage=[]
    for i in ob1.dic.keys():
        if ob1.dic[i]['function'] is not None:

            if str(func)==ob1.dic[i]['function'][0]:
                print(type(ob1.dic[i]['function']))
                name.append(i)
                area.append(ob1.dic[i]['Area'])
                leakage.append(ob1.dic[i]['leakage'])
    plt.plot(area, leakage, linestyle='dashed',c="red", marker='o')
    plt.title('Leakage vs Area', fontsize=14)
    plt.xlabel('Area(um)', fontsize=14)
    plt.ylabel('Leakage(nW)', fontsize=14)
    for i,j,k in zip(area,leakage,name):
    
        plt.text(i,j,k.strip("sky130_fd_sc_hd__"))
    
    mplcursors.cursor(hover=True)

    plt.show()
   


def plot_area_vs_rise_delay(func,ob1):
    name=[]
    area=[]
    rise_delay=[]

    for i in ob1.dic.keys():
        if ob1.dic[i]['function'] is not None:
         if func in ob1.dic[i]['function']:
             name.append(i)
             area.append(ob1.dic[i]['Area'])
             rise_delay.append(statistics.median(ob1.dic[i]['max delay col rise']))
        
    plt.plot(area, rise_delay, linestyle='dashed',c="red", marker='o')
    plt.title('Area vs Rise Delay', fontsize=14)
    plt.xlabel('Area(um)', fontsize=14)
    plt.ylabel('Fall_Delay(ns)', fontsize=14)
    for i,j,k in zip(area,rise_delay,name):
       
        plt.text(i,j,k.strip("sky130_fd_sc_hd__"))
    
    mplcursors.cursor(hover=True)
   
    plt.show()
    





def plot_area_vs_fall_delay(func,ob1):
    name=[]
    area=[]
    fall_delay=[]

    for i in ob1.dic.keys():
        if ob1.dic[i]['function'] is not None:
         if func in ob1.dic[i]['function']:
             name.append(i)
             area.append(ob1.dic[i]['Area'])
             fall_delay.append(statistics.median(ob1.dic[i]['max delay col fall']))
        
    plt.plot(area, fall_delay, linestyle='dashed',c="red", marker='o')
    plt.title('Area vs Fall Delay', fontsize=14)
    plt.xlabel('Area(um)', fontsize=14)
    plt.ylabel('Fall_Delay(ns)', fontsize=14)
    for i,j,k in zip(area,fall_delay,name):
       
        plt.text(i,j,k.strip("sky130_fd_sc_hd__"))
    
    mplcursors.cursor(hover=True)
   
    plt.show()

def plot_leakage_vs_fall_delay(func,ob1):
    name=[]
    leakage=[]
    fall_delay=[]

    for i in ob1.dic.keys():
        if ob1.dic[i]['function'] is not None:
            if func in ob1.dic[i]['function']:
                name.append(i)
                leakage.append(ob1.dic[i]['leakage'])
                fall_delay.append(statistics.median(ob1.dic[i]['max delay col fall']))
        
    plt.plot(leakage, fall_delay, linestyle='dashed',c="red", marker='o')
    plt.title('Leakage vs Fall Delay', fontsize=14)
    plt.xlabel('leakage(nW)', fontsize=14)
    plt.ylabel('Fall_Delay(ns)', fontsize=14)
    for i,j,k in zip(leakage,fall_delay,name):
       
        plt.text(i,j,k.strip("sky130_fd_sc_hd__"))
    
    mplcursors.cursor(hover=True)
   
    plt.show()

    
def plot_leakage_vs_rise_delay(func,ob1):  
    name=[]
    leakage=[]
    rise_delay=[]

    for i in ob1.dic.keys():
        if ob1.dic[i]['function'] is not None:
            if func in ob1.dic[i]['function']:
                name.append(i)
                leakage.append(ob1.dic[i]['leakage'])
                rise_delay.append(statistics.median(ob1.dic[i]['max delay col rise']))
        
    plt.plot(leakage, rise_delay, linestyle='dashed',c="red", marker='o')
    plt.title('Leakage vs Rise Delay', fontsize=14)
    plt.xlabel('leakage(nW)', fontsize=14)
    plt.ylabel('Rise_Delay(ns)', fontsize=14)
    for i,j,k in zip(leakage,rise_delay,name):
       
        plt.text(i,j,k.strip("sky130_fd_sc_hd__"))
    
    mplcursors.cursor(hover=True)
   
    plt.show()



def delay_vs_cap_trans_graph(name_of_cell,cap_fall,cap_rise,del_fall,del_rise,label1,label2):
    
        f = plt.figure()
        plt.title(name_of_cell)
        f.set_figwidth(6)
        f.set_figheight(6)
        plt.plot(cap_fall,del_fall,color='blue',label='Cell Fall',marker='o',linestyle='dashed',markersize=12)
        plt.plot(cap_rise,del_rise,color='green',label='Cell Rise',marker='o',linestyle='dashed',markersize=12)
        plt.xlabel(label1)
        plt.ylabel(label2)
        mplcursors.cursor(hover=True)
        
        plt.legend(['CELL FALL','CELL RISE'],loc='upper left')
        plt.show()