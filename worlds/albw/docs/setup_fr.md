# A Link Between Worlds Guide d'Installation

## Software Nécessaire

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases).
- Une ROM décryptée de A Link Between Worlds d'Amérique du Nord en `.3ds`. Les instructions pour dump la ROM peuvent être trouvées (en anglais) [ici](https://wiki.hacks.guide/wiki/3DS:Dump_titles_and_game_cartridges). **Faîtes bien attention à selectionner "decrypt" lors du dump.** Si vous avez un fichier en `.cci` renommez le juste en `.3ds` et si vous avez un fichier en `.cia` utilisez [makerom.exe packagé dans ctrtool (attention installez makerom pas ctrtool)](https://github.com/3DSGuy/Project_CTR/releases) ou ce [script](https://github.com/davFaithid/CIA-to-3DS-Rom-Converter/releases)
- [Azahar](https://azahar-emu.org/pages/download/) (ou une archive [Lime3DS](https://github.com/Lime3DS/lime3ds-archive) ou [Citra](https://github.com/PabloMK7/citra/releases)). Note: Si vous utilisez l'émulateur Azahar, renommer le fichier de ROM de `.3ds` à `.cci` pour qu'il soit accepté par l'émulateur. Ces fichiers sont identiques, c'est juste l'extension qui change.
- **Le jeu doit être joué en langue ANGLAISE.** *RIP le français. 😞* (si vous le faîtes pas vous allez casser le jeu et softlock)

## Installation

1. Installer la dernière version de MultiworldGG.
2. En AP: Télécharger `albw.apworld` et le mettre dans le dossier `Archipelago/custom_worlds/` (double-cliquer dessus devrais aussi fonctionner).
3. Dans l'emulateur, sélectionner `Fichier > Ouvrier dossier <nom de l'émulateur>` (ou `File > Open <émulateur> Folder` en anglais). Créer un dossier `load` dans le dossier de l'émulateur et un dossier `mods` dans le dossier `load`.
4. (Pour les utilisateurs de Azahar uniquement): Sélectionner `Émulation > Configuration` (ou `Emulation > Configure` en anglais). Puis sélectionner l'onglet `Debug` et tout en bas cochez (si c'est pas dajà fait) l'option `Activer le serveur RPC` (ou `Enable RPC Server` en anglais).

## Mise à jour

1. Supprimer le dossier albwrandomizer du dossier `MultiworldGG/lib/`.
2. Faire les étapes 2 et 3 de l'[Installation](#installation) 

## Générer une partie

1. Créer le fichier YAML d'option du joueur. Un exemple est inclus et peut être généré avec le bouton `Generate Yaml Templates` dans le launcher de MultiworldGG.
2. (Hôte uniquement, identique pour tous les jeux): Récupérer les YAMLs de tous les joueurs de la partie dans le dossier `MultiworldGG/Players`.
3. (Hôte uniquement, identique pour tous les jeux): Exécuter le launcher de MultiworldGG est sélectionner `Generate` ("Générer").
4. (Hôte uniquement, identique pour tous les jeux): Un fichier zip va être créé dans le dossier `MultiworldGG/output`. Téléverser ce fichier sur [le site de MultiworldGG](/uploads) pour héberger la partie.
5. Dans le fichier zip se trouvera un fichier en `.apalbw`. Ce fichier **est nécessaire** pour jouer au jeu.

## Jouer au jeu

1. L'hôte (celui qui génère la partie) vous donnera le fichier `.apalbw` qui aura été créé. Glisser le fichier sur le launcher de MultiworldGG ou appuyer sur `Open Patch` dans la launcher et sélectionner le fichier `.apalbw`.
2. Entrer le chemin vers votre ROM A Link Between Worlds (première fois uniquement, il est sauvegardé dans `MultiworldGG/host.yaml`). Attendre environ 20 seconds pour que le jeu soit patché.
3. Celà fera 2 choses. D'abord ouvrir le client A Link Between World et ensuite créer un fichier zip dans le même dossier que le patch et avec le même nom. Dézipper ce fichier pour récupérer le dossier `00040000000EC300` dedans.
4. Mettre le dossier `00040000000EC300` dans le dossier `load/mods/` créé à l'installation. (Si il y a déjà un dossier avec le même nom dedans supprimer, déplacer ou renommer l'ancien avant de mettre le nouveau.)
5. Éxécuter A Link Between Worlds dans l'émulateur. Le client devrait se connecter automatiquement à l'émulateur (sinon fermer tout puis se référer à [Continuer une partie](#continuer-une-partie)).
6. Entrer l'URL du serveur hébergant la partie dans le client et appuyer sur `Connect`.

## Continuer une partie

1. Éxécuter A Link Between Worlds dans l'émulateur.
2. Éxécuter le launcher de MultiworldGG et sélectionner le client A Link Between Worlds. Le client devrait se connecter automatiquement à l'émulateur. Si ça ne fonctionne pas, verifiez les étapes d'[Installation](#installation).
3. Entrer l'URL du serveur hébergant la partie dans le client et appuyer sur `Connect`.
