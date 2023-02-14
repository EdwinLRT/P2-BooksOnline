import csv

# 1. Ouvrir un fichier en mode écriture en Python
f = open('nombres.csv', 'w')

# 2. Créez un objet CSV writer
writer = csv.writer(f)

# 3. Ecrire des données dans un fichier CSV
data = ["un", "deux", "trois", "quatre"]
writer.writerow(data)

# 4. Fermez un fichier ouvert avec open en Python
f.close()