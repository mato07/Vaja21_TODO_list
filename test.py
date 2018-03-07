datum1="01.05.2017"
datum2="03.04.1990"
datum3="03.04.2010"

datumi=[datum1,datum2,datum3]

nova=[]
for item in datumi:
    item2 = item.split(".")
    item3 = item2[2]+item2[1]+item2[0]
    nova.append(item3)
    najblizji = min(nova)
    indeksmin = nova.index(najblizji)
print najblizji
print indeksmin

