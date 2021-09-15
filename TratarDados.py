import pandas as pd

pokemons = pd.read_csv("main.csv")

pokemonsDanos = pd.read_csv("serebii.csv")

pokemons[['Ndex','pokemon_name']] = pokemons[['Ndex','pokemon_name']].astype('object')
pokemonsDanos[['Ndex','pokemon_name']] = pokemonsDanos[['Ndex','pokemon_name']].astype('object')

novoDF = pd.merge(pokemons, pokemonsDanos, how='outer')

print(novoDF.tail())

novoDF.to_csv('novo.csv', index=False)
# print(novoDF.loc[novoDF['Ndex'] == '#047'])