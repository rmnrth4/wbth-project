from bs4 import BeautifulSoup
import requests

side = "https://scrapeme.live/shop/"
html_text = requests.get(side).text
soup = BeautifulSoup(html_text, "lxml")

products = soup.find("ul", class_="products columns-4")
pokemons = products.find_all(
    "li",
    class_=lambda value: value and value.startswith("post-"),
)

for pokemon in pokemons:
    pokemon_name = pokemon.find("h2", class_="woocommerce-loop-product__title").text
    pokemon_price = pokemon.find("span", class_="woocommerce-Price-amount amount").text
    # print(pokemon_name, pokemon_price)
    print(
        f"""
    Pokemon Name: {pokemon_name}
    Price: {pokemon_price}"""
    )
