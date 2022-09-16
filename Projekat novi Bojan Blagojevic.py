from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from fiona.crs import from_epsg
import matplotlib.pyplot as plt

#ucitavanje fajla za rad
file = "C:/Users/Bojan/Desktop/Fakultet master GIS/Pajton/Opstine SRB projekat.shp"
opstine= gpd.read_file(file)
print(opstine)

#provera tipa fajla koji smo uneli
type(opstine)

#provera da li je nas fajl u koordinatnom sistemu MGI 1901/Balkans zona 7 EPSG:6316
opstine.crs
print(opstine.crs)

#brisanje nepotrebne kolone Opstine_lat iz atributne tabele
brisanje = gpd.GeoDataFrame(opstine)
del opstine['Optine_lat']
print(opstine)

#dodavanje kolone Povrsina u okvir atributne tabele i smestanje podataka o povrsinama svake opstine u Srbiji izrazene u kilometrima kvadratnih
opstine['Povrsina'] = opstine.area/1000000
print(opstine)

#dodavanje kolone Gustina naseljenosti u okvir atributne tabele i smestanje podataka o gustini naseljenosti
#svake opstine u Srbiji su izrazene po broju stanovnika na kvadratnom kilometru
opstine['Gustina naseljenosti']=opstine['br_st2002']/opstine['Povrsina']
print(opstine)

#dodavanje kolone Tip gustine koja ce biti prazna a u koju cemo kasnije smestiti informaciju da li je ona niska, srednja ili visoka
opstine['Tip gustine'] = None
print(opstine)

# odredjivanje Tipa gustinenaseljenosti na osnovu skale 0-25 stanovnika po kilometru kvadratnom - Niska, 
#25-50 srednje niska, 
#50-75 - srednja, 
#75-100 srednje visoka i 
#100-200 visoka

df = gpd.GeoDataFrame(opstine)
df.loc[df['Gustina naseljenosti'] < 25, 'Tip gustine'] = 'Niska'
df.loc[df['Gustina naseljenosti'] > 25, 'Tip gustine'] = 'Srednje niska'
df.loc[df['Gustina naseljenosti'] > 50, 'Tip gustine'] = 'Srednja'
df.loc[df['Gustina naseljenosti'] > 75, 'Tip gustine'] = 'Srednje visoka'
df.loc[df['Gustina naseljenosti'] > 100, 'Tip gustine'] = 'Visoka' 

print(df)
print(opstine)

#plotovanje mape sa simbologijom koja koristi vrednosti kolone Tip gustine
opstine.plot(column='Tip gustine', categorical=True, legend=True, figsize=(20,20),cmap="OrRd");
plt.title('Opstine Srbije prema tipu gustine naseljenosti\nPopis 2002.godine')
plt.show()

#snimanje dobijenog fajla na nas racunar
izlaz= "C:/Users/Bojan/Desktop/Fakultet master GIS/Pajton/Mapa gustine naseljenosti.shp"
opstine.to_file(izlaz)
