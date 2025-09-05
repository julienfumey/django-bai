# BAI La boîte à idées

La boîte à idées est une application Django pour créer un cahier de suggestions.


## Contribuer

Pour contribuer, vous devez d'abord cloner le repository sur votre ordinateur. Ensuite, vous devez créer un environnement virtuel et l'activer.

```bash
python -m venv .venv
source .venv/bin/activate
```

Vous devez ensuite installer les requirements:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

Vous devez ensuite mettre en place django:
```bash
python manage.py migrate
python manage.py createsuperuser
```

Pour démarrer le serveur:
```bash
python manage.py runserver
```

Si vous changez les modèles, vous devez créer les fichiers de migrations et les appliquer :
```bash
python manage.py makemigrations
python manage.py migrate
```
