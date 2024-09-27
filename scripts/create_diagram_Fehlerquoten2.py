import matplotlib.pyplot as plt
import pandas as pd

fig, ax = plt.subplots()
ax.set_xlabel('Missionen (IDs)')
ax.set_ylabel('Fehlerquote in %')
#ax.set_title('Entwicklung der Fehlerquoten 2018 - 2023')
ax.tick_params(axis='x', labelrotation=75, labelsize=8)

fehlerquoten = [8.4, 6.3, 4.2, 7.2, 2.9, 4.3, 4.1, 1.8, 2.2, 3.0, 3.5, 1.7]
fehlerquoten_pot = [5.6, 5.6, 3.8, 6.1, 2.9, 3.8, 3.0, 1.8, 1.3, 2.4, 3.5, 1.5]
mission = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
FQ_potenziell = pd.Series(fehlerquoten_pot, index=mission)
FQ_aktuell = pd.Series(fehlerquoten, index=mission)

plt.plot(FQ_aktuell, color='#76B900', label= 'Fehlerquoten aus Untersuchung')
plt.plot(FQ_potenziell, color='#FF5F00', linestyle='dashed', label= 'potenzielle Fehlerquoten')

plt.legend()
plt.show()
