# Load Nessesary Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create Window
window = tk.Tk()
window.geometry("1080x640")
window.wm_title("Trading - Forex")

# Create PanedWindow and Frames
pw = ttk.Panedwindow(window, orient=tk.HORIZONTAL)
pw.pack(fill=tk.BOTH, expand=True)

w2 = ttk.Panedwindow(pw, orient=tk.VERTICAL)

frame1 = ttk.Frame(pw, width=360, height=640, relief=tk.SUNKEN)
frame2 = ttk.Frame(pw, width=720, height=400, relief=tk.SUNKEN)
frame3 = ttk.Frame(pw, width=720, height=240, relief=tk.SUNKEN)

w2.add(frame2)
w2.add(frame3)

pw.add(w2)
pw.add(frame1)

# Fill Frame1 with TreeView and Button
item = ""
def callback(event):
    global item
    item = treeview.identify("item", event.x, event.y)


#treeview
treeview = ttk.Treeview(frame1)
treeview.grid(row=0, column=1, padx=25, pady=25)
treeview.insert("", "0", "Major", text="Major")
treeview.insert("Major", "1", "EUR/USD", text="EUR/USD")
treeview.insert("", "2", "Minor", text="Minor")
treeview.insert("Minor", "3", "EUR/GBR", text="EUR/GBR")
treeview.bind("<Button-1>", callback)

#button

def readNews(item):
    if item == "EUR/USD":
        news = pd.read_csv("data/news_EURUSD.txt")
    elif item == "EUR/GBR":
        news = pd.read_csv("data/news_EURGBR.txt")
    
    textbox.insert(tk.INSERT, news)
    

def openTrade():
    global data, future, data_close_array, future_array, line1, line2, line3, line4, canvas1, canvas2, canvas3, canvas4, ax1, ax2, ax3, ax4
    
    if item != "":
        
        if item=="EUR/USD":
            
            #Button Settings
            open_trading_btn.config(state="disabled")
            start_trading_btn.config(state="normal")
            
            #Read Data
            data = pd.read_csv("data/eurusd.csv")
            
            #Split Data
            future = data[-1000:]
            data = data[:len(data)-1000]
            data_close_array = data.close1.values
            future_array = list(future.close1.values)
            
            #Line
            fig1 = plt.Figure(figsize=(5,4), dpi = 100)
            ax1 = fig1.add_subplot(111)
            line1, = ax1.plot(range(len(data)), data.close1, color="blue")
            canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
            canvas1.draw()
            canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #Scatter
            fig2 = plt.Figure(figsize=(5,4), dpi=100)
            ax2 = fig2.add_subplot(111)
            line2 = ax2.scatter(range(len(data)), data.close1, color="blue", alpha=0.5, s=1)
            canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #Read News
            readNews(item)
    
        elif item =="EUR/GBR":
            
            #Button Settings
            open_trading_btn.config(state="disabled")
            start_trading_btn.config(state="normal")
            
            #Read Data
            data = pd.read_csv("data/eurgbr.csv")
            
            #Split Data
            future = data[-1000:]
            data = data[:len(data)-1000]
            data_close_array = data.close1.values
            future_array = list(future.close1.values)
            
            #Line
            fig3 = plt.Figure(figsize=(5,4), dpi = 100)
            ax3 = fig3.add_subplot(111)
            line3, = ax3.plot(range(len(data)), data.close1, color="blue")
            canvas3 = FigureCanvasTkAgg(fig3, master=tab1)
            canvas3.draw()
            canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #Scatter
            fig4 = plt.Figure(figsize=(5,4), dpi=100)
            ax4 = fig4.add_subplot(111)
            line4 = ax4.scatter(range(len(data)), data.close1, color="blue", alpha=0.5, s=1)
            canvas4 = FigureCanvasTkAgg(fig4, master=tab2)
            canvas4.draw()
            canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            #Read News
            readNews(item)
        
        else:
            messagebox.showinfo(title="Warning", message="Please Choose a Currency Pair")
    else:
        messagebox.showinfo(title="Warning", message="Please Choose a Currency Pair")

open_trading_btn = tk.Button(frame1, text="Open Trading", command=openTrade)
open_trading_btn.grid(row=2, column=1, padx=5, pady=5)

# Create Frame3 with Text Editor & Scroll Bar
textbox = tk.Text(frame3, width=70, height=10, wrap="word")
textbox.grid(row=0, column=0, padx=25, pady=25)
scroll = tk.Scrollbar(frame3, orient=tk.VERTICAL, command=textbox.yview)
scroll.grid(row=0, column=1, sticky=tk.N + tk.S, pady=10)
textbox.config(yscrollcommand=scroll.set)

# Create Frame2 with Tab, Radio Button, Button, Result(Label Frame), and Plot
#tabs
tabs = ttk.Notebook(frame2, width=540, height=300)
tabs.place(x=25, y=25)
tab1 = ttk.Frame(tabs, width=50, height=50)
tab2 = ttk.Frame(tabs, width=50, height=50)
tabs.add(tab1, text="Line")
tabs.add(tab2, text="Scatter", compound=tk.LEFT)

#label frame
label_frame = tk.LabelFrame(frame2, text="Result", width=100, height=100)
label_frame.place(x=580, y=40)
tk.Label(label_frame, text="Buy: ", bd=3).grid(row=0, column=0)
tk.Label(label_frame, text="Sell: ", bd=3).grid(row=1, column=0)

#buy and sell labels
buy_value = tk.Label(label_frame, text="1", bd=3)
buy_value.grid(row=0, column=1)

sell_value = tk.Label(label_frame, text="0", bd=3)
sell_value.grid(row=1, column=1)

#radiobutton
method = tk.StringVar()
tk.Radiobutton(frame2, text="m1: ", value="m1", variable=method).place(x=580, y=150)
tk.Radiobutton(frame2, text="m2: ", value="m2", variable=method).place(x=580, y=180)

#button
def moving_average(a, n=50):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n-1:]/n

def update():
    global data_close_array, ax1, ax2, ax3, ax4
    
    spread = 0.002
    buy_value.config(text=str((data_close_array[-1]-spread).round(5)))
    sell_value.config(text=str((data_close_array[-1]+spread).round(5)))
    
    window.after(300, update)
    data_close_array = np.append(data_close_array, future_array.pop(0))
    
    if method.get() == "m1":
        if item == "EUR/USD":
            # line
            ax1.set_xlim(0,len(data_close_array) + 10)
            line1.set_ydata(data_close_array)
            line1.set_xdata(range(len(data_close_array)))
            
            # scatter
            ax2.set_xlim(0,len(data_close_array) + 10)
            ax2.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
            
            # moving average
            n = 50
            mid_rolling = moving_average(data_close_array,n)
            ax1.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle = "--", color = "red")
            ax2.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle = "--", color = "red")
            
            canvas1.draw()
            canvas2.draw()
        
        elif item == "EUR/GBR":
            # line
            ax3.set_xlim(0,len(data_close_array) + 10)
            line3.set_ydata(data_close_array)
            line3.set_xdata(range(len(data_close_array)))
            
            # scatter
            ax4.set_xlim(0,len(data_close_array) + 10)
            ax4.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
            
            # moving average
            n = 50
            mid_rolling = moving_average(data_close_array,n)
            ax3.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle = "--", color = "red")
            ax4.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle = "--", color = "red")
            
            canvas3.draw()
            canvas4.draw()
            
    elif method.get() == "m2":
        if item == "EUR/USD":
            # line
            ax1.set_xlim(0,len(data_close_array) + 10)
            line1.set_ydata(data_close_array)
            line1.set_xdata(range(len(data_close_array)))
            
            # scatter
            ax2.set_xlim(0,len(data_close_array) + 10)
            ax2.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
            
            # moving average
            n = 200
            long_rolling = moving_average(data_close_array,n)
            ax1.plot(range(n-1,len(data_close_array)),long_rolling,linestyle = "--", color = "green")
            ax2.plot(range(n-1,len(data_close_array)),long_rolling,linestyle = "--", color = "green")
            
            canvas1.draw()
            canvas2.draw()
        
        elif item == "EUR/GBR":
            # line
            ax3.set_xlim(0,len(data_close_array) + 10)
            line3.set_ydata(data_close_array)
            line3.set_xdata(range(len(data_close_array)))
            
            # scatter
            ax4.set_xlim(0,len(data_close_array) + 10)
            ax4.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
            
            # moving average
            n = 200
            long_rolling = moving_average(data_close_array,n)
            ax3.plot(range(n-1,len(data_close_array)),long_rolling,linestyle = "--", color = "green")
            ax4.plot(range(n-1,len(data_close_array)),long_rolling,linestyle = "--", color = "green")
            
            canvas3.draw()
            canvas4.draw()
        else:
            if item == "EUR/USD":
                # line
                ax1.set_xlim(0,len(data_close_array) + 10)
                line1.set_ydata(data_close_array)
                line1.set_xdata(range(len(data_close_array)))
                
                # scatter
                ax2.set_xlim(0,len(data_close_array) + 10)
                ax2.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
                
                canvas1.draw()
                canvas2.draw()
            elif item == "EUR/GBR":
                # line
                ax3.set_xlim(0,len(data_close_array) + 10)
                line3.set_ydata(data_close_array)
                line3.set_xdata(range(len(data_close_array)))
                
                # scatter
                ax4.set_xlim(0,len(data_close_array) + 10)
                ax4.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
                
                canvas3.draw()
                canvas4.draw()
            
            

def startTrading():
    window.after(0, update)

start_trading_btn = tk.Button(frame2, text="Start Trading", command=startTrading)
start_trading_btn.place(x=580, y= 285)
start_trading_btn.config(state="disabled")



window.mainloop()