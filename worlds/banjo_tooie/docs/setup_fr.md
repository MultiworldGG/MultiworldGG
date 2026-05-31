# Guide d'installation pour le randomiseur MultiworldGG de Banjo-Tooie

## Important

Ce guide s'applique uniquement aux systèmes Windows et Linux.
Le randomizeur prend également en charge l'Everdrive 3.0 et X7 (support USB).

## Logiciels et matériel requis

- Emulation sur PC:
    -   BizHawk: [Versions de BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory)
        -   La version **2.10** et les versions plus récentes sont supportées
        -   Les instructions d'installation détaillées de BizHawk se trouvent sur le lien ci-dessus
        -   Sur Windows, il faut d'abord exécuter l'installateur des pré-requis, également disponible sur le lien ci-dessus.
    -   Project64 3.0: [Versions publiques](https://www.pj64-emu.com/public-releases)
        -   Version **3.0.1** supportée
        -   Les paramètres par défaut devraient fonctionner.
        -   Activez le plugin d'entrée N-Rage si vous rencontrez des problèmes de configuration de manette.
        -   N'activez pas le débogage dans Options > configuration > Debugging
        -   Pour réduire le lag:
            1. Ouvrez la ROM
            2. Options > Config: RANDO TOOIE > Counter Factor à 0 ou 1
    -   Project64 4.0: [Versions de développement](https://www.pj64-emu.com/nightly-builds)
        -   Version **4.0.6701** testée
        -   Le Interpreter Core doit être activé:
            - Options > configurations > Décochez Hide Advanced Settings
            - Options > configurations > Advanced > Always Enable Interpreter Core
            - N'activez pas le débogage dans Options > configuration > Debugging
        -   Pour réduire le lag:
            1. Ouvrez la ROM
            2. Options > Config: RANDO TOOIE > Counter Factor à 0 ou 1
    -   Luna64: [Dernières versions](https://github.com/Luna-Project64/Luna-Project64/releases)
        -   Version **3.6.5** testée
        -   Emulate Frame Buffer doit être activé:
            - Options > Graphic Settings > Frame Buffer > Emulate Frame Buffer
            - N'activez pas le débogage dans Options > configuration > Debugging
        -   Pour réduire le lag:
            1. Ouvrez la ROM
            2. Options > Config: RANDO TOOIE > Counter Factor à 0 ou 1
    -   RMG: [Dernières versions](https://github.com/Rosalie241/RMG/releases)
        -   Version **0.8.9** testée
        -   Les paramètres par défaut devraient fonctionner.
        -   Pour réduire le lag:
            1. Ouvrez la ROM
            2. Settings > Game > Counter Factor à 0 ou 1
- Everdrive:
    - Le pilote USB sur le PC qui se connectera à l'Everdrive
        - Windows: https://ftdichip.com/wp-content/uploads/2021/08/CDM212364_Setup.zip
        - Linux: https://ftdichip.com/wp-content/uploads/2022/07/libftd2xx-x86_64-1.4.27.tgz
    - Pour l'Everdrive 3.0, la version du système d'exploitation doit être 3.06 pour être compatible
    - Le Nintendo 64 Expansion Pak est requis
    - Téléchargez la dernière version du connecteur Everdrive sur https://github.com/jjjj12212/AP_Banjo-Tooie/releases
-   Une ROM de Banjo-Tooie (version nord-américaine uniquement)

## Jouer sur BizHawk
### Configuration de BizHawk

Une fois BizHawk installé, ouvrez EmuHawk et modifiez les paramètres suivants:

- Sous Config > Customize, cochez les cases "Run in background" et "Accept background input". Cela vous permettra de continuer à jouer en arrière-plan, même si une autre fenêtre est sélectionnée
- Sous Config > Hotkeys, de nombreux raccourcis sont listés, avec beaucoup d'entre eux liés à des touches courantes du clavier. Vous voudrez probablement en désactiver la plupart, ce que vous pouvez faire rapidement avec `Esc`
- Si vous jouez avec une manette, lors de la configuration des contrôles, désactivez "P1 A Up", "P1 A Down", "P1 A Left" et "P1 A Right", car ils interfèrent avec la sensibilité du joystick. Configurez plutôt les directions avec l'onglet Analog
- Sous N64, activez "Use Expansion Slot". (Le menu N64 n'apparaît qu'après le chargement d'une ROM.)
- Sous Config -> Speed/Skip, cliquez sur "Audio Throttle", car cela corrige les sons déformés pendant le jeu

Il est fortement recommandé d'associer les extensions de ROM N64 (*.n64, *.z64) à EmuHawk. Pour ce faire, recherchez une ROM N64 que vous possédez, faites un clic droit et sélectionnez "Ouvrir avec…", dépliez la liste qui apparaît et sélectionnez l'option en bas "Rechercher une autre application", puis parcourez jusqu'au dossier BizHawk et sélectionnez EmuHawk.exe.

Si vous rencontrez des problèmes de performance avec Banjo-Tooie, vous pouvez essayer ceci:
- Sous N64 -> Plugins, définissez Active Video Plugin sur Rice.
Cela créera quelques artefacts visuels, mais cela ne devrait pas affecter le gameplay.

Pour vous aider à récupérer après un crash dans BizHawk, jouez avec le script BT_companion.lua chargé en faisant glisser le script Lua depuis data/lua/BT_companion.lua sur BizHawk.

### Démarrage - Émulateur
- Lancez Launcher.exe et sélectionnez Banjo-Tooie Client
- Si c'est la première fois que vous exécutez cette version, le client vous demandera votre ROM Banjo-Tooie (US)
- La ROM patchée se trouve par défaut dans le dossier racine de MultiworldGG
    - Le chemin exact est également affiché dans le client Banjo-Tooie
    - Vous pouvez aussi cliquer sur "Browse Files" dans le Launcher, ce qui vous mènera à ce dossier
- **Une seule fois**, exécutez `/autostart` dans le client Banjo-Tooie et sélectionnez votre émulateur préféré. Cela ouvrira automatiquement votre émulateur et la ROM patchée de Banjo-Tooie
- Pour certains émulateurs qui ne s'ouvrent pas automatiquement, exécutez `/program_args ` et réessayez
- Connectez le client MultiworldGG au serveur.
    - Pour connecter le client au multiserver, entrez simplement `<adresse>:<port>` dans le champ en haut et appuyez sur `connect` (si le serveur utilise un mot de passe, il vous sera demandé après la connexion)
- Si vous préférez ne pas utiliser **/autostart**:
    - Ouvrez votre émulateur supporté préféré et chargez votre ROM patchée de Banjo-Tooie (US)

- Si vous utilisez **BizHawk**, une fois dans le menu titre ou l'écran de sélection de sauvegarde, faites glisser-déposer le script BT_companion.lua (qui se trouve dans le dossier data/lua de MultiworldGG) sur la fenêtre de la console Lua. Cela vous permettra de récupérer après un crash si vous en rencontrez un.

## Jouer sur Everdrive
- Lancez MultiworldGGLauncher.exe et sélectionnez Banjo-Tooie Client
- Si c'est la première fois que vous exécutez cette version, le client vous demandera votre ROM Banjo-Tooie (US)
- La ROM patchée se trouve dans le dossier racine de MultiworldGG
    - Le chemin exact est également affiché dans le client Banjo-Tooie
    - Vous pouvez aussi cliquer sur "Browse Files" dans le Launcher, ce qui vous mènera à ce dossier
- Chargez la version patchée de la ROM sur la carte SD de votre Everdrive
- L'Everdrive devra être connecté en USB au PC qui exécutera le client Banjo-Tooie
- **Une seule fois**, exécutez `/autostart` dans le client Banjo-Tooie et sélectionnez banjo_tooie_everdrive_connector.exe. Cela ouvrira automatiquement le connecteur pour l'Everdrive
    - Si vous êtes sur Linux, sélectionnez Banjo_Tooie_everdrive_connector_linux à la place
- Si vous préférez ne pas utiliser `/autostart`:
    - Ouvrez banjo_tooie_everdrive_connector.exe si vous êtes sur Windows
    - Si vous êtes sur Linux, sélectionnez Banjo_Tooie_everdrive_connector_linux à la place
- Lancez la ROM patchée de Banjo-Tooie sur l'Everdrive
- Connectez le client MultiworldGG au serveur. (La fenêtre banjo_tooie_connector devrait afficher "Connection Established")
- Pour connecter le client au multiserver, entrez simplement `<adresse>:<port>` dans le champ en haut et appuyez sur `connect` (si le serveur utilise un mot de passe, il vous sera demandé après la connexion)
