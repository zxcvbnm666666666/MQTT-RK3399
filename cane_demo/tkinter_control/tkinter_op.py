
import time
import serial
import binascii
import pynmea2
import threading
import datetime
import time
import tkinter as tk
from multiprocessing import Process, Manager, Pool, Queue
def tk_fun(oil, flow, rotate, angle, lon):
    
    root = tk.Tk()
    root.title('甘蔗信息管理系统 v1.0')
    root.geometry('600x400')

    menubar = tk.Menu(root)
    menubar.add_command(label="主界面")
    menubar.add_command(label="子界面")
    root.config(menu=menubar)

    label = tk.Label(root, text="根切刀辊").place(x=20, y=60, anchor='nw')
    label = tk.Label(root, text="切断刀辊").place(x=20, y=100, anchor='nw')
    label = tk.Label(root, text="二级输送").place(x=20, y=140, anchor='nw')
    label = tk.Label(root, text="排杂风机").place(x=20, y=180, anchor='nw')
    label = tk.Label(root, text="车辆信息").place(x=20, y=260, anchor='nw')

    label = tk.Label(root, text="进油压(bar)").place(x=100, y=20, anchor='nw')
    label = tk.Label(root, text="出油压(bar)").place(x=200, y=20, anchor='nw')
    label = tk.Label(root, text="流量(L/min)").place(x=300, y=20, anchor='nw')
    label = tk.Label(root, text="转速(r/min)").place(x=400, y=20, anchor='nw')

    label = tk.Label(root, text="角度x(度))").place(x=100, y=230, anchor='nw')
    label = tk.Label(root, text="角度y(度)").place(x=200, y=230, anchor='nw')
    label = tk.Label(root, text="角度z(度)").place(x=300, y=230, anchor='nw')
    label = tk.Label(root, text="车速(m/min)").place(x=400, y=230, anchor='nw')

    gen_jin = tk.StringVar()              #根切器的进油
    gen_jin.set('100')
    qie_jin = tk.StringVar()              #切断
    qie_jin.set('120')
    er_jin = tk.StringVar()               #二级输送
    er_jin.set('140')
    pai_jin = tk.StringVar()              #排杂风机
    pai_jin.set('160')


    gen_chu = tk.StringVar()
    gen_chu.set('10')
    qie_chu = tk.StringVar()
    qie_chu.set('5')
    er_chu = tk.StringVar()
    er_chu.set('4')
    pai_chu = tk.StringVar()
    pai_chu.set('3')

    gen_l = tk.StringVar()
    gen_l.set('100')
    qie_l = tk.StringVar()
    qie_l.set('80')
    er_l = tk.StringVar()
    er_l.set('90')
    pai_l = tk.StringVar()
    pai_l.set('120')


    gen_r = tk.StringVar()
    gen_r.set('500')
    qie_r = tk.StringVar()
    qie_r.set('600')
    er_r = tk.StringVar()
    er_r.set('500')
    pai_r = tk.StringVar()
    pai_r.set('1000')

    jiao_x = tk.StringVar()
    jiao_x.set('5')
    jiao_y = tk.StringVar()
    jiao_y.set('50')
    jiao_z = tk.StringVar()
    jiao_z.set('40')
    che_su = tk.StringVar()
    che_su.set('40')


    #进油压
    label_gen_jin = tk.Label(root, textvariable=gen_jin).place(x=100, y=60, anchor='nw')
    label_qie_jin = tk.Label(root, textvariable=qie_jin).place(x=100, y=100, anchor='nw')
    label_er_jin = tk.Label(root, textvariable=er_jin).place(x=100, y=140, anchor='nw')
    label_pai_jin = tk.Label(root, textvariable=pai_jin).place(x=100, y=180, anchor='nw')

    #出油压
    label_gen_chu = tk.Label(root, textvariable=gen_chu).place(x=200, y=60, anchor='nw')
    label_qie_chu = tk.Label(root, textvariable=qie_chu).place(x=200, y=100, anchor='nw')
    label_er_chu = tk.Label(root, textvariable=er_chu).place(x=200, y=140, anchor='nw')
    label_pai_chu = tk.Label(root, textvariable=pai_chu).place(x=200, y=180, anchor='nw')

    #流量
    label_gen_l = tk.Label(root, textvariable=gen_l).place(x=300, y=60, anchor='nw')
    label_qie_l = tk.Label(root, textvariable=qie_l).place(x=300, y=100, anchor='nw')
    label_er_l = tk.Label(root, textvariable=er_l).place(x=300, y=140, anchor='nw')
    label_pai_l = tk.Label(root, textvariable=pai_l).place(x=300, y=180, anchor='nw')

    #转速
    label_gen_r = tk.Label(root, textvariable=gen_r).place(x=400, y=60, anchor='nw')
    label_qie_r = tk.Label(root, textvariable=qie_r).place(x=400, y=100, anchor='nw')
    label_er_r = tk.Label(root, textvariable=er_r).place(x=400, y=140, anchor='nw')
    label_pai_r = tk.Label(root, textvariable=pai_r).place(x=400, y=180, anchor='nw')
    
    label_x = tk.Label(root, textvariable=jiao_x).place(x=100, y=260, anchor='nw')
    label_y = tk.Label(root, textvariable=jiao_y).place(x=200, y=260, anchor='nw')
    label_z = tk.Label(root, textvariable=jiao_z).place(x=300, y=260, anchor='nw')
    label_chesu = tk.Label(root, textvariable=che_su).place(x=400, y=260, anchor='nw')

    def update_label():
        if not oil.empty():
            OIL = oil.get()
            gen_jin.set(round(OIL[0],2))
            gen_chu.set(round(OIL[1],2))
            qie_jin.set(round(OIL[2],2))
            qie_chu.set(round(OIL[3],2))
            er_jin.set(round(OIL[4],2))
            er_chu.set(round(OIL[5],2))
            pai_jin.set(round(OIL[6],2))
            pai_chu.set(round(OIL[7],2))
        if not flow.empty():
            FLOW = flow.get()
            gen_l.set(round(FLOW[0],2))
            qie_l.set(round(FLOW[1],2))
            er_l.set(round(FLOW[2],2))
            pai_l.set(round(FLOW[3],2))

        if not rotate.empty():
            ROTATE = rotate.get()
            gen_r.set(round(ROTATE[0],2))
            qie_r.set(round(ROTATE[1],2))
            er_r.set(round(ROTATE[2],2))
            pai_r.set(round(ROTATE[3],2))
            che_su.set(round(ROTATE[4],2))

        if not angle.empty():
            ANGLE= angle.get()
            jiao_x.set(round(ANGLE[0],2))
            jiao_y.set(round(ANGLE[1],2))
            jiao_z.set(round(ANGLE[2],2))


        root.after(100, update_label)

    # 启动刷新函数
    update_label()

    


    root.update()
    root.mainloop()

def main():
    oil = Queue()                #代表油压的队列
    flow = Queue()               #流量的队列
    rotate = Queue()             #转速的队列
    angle = Queue()              #角度的队列
    lon = Queue() 
    

    #p1 = Process(target=threading_control, args=(q1, q2))
   
    p2 = Process(target=tk_fun, args=(oil, flow, rotate, angle, lon))
    p2.start()
    p2.join()
    print('123')
if __name__ == '__main__':
     
     main()

