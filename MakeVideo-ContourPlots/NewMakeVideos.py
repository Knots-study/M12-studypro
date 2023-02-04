import os
import requests
import pprint
import tkinter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(tkinter.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=680, height=280)
        self.root = root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()
    
    def create_widgets(self):
        #テキストボックス
        self.text_box = tkinter.Entry(self)
        self.text_box['width'] = 10
        self.text_box.pack()

        #実行ボタン
        submit_btn = tkinter.Button(self)
        submit_btn['text'] = '実行'
        submit_btn['command'] = self.display_graph
        submit_btn.pack()

        #グラフの描画
        plt.rcParams['font.size'] = 7
        self.fig, self.ax = plt.subplots(figsize=(12,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

    def display_graph(self):
        symbol = self.text_box.get()
        api_key = os.environ['ALPHA_VANTAGE_KEY']
        url = 'https://www.alphavantage.co/query?'\
            f'function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}'
        data= requests.get(url).json()

        monthly_data = dict(reversed(data['Monthly Time Series'].items()))
        monthly_list = monthly_data.keys()
        close_list = [float(x['4. close']) for x in monthly_data.values()]

        self.ax.clear()
        self.ax.plot(monthly_list, close_list)
        self.ax.xaxis.set_major_locator(mdates.DayLocator(interval=28))
        self.ax.grid()
        self.canvas.draw()

def main():
    root = tkinter.Tk()
    root.title("てすとだよ")
    root.geometry('700x300')
    app = Application(root=root)
    app.mainloop()

if __name__ == '__main__':
    main()