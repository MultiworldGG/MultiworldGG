# Guide de configuration pour Ocarina of Time Archipelago

## Logiciel requis

- Un émulateur au choix
  - [BizHawk] (https://tasvideos.org/BizHawk/ReleaseHistory) (v2.10+)
  - [Project 64](https://www.pj64-emu.com/windows-downloads)
  - [simple64](https://simple64.github.io/)
  - [Rosalie's Mupen GUI](https://github.com/Rosalie241/RMG)
  - [Gopher64](https://github.com/gopher64/gopher64) (Windows/Linux)
  - [ares](https://ares-emu.net/) (Windows/Linux)
  - [RetroArch](https://www.retroarch.com/?page=platforms) (marche sur MacOS) 
- Le OoT client Archipelago intégré, qui peut être installé [ici](https://github.com/ArchipelagoMW/Archipelago/releases)
- Un fichier ROM v1.0 US d'Ocarina of Time.

## Configuration de BizHawk

Une fois BizHawk installé, ouvrez EmuHawk et modifiez les paramètres suivants :

- Sous Config > Personnaliser > Avancé, assurez-vous que la case AutoSaveRAM est cochée et cliquez sur le bouton 5s.
   Cela réduit la possibilité de perdre des données de sauvegarde en cas de crash de l'émulateur.
- Sous Config > Personnaliser, cochez les cases « Exécuter en arrière-plan » et « Accepter la saisie en arrière-plan ». Cela vous permettra continuez à jouer en arrière-plan, même si une autre fenêtre est sélectionnée.
- Sous Config > Hotkeys, de nombreux raccourcis clavier sont répertoriés, dont beaucoup sont liés aux touches communes du clavier. Vous voudrez probablement pour désactiver la plupart d'entre eux, ce que vous pouvez faire rapidement en utilisant « Esc ».
- Si vous jouez avec une manette, lorsque vous associez des commandes, désactivez "P1 A Up", "P1 A Down", "P1 A Left" et "P1 A Right".
   car ceux-ci interfèrent avec la visée s’ils sont liés. Définissez plutôt l'entrée directionnelle à l'aide de l'onglet Analogique.
- Sous N64, activez "Utiliser le connecteur d'extension". Ceci est nécessaire pour que les états de sauvegarde fonctionnent.
   (Le menu N64 n'apparaît qu'après le chargement d'une ROM.)

Il est fortement recommandé d'associer les extensions de rom N64 (\*.n64, \*.z64) à l'EmuHawk que nous venons d'installer.
Pour ce faire, vous devez simplement rechercher n'importe quelle rom N64 que vous possédez, faire un clic droit et sélectionner "Ouvrir avec...", déplier la liste qui apparaît et sélectionnez l'option du bas "Rechercher une autre application", puis accédez au dossier BizHawk et sélectionnez EmuHawk.exe.

Un guide de configuration BizHawk alternatif ainsi que divers conseils de dépannage sont disponibles
[ici](https://wiki.ootrandomizer.com/index.php?title=Bizhawk).

## Créer un fichier de configuration (.yaml)

### Qu'est-ce qu'un fichier de configuration et pourquoi en ai-je besoin ?

Consultez le guide sur la configuration d'un YAML de base lors de la configuration de l'archipel.
guide : [Guide de configuration de base de Multiworld](/tutorial/Archipelago/setup/en)

### Où puis-je obtenir un fichier de configuration (.yaml) ?

La page Paramètres du lecteur sur le site Web vous permet de configurer vos paramètres personnels et d'exporter un fichier de configuration depuis eux. Page des paramètres du joueur : [Page des paramètres du joueur d'Ocarina of Time](/games/Ocarina%20of%20Time/player-options)

### Vérification de votre fichier de configuration

Si vous souhaitez valider votre fichier de configuration pour vous assurer qu'il fonctionne, vous pouvez le faire sur la page YAML Validator. 
YAML page du validateur : [page de validation YAML](/mysterycheck)

## Rejoindre un jeu multimonde

### Obtenez votre fichier OOT modifié

Lorsque vous rejoignez un jeu multimonde, il vous sera demandé de fournir votre fichier YAML à celui qui l'héberge. Une fois cela fait, l'hébergeur vous fournira soit un lien pour télécharger votre fichier de données, soit un fichier zip contenant les données de chacun des dossiers. Votre fichier de données doit avoir une extension « .apz5 ».

Double-cliquez sur votre fichier « .apz5 » pour démarrer votre client et démarrer le processus de correctif ROM. Une fois le processus terminé (cela peut prendre un certain temps), le client et l'émulateur seront automatiquement démarrés (si vous avez associé l'extension à l'émulateur comme recommandé).
Pour choisir un émulateur précis au lancement automatique, définissez `oot_options.emulator_path` dans votre `host.yaml`
avec le chemin vers l'exécutable de l'émulateur. Laissez ce champ vide pour utiliser l'application par défaut de votre
système pour les fichiers `.z64`.

### Connectez-vous au multiserveur

Une fois le client et l'émulateur démarrés, le client OoT se connecte automatiquement à la ROM chargée. Vous n'avez pas
besoin d'ouvrir la console Lua de BizHawk ni de faire glisser un script de connexion dans l'émulateur. Si le client ne se
connecte pas, vérifiez que la ROM corrigée est chargée dans un émulateur pris en charge, puis utilisez `/n64` dans le
client pour vérifier l'état de la connexion à l'émulateur.
Pour RetroArch, activez `Settings > Network > Network Commands` et laissez le Network Command Port sur `55355`.

Pour connecter le client au multiserveur, mettez simplement `<adresse>:<port>` dans le champ de texte en haut et appuyez sur Entrée (si le serveur utilise un mot de passe, tapez dans le champ de texte inférieur `/connect <adresse>:<port> [mot de passe]`)

Vous êtes maintenant prêt à commencer votre aventure dans Hyrule.
