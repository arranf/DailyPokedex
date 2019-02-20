rm function.zip
zip -r9 function.zip ./v-env/lib/python3.6/site-packages
zip -g function.zip function.py pokedex.csv