import matplotlib.pyplot as plt
import pandas as pd

fig, ax = plt.subplots()
ax.set_xlabel('Missionen (IDs)')
ax.set_ylabel('Fehlerquote in %')
ax.set_title('Entwicklung der Fehlerquoten')
ax.tick_params(axis='x', labelrotation=75, labelsize=8)


fehlerquote = [8.4, 6.3, 4.2, 7.2, 2.9, 4.3, 4.1, 1.8, 2.2, 3.0, 3.5, 1.7]
mission = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
S = pd.Series(fehlerquote, index=mission)


plt.plot(S, color='#76B900')  # notwendig ab Pandas-Version 0.23.4
#S.plot()    # funktioniert bis 0.23.4 
plt.show()

