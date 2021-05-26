# YourBookingZone_Scraping

Ce projet permet de récupérer des informations de vols ou d'hébergements en interrogeant les sites/API

## Setup

- Pour récupérer les données de AirBnb lancer la commande suivante:

```bash
scrapy crawl airbnb --nolog -o $NOMFICHIER$ -a lieu=$LIEU$ -a bebe=$NB_BEBEs$ -a enfant=$NB_ENFANTS$-a adults= $NB_ADULTES$ -a checkin=$DATE_ALLER$ -a checkout=$DATE_RETOUR$ -a price_lb=$PRIX_MIN$ -a price_ub=$PRIX_MAX$
```

- Pour récupérer les données Google Flights lancer la commande suivante:

```bash
scrapy crawl flights --nolog -o $NOMFICHIER$
```

- Pour récupérer les données Voyages A Rabais lancer la commande suivante:

```bash
scrapy crawl voyagesarabais --nolog -o $NOMFICHIER$ -a depart=$AEROPORTDEDEPART$ -a arrivee=$PAYSARRIVEE$ -a date=$DATESTRING$ -a duree=$DUREE$ -a age1=$AGE1$ -a age2=$AGE2$ -a age3=$AGE3$ -a age4=$AGE4$
```
