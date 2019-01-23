# -*- coding: utf-8 -*-
import Tkinter as tk
import DrawBox as drbx #DrawBox.py 

window=tk.Tk()
window.title('行李放置')
window.geometry('200x60') #視窗大小
#
def run_pack(): #執行DrawBox.py 中的 run_plot
        drbx.run_plot()

# def run_optpack(): #執行DrawBox.py 中的 run_plot
#         drbx.run_optplot()

b = tk.Button(window, text='車箱行李放置', width=20,
              height=2, command=run_pack)
b.place(x=20, y=10, anchor='nw') #Button position

# b2 = tk.Button(window, text='最徍車箱行李放置', width=20,
#               height=2, command=run_optpack)
# b2.place(x=20, y=60, anchor='nw')
#
window.mainloop()