import pandas as pd

pokemons = pd.read_csv("main.csv")

pokemonsDanos = pd.read_csv("serebii.csv")

novoDF = pd.merge(pokemons, pokemonsDanos, how='outer')

print(novoDF.tail())

novoDF.to_csv('novo.csv', index=False)
# print(novoDF.loc[novoDF['Ndex'] == '#047'])