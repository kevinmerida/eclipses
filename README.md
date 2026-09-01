# Les éclipses de Soleil

## Introduction

Le site [**timeanddate**](https://www.timeanddate.com/) donne accès à de nombreuses informations, dont celles associées aux éclipses de Soleil. Dans la suite de l'exposé, l'idée est d'exploiter les données disponibles sur ce site afin de restituer une séquence illustrant un moyen de prédire la trajectoire de l'ombre lors d'une éclipse. Cette prédiction fait appel aux [éléments besseliens](https://fr.wikipedia.org/wiki/%C3%89l%C3%A9ments_besseliens), où l'on s'intéresse initialement à l'ombre projetée sur un plan orthogonal à la direction Soleil-Terre.

Pour chaque éclipse, le site **timeanddate** propose une vidéo montrant la trajectoire de l'ombre sur une carte en [projection cylindrique équidistante](https://fr.wikipedia.org/wiki/Projection_cylindrique_%C3%A9quidistante). Cette carte est le résultat d'une prédiction dont on a du mal à saisir les étapes, la forme complexe des différentes zones (ombre totale ou partielle) ne pouvant pas aboutir à une interprétation simple. Avec la conversion de cette carte en une [projection orthographique](https://fr.wikipedia.org/wiki/Projection_orthographique) centrée sur le point où, à chaque instant, le Soleil est à la verticale du lieu (point subsolaire), on restitue une vue où la forme de l'ombre (circulaire) et son déplacement (linéaire) est bien plus explicite. On peut par ailleurs orienter la projection de sorte que l'axe horizontal corresponde au **plan de l'écliptique**. 

## Les programmes

Le programme en Python [**eclipse.py**](eclipse.py) réalise la conversion de la vidéo initiale (**vid_ent**) visualisant la trajectoire de l'ombre en projection cylindrique équidistante en une vidéo (**vid_sor**) en projection orthographique.

Cette vidéo initiale peut être téléchargée à partir de [la page décrivant l'éclipse sur le site timeanddate (Eclipse Shadow Path)](https://www.timeanddate.com/eclipse/solar/1999-august-11), par exemple celle du **11 août 1999**.

Il faut par ailleurs disposer de la latitude (**phi0**) et la longitude (**lambda0**) du point subsolaire à l'heure UTC où débute la séquence, disponibles sur [**Day and Night World Map**](https://www.timeanddate.com/worldclock/sunearth.html?iso=19990811T0822). Une correction sur la longitude est éventuellement nécessaire, si la carte initiale n'est pas centrée sur le méridien 0. La carte finale est de dimension **T**X**T** pixels.

Enfin, l'inclinaison apparente de l'axe de rotation de la Terre est vers la gauche du 21 juin au 21 décembre (**sig_theta=1**) et vers la droite du 21 décembre au 21 juin (**sig_theta=-1**).

Avec l'exemple de l'éclipse du 11 août 1999, choisi pour décrire le mode d'emploi, le programme [eclipse_19990811.py](eclipse_19990811.py) lance directement la fonction de conversion, avec les paramètres requis.

```python
from eclipse import eclipse_orth
eclipse_orth(vid_ent="anim-19990811.mp4", vid_sor="eclipse_19990811.mp4", lambda0=55+49/60-25, phi0=15+21/60, sig_theta=1, T=500
```
## Les illustrations

### Commentaires

Les éclipses du 11 août 1999 et du 21 août 2017 appartiennent à la même [série de saros 145](https://fr.wikipedia.org/wiki/Saros_solaire_145).

Les éclipses du 1er août 2008 et du 12 août 2026 appartiennent à la même [série de saros 126](https://en.wikipedia.org/wiki/Solar_Saros_126).

### Eclipse du 11 août 1999

Le programme : [eclipse_19990811.py](eclipse_19990811.py)

https://github.com/user-attachments/assets/a962ef95-5c77-4093-8e62-c11a350d4df1

https://github.com/user-attachments/assets/50bbcf77-98ef-428d-93ca-bf4127535b39

### Eclipse du 21 août 2017

Le programme : [eclipse_20170821.py](eclipse_20170821.py)

https://github.com/user-attachments/assets/6fd30ac8-03d2-41a0-b124-0470af455456

https://github.com/user-attachments/assets/08e1f0a7-87a4-450e-8ca0-1f5ef9db4d79

### Eclipse du 1er août 2008

Le programme : [eclipse_20080801.py](eclipse_20080801.py)

https://github.com/user-attachments/assets/1df7c5ee-b333-4f40-9ec5-828de2fb8866

https://github.com/user-attachments/assets/aaefec92-ffda-4ed8-99b3-230b5f602f89

### Eclipse du 12 août 2026

Le programme : [eclipse_20260812.py](eclipse_20260812.py)

https://github.com/user-attachments/assets/6e2b2dd2-5b14-430c-9f72-616f98d0dca8

https://github.com/user-attachments/assets/c7bda5ef-061e-49a4-8544-33b5233b9d75

