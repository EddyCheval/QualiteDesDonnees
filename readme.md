# Module **Qualité Des Données**

Projet réalisé par **Eddy CHEVAL** & **Alban GUILLET**, EPSI Nantes I2 Classe 2 2020-2021.

## Version utilisée dans le cadre de ce projet

|Elément|Version|
|---|---|
|Python|3.9.1|
|pip|20.2.3|
|numpy|1.19.5|
|pandas|1.2.0|
|matplotlib|3.3.3|

## Détail sur la réalisation du projet

### Calcul de valeurs à partir d'un dataframe (SI)

Pour l'affichage des données suivantes :
- moyenne par mois
- min / max par mois et par année
- écart type par mois

Nous avons choisi d'utiliser Numpy plutôt que Scipy car les méthodes de cette dernière sont décrites comme "*deprecated*". Il est aussi recommandé d'utiliser Numpy.

### Nettoyage des données de SI - Erreur

#### Démarche
Dans le jeu de données SI - erreur, on peut y distinguer deux types d'erreur :
- Les erreurs de types (Exemple : Sun, 0xFFFF)
- Les erreurs d'échelle (Exemple: 48°C,-33°C)

Pour répondre à ces deux problématiques, nous allons employer deux méthodes :
- La première méthode consiste à convertir toutes les valeurs non-numérique en NaN
- La seconde méthode consiste à utiliser l'écart interquartile pour évaluer si une valeur est incohérente vis-à-vis des valeurs du mois correspondant. 
On définit l'incohérence en fonction d'un paramètre laissé à l'appréciation de chacun de la définition d'un outliner.(Dans notre cas la valeur est 3)

Ensuite, une fois que toutes les valeurs incohérentes sont transformées en NaN, nous pouvons mettre à l'œuvre notre stratégie visant à rendre cohérentes ces valeurs. 
S'agissant de la température des villes, on peut supposer qu'il existe un lien fort entre la température des jours J, J-1 et J+1. 
Ainsi, nous sommes partis sur le principe que nos valeurs NaN pouvaient être remplacées par une moyenne de J-1 et J+1 afin de préserver la cohérence de l'ensemble.

#### Conclusion
En utilisant cette méthode, on remarque que globalement les valeurs sont proches de la réalité, mais que les informations qui ont été retravaillées ont parfois des écarts significatifs comme pour le mois de janvier par exemple avec 9°C de différence. Toutefois, dans l'ensemble, la différence n'est pas très conséquente.

On remarque, une fois les moyennes faites, qu'à l'échelle de la donnée annuel la différence est moindre (-0.011) et que les différences en questions sont très proches de 0 avec une moyenne de -0.6 °C. 
La donnée est donc globalement fiable même après la correction des erreurs.


### Déterminer le type de climat de climat.xls

#### Démarche
En comparant climat.xls avec les données de Savukoski Kirkonkyla, on peut constater que la température est plus rude chez Savukoski Kirkonkyla et 
donc que la position de climat.xls doit être plus au sud. 
Ainsi, s'il s'agit d'une capitale on peut supposer qu'il s'agit d'Helsinki, la capital de la Finlande. Pour vérifier cette hypothèse, nous sommes allez chercher des données
météorologique d'Helsinki et d'autres capitales européennes.
Parmis ces capitales, nous avons choisit celles des pays suivants :
- France & Grèce, des pays relativement éloignés afin de confirmer que notre jeu de données correspond bien à l'Europe du nord. Cela permet aussi de vérifier que nos calculs sont cohérent en utilisant des valeurs bien différentes.
- Suède, Estonie, Lettonie, des pays de la même zone que notre jeu de données afin de situer un peu plus précisément le type de climat de celui-ci.

En comparant les données d'Helsinki et d'autres capitales que nous avons trouvé sur Internet, on peut renforcer cette hypothèse.
En effet, nous pouvons voir des similitudes entre les courbes du climat et des données trouvées sur Internet 
(Malgré quelques décalages notamment sur le pique de froid du début d'année. On peut supposer qu'il s'agit d'une année différente ou de données alterées.) 
mais également des similitudes au niveau des maximums et minimums.

Nous constatons 5°C de différence en moyenne à Helsinki avec un début d'année beaucoup plus chaud comme la plupart des capitales testées.
Toutefois on remarque que c'est bien le même type de climat car les deux courbes se suivent relativement bien contrairement à la courbe de Paris ou Athènes qui sont constamment au-dessus.
Elles sont donc probablement situées dans la même région du monde (dans notre cas la Finlande). 

Nous avons aussi choisit de calculer l'aire entre les courbes de nos capitales et celle de notre jeu de données. Plus l'écart entre les courbes est faible et plus la probabilité que nous ayons à faire à des climats similaires est forte. Pour cela, nous avons choisit d'utiliser une méthode basée sur l'intégrale. Nous avions choisi d'utiliser la méthode des trapèzes dans un premier temps mais celle-ci nous donnait des résultats qui ne nous paraissait pas correcte. Nous avons choisit une méthode déterminant les intersections entre les courbes pour déterminer l'aire entre chacune de ces sections afin de gérer les aires de manières "absolues". En effet, dans le cas ou deux courbes se croisent, il ne faudrait pas que les aires puissent s'annuler (bien qu'une aire n'est normalement pas négative). 

Afin d'avoir un résultat correcte nous avons choisit de mettre en place un système de scoring. Ce score nous permettera de déterminer quelle sera la ville la plus proche et se base sur diverses informations, obtenus précédement. Parmis celle-ci, nous retrouver l'aire que nous venons de calculer mais aussi le coefficient de corrélation.

#### Conclusion
Pour ce qui est de Savukoski, cela concorde avec nos hypothèses. Le climat finlandais est de type continental. On peut noter que Helsinki est plus proche d'un climat continental 
humide alors que Savukoski est plus proche d'un climat continental froid ce qui peut expliquer les différentes en 
terme de température, mais également les similitudes entre les courbes et renforce donc notre hypothèse comme quoi il s'agit de Helsinki.
Toutefois, il peut s'agir de Riga ou Tallinn, les capitales de la Lettonie et Estonie qui sont très proches géographiquement. Et il ne faut 
pas omettre qu'il existe d'autres capitales, que les données ne sont potentiellement pas sur les mêmes années de données et que rien ne garantir l'intégrité de nos données comme de ceux de nos sources extérieures.
