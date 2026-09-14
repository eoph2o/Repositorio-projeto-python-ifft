from pathlib import Path
import pandas as pd 
from io import StringIO
import numpy as np
import scipy as sp
from scipy.fft import ifftshift, ifft

import matplotlib.pyplot as plt


class ArquivoController:


    def __init__(self): 

        self.arquivos = {}
        self.df = pd.DataFrame()
        
    def manejaArquivo(self, caminho):   

        pasta = Path(caminho)

        self.arquivos = {
            p.name: str(p)
            for p in pasta.glob("*.s2p")
        }

        #print(f'Dicionário - arquivos: {self.arquivos}')
        return list(self.arquivos.keys())
    
    def pegarData(self, nomeArquivo): 
        self.caminhoPlot  = self.arquivos[nomeArquivo]
        with open(self.caminhoPlot, 'r') as arquivo:

            linhas = [
            linha for linha in arquivo
            if not linha.startswith('!')
            and not linha.startswith('#')
        ]
        
        self.df = pd.read_csv(StringIO(''.join(linhas)), sep=r'\s+', header=None)
        self.df.columns = ["frequencia", "modulo", "fase"]

        #Funções para desenvolvimento da transformada de fourier
    def get_Fourier(self):     
                freq, amplitude, fase = self.VetorNumPy(
                    self.get_freq(), self.get_amplitude(), self.get_fase())
                
                espectroComplex = self.espectroComplexo(amplitude, fase) #espectro complexo, criando A*e^jw
        
                resulIFFT = ifft(espectroComplex) * 2 * len(espectroComplex)
        
                self.real = np.real(resulIFFT) 
                self.nAmostras  = len(resulIFFT)         
                self.tempo= self.EixoTempo(freq, self.nAmostras)
        
                return self.real, self.tempo 

    def get_freq(self):
        return self.df["frequencia"] 
     
    def get_amplitude(self):
        
        return 10**(self.df["modulo"] /20)  #transforma amplitude de db para escala linear, é tensão portanto "/20"
    
    def get_fase(self):
        
        return np.deg2rad(self.df["fase"]) #fase em radianos.

    def VetorNumPy (self, freq, amplitude, fase):
        self.npfreq = np.array( freq, dtype='float')
        self.npamplitude = np.array( amplitude, dtype='float')
        self.npfase = np.array( fase, dtype='float')

        return self.npfreq, self.npamplitude, self.npfase 

    def espectroComplexo(self, amplitude, fase): 
         #espectro complexo, criando A*e^jw
            self.espectroComplex = amplitude*np.exp(1j*fase) 
            return self.espectroComplex

    def EixoTempo (self, freq, nAmostras): 
        #eixo temporal        
        # espaço entre frequencias, por serem igualmente espeaçadas será um valore constante 
                self.difFreq = freq[1] - freq[0]
                self.dt = 1/(nAmostras*self.difFreq)  
                self.tempo = np.arange(nAmostras)*self.dt

                return self.tempo
    
    def PlotPopUp (self):
         
        real, tempo = self.get_Fourier()
        freq = self.npfreq
        amplitude = self.npamplitude
        fase = self.npfase
   

        # Cria uma janela com 3 gráficos
        fig, axs = plt.subplots(3, 1, figsize=(10, 8))

        # Primeiro gráfico
        axs[0].plot(freq, amplitude)
        axs[0].set_title("Amplitude x Freq", loc = 'left', pad=8)
        axs[0].set_xlabel("frequência")
        axs[0].set_ylabel("Amplitude")
        axs[0].grid(True)

        # Segundo gráfico
        axs[1].plot(freq, fase)
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
          

   