from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class Principal(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.place(relx=0.18, y=0, relwidth=0.82, relheight=1)

        # Criação da figura
        self.fig = Figure(figsize=(6, 5), dpi=100)

        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312)
        self.ax3 = self.fig.add_subplot(313)
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        
        # Exibe o canvas
        self.canvas.get_tk_widget().pack(expand=True, fill="both")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    def plotar(self, amplitude, fase, freq, real, tempo ):

        # Limpa os gráficos antigos
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        self.ax1.plot(freq, amplitude)

        self.ax1.set_title("Amplitude", size= 11, loc = 'left', pad=8)
        self.ax1.set_xlabel("Frequência", size= 9, labelpad=5)
        self.ax1.set_ylabel("dB", size= 9, labelpad=5)
        self.ax1.grid(True)

        
        self.ax2.plot(freq, fase)

        self.ax2.set_title("Fase", size= 11, loc = 'left', pad=8)
        self.ax2.set_xlabel("Frequência", size= 9, labelpad=5)
        self.ax2.set_ylabel("Radiano", size= 9, labelpad=5)
        self.ax2.grid(True)

        self.ax3.plot(tempo, real )

        self.ax3.set_title("Transformada Inversa de Fourier", size= 11, loc = 'left', pad=8)
        self.ax3.set_xlabel("Tempo", size= 9, labelpad=5)
        self.ax3.set_ylabel("Amplitude", size= 9, labelpad=5)
        self.ax3.grid(True)

        self.fig.tight_layout(pad=0.5)
        self.canvas.draw()
       