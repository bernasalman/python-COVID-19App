"""COVID-19 UYGULAMASI"""
python -m pip install requests

import requests           
import datetime    

from tkinter import *
from tkinter.ttk import *

#import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg   #grafiği hareket ettirip, yakınlaştırma izinleri
from matplotlib import style        # grafik stili
style.use("Solarize_Light2")
from pandas import DataFrame

def main():
    vakalar = []
    tarihler = []
    ölümler= []
    ülkeler = []
    sıra = 1

    pencere= Tk()
    pencere.title("COVID-19 UYGULAMASI(1181602036-Berna Salman)")
    pencere.geometry("{0}x{1}+0+0".format(pencere.winfo_screenwidth(),pencere.winfo_screenheight()))

    #covid-19 verilerini belli bir konumda alıp indrime
    url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx"
    file = requests.get(url, allow_redirects=True)
    open('D:/Dersler/Final Projesi/Python Final/file'
         '/COVID-19-geographic-disbtribution-worldwide.xlsx', 'wb').write(file.content)
    kitap = xlrd.open_workbook('file/COVID-19-geographic-disbtribution-worldwide.xlsx')
    sayfa = kitap.sheet_by_index(0)
    ülkeler = ülkeler_listesi_al(sıra, sayfa, ülkeler)

    #ülke seçimi
    dekişken = StringVar(pencere)
    değişken.set("Ülkeler")  
    drop_down_menu = OptionMenu(pencere, değişken, *ülkeler)
    drop_down_menu.pack()

    def tamam():
        seçim = değişken.get()
        widgetler = pencere.winfo_children()
        for i in witgetler:
            i.pack_forget()
        pencere.quit()
        return seçim
    tamam_button = Button(pencere, text="TAMAM", command=tamam)
    tamam_button.pack()
    msg3 = Label(pencere, justify=CENTER, text="Grafikleri görmek için ülke seçin ve 'TAMAM' a basın." , font="Arial 11 italic")
    msg3.pack()
    pencere.mainloop()

    ülke = tamam()
    while sayfa.cell(sıra, 6).value != xlrd.empty_cell.value:
        if ülke == sayfa.cell(sıra, 6).value:
            break
        sıra += 1

    #tarihlerdeki vakalar
    while sayfa.cell(sıra, 6).value == ülke:
        ölümler = ölümler_al(sıra, ölümler, sayfa)
        vakalar = vakalar_al(sıra, vakalar, sayfa)
        tarihler =tarih_al(sıra, tarihler, sayfa)
        sıra+= 1
    ölümler.reverse()
    vakalar.reverse()
    tarihler.reverse()
    
    tarihler = [datetime.datetime.strptime(t, "%m/%d/%Y").tarih() for t in tarihler]

    # grafikler için pencere
    grafikler = pencere

    # vaka ve tarihler için çerçeve 
    vakalar_corresponding_tarihler = {"Tarih": tarihler, "Vakalar": vakalar}
    vakalar_tarihler_frame = Frame(vakalar_corresponding_tarihler, columns=["Tarih", "Vakalar"])

    # matplot grafiğiyle vakalar ve tarih çerçevesi
    vakalar_figure = plt.Figure(figsize=(6, 6), dpi=100)
    vakalar_axis = vakalar_figure.add_subplot(111)
    vakalar_graph = FigureGrafiklerTkAgg(vakalar_figure, grafikler)
    vakalar_graph.get_tk_widget().pack(side=LEFT, fill=BOTH)
    vakalar_tarihler_frame = vakalar_tarihler_frame[["Tarih", "Vakalar"]].groupby("Tarih").sum()
    vakalar_tarihler_frame.plot(kind='line', legend=True, ax=vakalar_axis, color='y', fontsize=7)
    vakalar_axis.set_title(ülke+"'nin COVID-19 vakaları")

    # ölümler ve tarihler için çerçeve
    ölümler_corresponding_tarihler = {"Tarih": tarihler, "Ölümler": ölümler}
    ölümler_tarihler_frame = Frame(ölümler_corresponding_tarihler, columns=["Tarih", "Ölümler"])

    #matplot grafiğinde ölümler ve tarih çerçevesi
    ölümler_figure = plt.Figure(figsize=(8, 6), dpi=100)
    ölümler_axis = ölümler_figure.add_subplot(111)
    ölümler_graph = FigureGrafiklerTkAgg(ölümler_figure,grafikler)
    ölümler_graph.get_tk_widget().pack(side=RIGHT, fill=BOTH)
    ölümler_tarihler_frame = ölümler_dates_frame[["Tarih", "Ölümler"]].groupby("Tarih").sum()
    ölümler_tarihler_frame.plot(kind='line', legend=True, ax=ölümler_axis, color='r', fontsize=7)
    ölümler_axis.set_title(ülke + "'nin COVID-19 Ölümleri")
    grafikler.mainloop()

def ülkeler_listesi_al(sıra, sayfa, ülkeler):
    ülke =sayfa.cell(sıra, 6).value
    ülkeler.append(ülke)
    for ssıra in range(1, sayfa.sıraa):
        if ülke != sayfa.cell(ssıra, 6).value:
            ülke = sayfa.cell(ssıra, 6).value
            ülkeler.append(ülke)
    return ülkeler

def tarih_al(sıra, tarihler, sayfa):
    gün = int(worksheet.cell(sıra, 1).value)
    ay = int(worksheet.cell(sıra, 2).value)
    yıl = int(worksheet.cell(sıra, 3).value)
    tarihler.append(str(ay)+"/"+str(gün)+"/"+str(yıl))
    return tarihler

def vaka_al(sıra, vakalar, sayfa):
    vakalar_cell = worksheet.cell(sıra, 4).value
    vakalar.append(vakalar_cell)
    return vakalar


def ölümler_al(sıra, ölümler, sayfa):
    ölümler_cell = sayfa.cell(sıra, 5).value
    ölümler.append(ölümler_cell)
    return ölümler


if __name__ == '__main__':
    main()

