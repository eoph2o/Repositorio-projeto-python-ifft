from pathlib import Path
import pandas as pd 
from io import StringIO
import numpy as np
from scipy.fft import ifft

import matplotlib.pyplot as plt


class ArquivoController:


    def __init__(self, nomeArquivo, caminho): 

        self.df = pd.DataFrame()
        self.caminho = caminho 
        self.nomeArquivo = nomeArquivo
        
    def pegarData(self): 
        with open(self.caminho, 'r') as arquivo:

            linhas = [
            linha for linha in arquivo
            if not linha.startswith('!')
            and not linha.startswith('#')
        ]
        
        self.df = pd.read_csv(StringIO(''.join(linhas)), sep=r'\s+', header=None)
        self.df.columns = ["frequencia", "modulo", "fase"]

        #Funções para desenvolvimento da transformada de fourier

    def get_freq(self):
        return np.array (self.df["frequencia"], dtype='float') 
    
    def get_amplitude(self):
        
        return np.array(10**(self.df["modulo"] /20), dtype='float' ) #transforma amplitude de db para escala linear, é tensão portanto "/20"
    
    def get_fase(self):
        
        return np.array(np.deg2rad(self.df["fase"]), dtype='float') #fase em radianos.

    def PlotPopUp (self):
         
        real, tempo = self.get_Fourier()   

        # Cria uma janela com 3 gráficos
        fig, axs = plt.subplots(3, 1, figsize=(10, 8))

        # Primeiro gráfico
        axs[0].plot(self.freq, self.amplitude)
        axs[0].set_title("Amplitude x Freq", loc = 'left', pad=8)
        axs[0].set_xlabel("frequência")
        axs[0].set_ylabel("Amplitude")
        axs[0].grid(True)

        # Segundo gráfico
        axs[1].plot(self.freq, self.fase)
        axs[1].set_title("fase X Freq",loc = 'left', pad=8)
        axs[1].set_xlabel("frequancia")
        axs[1].set_ylabel("fase")
        axs[1].grid(True)

        # Terceiro gráfico
        axs[2].plot(tempo, real)
        axs[2].set_title("IFFT",loc = 'left', pad=8)
        axs[2].set_xlabel("Tempo")
        axs[2].set_ylabel("Real")
        axs[2].grid(True)

        # Ajusta automaticamente os espaços
        plt.tight_layout()

        # Mostra a janela
        plt.show()

    def leituraAll(self): 
        for atual in self.arquivos:
            self.pegarData(atual) 
            self.PlotPopUp()
            self.df = self.df.iloc[0:0]        

                  
    def get_Fourier(self):     
        self.freq = self.get_freq()
        self.amplitude = self.get_amplitude()
        self.fase = self.get_fase()
        espectroComplex = self.espectroComplexo(self.amplitude,self.fase) #espectro complexo, criando A*e^jw
            
        resulIFFT = ifft(espectroComplex) * 2 * len(espectroComplex)
            
        real = np.real(resulIFFT) 
        nAmostras  = len(resulIFFT)         
        tempo = self.EixoTempo(self.freq, nAmostras)
            
        return real, tempo 
    
    def espectroComplexo(self, amplitude, fase): 
         #espectro complexo, criando A*e^jw
            espectroComplex = amplitude*np.exp(1j*fase) 
            return espectroComplex

    def EixoTempo (self, freq, nAmostras): 
        #eixo temporal        
        # espaço entre frequencias, por serem igualmente espeaçadas será um valore constante 
                difFreq = freq[1] - freq[0]
                dt = 1/(nAmostras*difFreq)  
                tempo = np.arange(nAmostras)*dt

                return tempo
    