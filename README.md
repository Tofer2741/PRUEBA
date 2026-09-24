# PRUEBA
Prueba

## Ruleta de premios

Juego de ruleta de casino para la terminal (Python 3.9+, sin dependencias).

```bash
python3 ruleta.py                    # jugar con 100 fichas
python3 ruleta.py --fichas 50        # elegir fichas iniciales
python3 ruleta.py --probabilidades   # ver premios y probabilidades
python3 ruleta.py --semilla 42       # resultados reproducibles
```

Cada giro cuesta 10 fichas. Pulsa Enter para girar, `p` para ver las
probabilidades y `q` para salir. Los premios y sus pesos se editan en la
lista `PREMIOS` de `ruleta.py`.
