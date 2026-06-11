# API Explorer: PokéAPI

## Objective
Practice making HTTP requests, parsing JSON responses, and writing results to a file.

## Setup
Create a new file called `api_explorer.py`.

You will need the `requests` library. Install it with:
```
pip install requests
```

## The API
The PokéAPI is a free, open REST API with no authentication required.

Base URL: `https://pokeapi.co/api/v2/`

To get data about a Pokémon: `https://pokeapi.co/api/v2/pokemon/{name or id}`

For example: `https://pokeapi.co/api/v2/pokemon/pikachu`

## Starter Code
Paste this into your file. The API request is done for you — your job is to parse the response and write the output.

```python
import requests

pokemon_name = input("Enter a Pokémon name: ").lower()
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # data is now a dictionary with all the Pokémon's info
    # YOUR CODE HERE: extract the fields listed below and write them to {pokemon_name}.txt
else:
    print(f"Error: could not find '{pokemon_name}' (status code {response.status_code})")
```

## Instructions
Using the `data` dictionary from the starter code, extract the following fields and write them to a file named after the Pokémon (e.g., `pikachu.txt`):
   - Name
   - ID
   - Height
   - Weight
   - Types (a Pokémon can have more than one)
   - Base stats (hp, attack, defense, special-attack, special-defense, speed)

## Things to Consider
- What happens if the user enters a Pokémon that doesn't exist?
- What HTTP status code comes back in that case?
- How should your script handle that?
- What if a file already exists for that Pokémon? Should it overwrite, skip, or ask the user?

## Example Output (`pikachu.txt`)
```
Name: pikachu
ID: 25
Height: 4
Weight: 60
Types: electric
Stats:
  hp: 35
  attack: 55
  defense: 40
  special-attack: 50
  special-defense: 50
  speed: 90
```