#define source_path ReadIni(SourcePath + "\setup.ini", "Data", "source_path")
#define min_windows ReadIni(SourcePath + "\setup.ini", "Data", "min_windows")

#define MyAppName "MultiworldGG"
#define MyAppExeName "MultiworldGGLauncher.exe"
#define MyAppIcon "data/icon.ico"
#dim VersionTuple[4]
#define MyAppVersion GetVersionComponents(source_path + '\MultiworldGGLauncher.exe', VersionTuple[0], VersionTuple[1], VersionTuple[2], VersionTuple[3])
#define MyAppVersionText Str(VersionTuple[0])+"."+Str(VersionTuple[1])+"."+Str(VersionTuple[2])


[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{918BA46A-FAB8-460C-9DFF-AE691E1C865D}}
AppName={#MyAppName}
AppCopyright=Distributed under GPLv3 License
AppVerName={#MyAppName} {#MyAppVersionText}
VersionInfoVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
DefaultGroupName=MultiworldGG
OutputDir=setups
OutputBaseFilename=Setup {#MyAppName} {#MyAppVersionText}
Compression=lzma2
SolidCompression=yes
LZMANumBlockThreads=8
ArchitecturesInstallIn64BitMode=x64compatible arm64
ChangesAssociations=yes
ArchitecturesAllowed=x64compatible arm64
AllowNoIcons=yes
SetupIconFile={#MyAppIcon}
UninstallDisplayIcon={app}\{#MyAppExeName}
LicenseFile=docs\combined_license_inno.txt
WizardStyle= modern
SetupLogging=yes
MinVersion={#min_windows}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}";
Name: "deletelib"; Description: "Clean existing /lib folder and subfolders including /worlds (leave checked if unsure)"; Check: ShouldShowDeleteLibTask

[Types]
Name: "full"; Description: "Full installation"
Name: "minimal"; Description: "Minimal installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Dirs]
NAME: "{app}"; Flags: setntfscompression; Permissions: everyone-modify users-modify authusers-modify;

[Files]
Source: "{#source_path}\*"; Excludes: "*.sfc, *.log, data\sprites\alttp, SNI, EnemizerCLI"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#source_path}\SNI\*"; Excludes: "*.sfc, *.log"; DestDir: "{app}\SNI"; Flags: ignoreversion recursesubdirs createallsubdirs;
Source: "{#source_path}\EnemizerCLI\*"; Excludes: "*.sfc, *.log"; DestDir: "{app}\EnemizerCLI"; Flags: ignoreversion recursesubdirs createallsubdirs;
Source: "vc_redist.x64.exe"; DestDir: {tmp}; Flags: deleteafterinstall

[Icons]
Name: "{group}\{#MyAppName} Folder"; Filename: "{app}";
Name: "{group}\{#MyAppName} Launcher"; Filename: "{app}\MultiworldGGLauncher.exe"

Name: "{commondesktop}\{#MyAppName} Folder"; Filename: "{app}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyAppName} Launcher"; Filename: "{app}\MultiworldGGLauncher.exe"; Tasks: desktopicon

[Run]

Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/passive /norestart"; Check: IsVCRedist64BitNeeded; StatusMsg: "Installing VC++ redistributable..."
Filename: "{app}\MultiworldGGLauncher"; Parameters: "--update_settings"; StatusMsg: "Updating host.yaml..."; Flags: runasoriginaluser runhidden
Filename: "{app}\MultiworldGGLauncher"; Description: "{cm:LaunchProgram,{#StringChange('Launcher', '&', '&&')}}"; Flags: nowait postinstall skipifsilent
; Silent install from updater auto starts the launcher again
Filename: "{app}\MultiworldGGLauncher"; StatusMsg: "Restarting MultiworldGG Launcher..."; Flags: nowait skipifnotsilent


[UninstallDelete]
Type: dirifempty; Name: "{app}"

[InstallDelete]
Type: files; Name: "{app}\*.exe"
Type: files; Name: "{app}\data\lua\connector_pkmn_rb.lua"
Type: files; Name: "{app}\data\lua\connector_ff1.lua"
Type: filesandordirs; Name: "{app}\SNI\lua*"
Type: filesandordirs; Name: "{app}\EnemizerCLI*"
#include "installdelete.iss"

[Registry]

Root: HKCR; Subkey: ".aplttp";                                    ValueData: "{#MyAppName}alttppatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}alttppatch";                     ValueData: "MultiworldGG A Link to the Past Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}alttppatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                  ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}alttppatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";         ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apsm";                                     ValueData: "{#MyAppName}smpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smpatch";                       ValueData: "MultiworldGG Super Metroid Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smpatch\DefaultIcon";           ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smpatch\shell\open\command";    ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apdkc3";                                   ValueData: "{#MyAppName}dkc3patch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}dkc3patch";                     ValueData: "MultiworldGG Donkey Kong Country 3 Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}dkc3patch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}dkc3patch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".aptatk";                                   ValueData: "{#MyAppName}tatkpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}tatkpatch";                     ValueData: "MultiworldGG Tetris Attack Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}tatkpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}tatkpatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apsmw";                                    ValueData: "{#MyAppName}smwpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smwpatch";                      ValueData: "MultiworldGG Super Mario World Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smwpatch\DefaultIcon";          ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smwpatch\shell\open\command";   ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apzl";                                     ValueData: "{#MyAppName}zlpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}zlpatch";                       ValueData: "MultiworldGG Zillion Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}zlpatch\DefaultIcon";           ValueData: "{app}\MultiworldGGZillionClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}zlpatch\shell\open\command";    ValueData: """{app}\MultiworldGGZillionClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apsmz3";                                   ValueData: "{#MyAppName}smz3patch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smz3patch";                     ValueData: "MultiworldGG SMZ3 Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smz3patch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smz3patch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apsoe";                                    ValueData: "{#MyAppName}soepatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}soepatch";                      ValueData: "MultiworldGG Secret of Evermore Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}soepatch\DefaultIcon";          ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}soepatch\shell\open\command";   ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apl2ac";                                   ValueData: "{#MyAppName}l2acpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}l2acpatch";                     ValueData: "MultiworldGG Lufia II Ancient Cave Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}l2acpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}l2acpatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apkdl3";                                   ValueData: "{#MyAppName}kdl3patch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}kdl3patch";                     ValueData: "MultiworldGG Kirby's Dream Land 3 Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}kdl3patch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}kdl3patch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apmc";                                     ValueData: "{#MyAppName}mcdata";         Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mcdata";                        ValueData: "MultiworldGG Minecraft Data"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mcdata\DefaultIcon";            ValueData: "{app}\MultiworldGGLauncher.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mcdata\shell\open\command";     ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apz5";                                     ValueData: "{#MyAppName}n64zpf";         Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}n64zpf";                        ValueData: "MultiworldGG Ocarina of Time Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}n64zpf\DefaultIcon";            ValueData: "{app}\MultiworldGGLauncher.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}n64zpf\shell\open\command";     ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apred";                                    ValueData: "{#MyAppName}pkmnrpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}pkmnrpatch";                    ValueData: "MultiworldGG Pokemon Red Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}pkmnrpatch\DefaultIcon";        ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}pkmnrpatch\shell\open\command"; ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apblue";                                   ValueData: "{#MyAppName}pkmnbpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}pkmnbpatch";                    ValueData: "MultiworldGG Pokemon Blue Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}pkmnbpatch\DefaultIcon";        ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}pkmnbpatch\shell\open\command"; ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apbn3";                                    ValueData: "{#MyAppName}bn3bpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}bn3bpatch";                     ValueData: "MultiworldGG MegaMan Battle Network 3 Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}bn3bpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}bn3bpatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apemerald";                                 ValueData: "{#MyAppName}pkmnepatch";                               Flags: uninsdeletevalue; ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}pkmnepatch";                     ValueData: "MultiworldGG Pokemon Emerald Patch";                    Flags: uninsdeletekey;   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}pkmnepatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                                          ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}pkmnepatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                                 ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apmlss";                                 ValueData: "{#MyAppName}mlsspatch";                               Flags: uninsdeletevalue; ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mlsspatch";                     ValueData: "MultiworldGG Mario & Luigi Superstar Saga Patch";                    Flags: uninsdeletekey;   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mlsspatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                                          ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mlsspatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                                 ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apcv64";                                 ValueData: "{#MyAppName}cv64patch";                               Flags: uninsdeletevalue; ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}cv64patch";                     ValueData: "MultiworldGG Castlevania 64 Patch";                    Flags: uninsdeletekey;   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}cv64patch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                                          ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}cv64patch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                                 ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apcvcotm";                                 ValueData: "{#MyAppName}cvcotmpatch";                               Flags: uninsdeletevalue; ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}cvcotmpatch";                     ValueData: "MultiworldGG Castlevania Circle of the Moon Patch";                    Flags: uninsdeletekey;   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}cvcotmpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                                          ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}cvcotmpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                                 ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apcvdos";                                 ValueData: "{#MyAppName}cvdospatch";                               Flags: uninsdeletevalue; ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}cvdospatch";                     ValueData: "MultiworldGG Castlevania Dawn of Sorrow Patch";                    Flags: uninsdeletekey;   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}cvdospatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                                          ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}cvdospatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                                 ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apmm2";                                   ValueData: "{#MyAppName}mm2patch";                               Flags: uninsdeletevalue; ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mm2patch";                     ValueData: "MultiworldGG Mega Man 2 Patch";                    Flags: uninsdeletekey;   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mm2patch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                                          ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mm2patch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                                 ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apmm3";                                   ValueData: "{#MyAppName}mm3patch";                               Flags: uninsdeletevalue; ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mm3patch";                     ValueData: "MultiworldGG Mega Man 3 Patch";                    Flags: uninsdeletekey;   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mm3patch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                                          ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mm3patch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                                 ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apmmx3";                                   ValueData: "{#MyAppName}mmx3patch";                               Flags: uninsdeletevalue; ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mmx3patch";                     ValueData: "MultiworldGG Mega Man X3 Patch";                    Flags: uninsdeletekey;   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mmx3patch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                                          ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mmx3patch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                                 ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apladx";                                   ValueData: "{#MyAppName}ladxpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}ladxpatch";                     ValueData: "MultiworldGG Links Awakening DX Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}ladxpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}ladxpatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apladxb";                                   ValueData: "{#MyAppName}ladxbpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}ladxbpatch";                     ValueData: "MultiworldGG Links Awakening DX Beta Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}ladxbpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}ladxbpatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".aptloz";                                   ValueData: "{#MyAppName}tlozpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}tlozpatch";                     ValueData: "MultiworldGG The Legend of Zelda Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}tlozpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                          ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}tlozpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                     ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apadvn";                                   ValueData: "{#MyAppName}advnpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}advnpatch";                     ValueData: "MultiworldGG Adventure Patch";  Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}advnpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}advnpatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";       ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apyi";                                   ValueData: "{#MyAppName}yipatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}yipatch";                     ValueData: "MultiworldGG Yoshi's Island Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}yipatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}yipatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apygo06";                                   ValueData: "{#MyAppName}ygo06patch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}ygo06patch";                     ValueData: "MultiworldGG Yu-Gi-Oh 2006 Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}ygo06patch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}ygo06patch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apalbw";                                   ValueData: "{#MyAppName}apalbwpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apalbwpatch";                     ValueData: "MultiworldGG A Link Between Worlds Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apalbwpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apalbwpatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apbfbb";                                   ValueData: "{#MyAppName}apbfbbpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apbfbbpatch";                     ValueData: "MultiworldGG Spongebob: BFBB Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apbfbbpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apbfbbpatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apcivvi";                                   ValueData: "{#MyAppName}apcivvipatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apcivvipatch";                     ValueData: "MultiworldGG Civilization 6 Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apcivvipatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apcivvipatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apcrystal";                                     ValueData: "{#MyAppName}apcrystalpatch";    Flags: uninsdeletevalue;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apcrystalpatch";                     ValueData: "MultiworldGG Pkmn Crystal Patch"; Flags: uninsdeletekey;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apcrystalpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                        ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apcrystalpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";               ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apdkc";                                   ValueData: "{#MyAppName}dkcpatch";        Flags: uninsdeletevalue;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}dkcpatch";                     ValueData: "MultiworldGG Donkey Kong Country Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}dkcpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}dkcpatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apdkc2";                                   ValueData: "{#MyAppName}dkc2patch";        Flags: uninsdeletevalue;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}dkc2patch";                     ValueData: "MultiworldGG Donkey Kong Country 2 Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}dkc2patch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}dkc2patch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apeb";                                   ValueData: "{#MyAppName}apebpatch";        Flags: uninsdeletevalue;         ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apebpatch";                     ValueData: "MultiworldGG Earthbound Patch"; Flags: uninsdeletekey;     ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apebpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apebpatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apeos";                                     ValueData: "{#MyAppName}apeospatch";    Flags: uninsdeletevalue;           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apeospatch";                     ValueData: "MultiworldGG Pkmn MD Explorers of Sky Patch"; Flags: uninsdeletekey;  ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apeospatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                        ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apeospatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";               ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apff4fe";                                   ValueData: "{#MyAppName}apff4fepatch";        Flags: uninsdeletevalue;      ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apff4fepatch";                     ValueData: "MultiworldGG Final Fantase IV: FE Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apff4fepatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apff4fepatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apffvcd";                                     ValueData: "{#MyAppName}apffvcdpatch";        Flags: uninsdeletevalue;     ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apffvcdpatch";                     ValueData: "MultiworldGG Final Fantasy 5 CD Patch"; Flags: uninsdeletekey;        ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apffvcdpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apffvcdpatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apfirered";                                     ValueData: "{#MyAppName}apfireredpatch";    Flags: uninsdeletevalue;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apfireredpatch";                     ValueData: "MultiworldGG Pkmn Firered Patch"; Flags: uninsdeletekey;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apfireredpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                        ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apfireredpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";               ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apfm";                                     ValueData: "{#MyAppName}apfmpatch";    Flags: uninsdeletevalue;            ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apfmpatch";                     ValueData: "MultiworldGG Yu-Gi-Oh! Forbidden Memories Patch"; Flags: uninsdeletekey;  ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apfmpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                        ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apfmpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";               ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apgstla";                                     ValueData: "{#MyAppName}apgstlapatch";    Flags: uninsdeletevalue;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apgstlapatch";                     ValueData: "MultiworldGG Golden Sun TLA Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apgstlapatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                      ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apgstlapatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";             ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apk64cs";                                     ValueData: "{#MyAppName}apk64cspatch";    Flags: uninsdeletevalue;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apk64cspatch";                     ValueData: "MultiworldGG Kirby 64 Patch"; Flags: uninsdeletekey;         ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apk64cspatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                      ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apk64cspatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";             ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apleafgreen";                                     ValueData: "{#MyAppName}apleafgreenpatch";    Flags: uninsdeletevalue;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apleafgreenpatch";                     ValueData: "MultiworldGG Pkmn Leafgreen Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apleafgreenpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                      ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apleafgreenpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";             ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".aplm";                                     ValueData: "{#MyAppName}aplmpatch";    Flags: uninsdeletevalue;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}aplmpatch";                     ValueData: "MultiworldGG Luigi's Mansion Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}aplmpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                      ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}aplmpatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";             ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apmetfus";                                     ValueData: "{#MyAppName}apmetfuspatch";    Flags: uninsdeletevalue;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmetfuspatch";                     ValueData: "MultiworldGG Metroid Fusion Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmetfuspatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                      ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmetfuspatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";             ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apmk64";                                     ValueData: "{#MyAppName}apmk64patch";    Flags: uninsdeletevalue;        ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmk64patch";                     ValueData: "MultiworldGG Mario Kart 64 Patch"; Flags: uninsdeletekey;    ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmk64patch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                      ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmk64patch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";             ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apmmhd";                                     ValueData: "{#MyAppName}apmmhdpatch";        Flags: uninsdeletevalue;     ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmmhdpatch";                     ValueData: "MultiworldGG Madou Monogatari Patch"; Flags: uninsdeletekey;      ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmmhdpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmmhdpatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apmzm";                                     ValueData: "{#MyAppName}apmzmpatch";    Flags: uninsdeletevalue;          ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmzmpatch";                     ValueData: "MultiworldGG Metroid Zero Mission Patch"; Flags: uninsdeletekey;  ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmzmpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                        ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apmzmpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";               ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apooa";                                     ValueData: "{#MyAppName}apooapatch";    Flags: uninsdeletevalue;        ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apooapatch";                     ValueData: "MultiworldGG Oracle of Ages Patch"; Flags: uninsdeletekey;  ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apooapatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                     ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apooapatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";            ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apoos";                                     ValueData: "{#MyAppName}apoospatch";    Flags: uninsdeletevalue;           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apoospatch";                     ValueData: "MultiworldGG Oracle of Seasons Patch"; Flags: uninsdeletekey;  ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apoospatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                        ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apoospatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";               ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".appm64";                                     ValueData: "{#MyAppName}appm64patch";    Flags: uninsdeletevalue;          ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}appm64patch";                     ValueData: "MultiworldGG Paper Mario 64 Patch"; Flags: uninsdeletekey;     ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}appm64patch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                        ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}appm64patch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";               ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apsmmr";                                     ValueData: "{#MyAppName}apsmmrpatch";        Flags: uninsdeletevalue;     ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apsmmrpatch";                     ValueData: "MultiworldGG SM Map Rando Patch"; Flags: uninsdeletekey;      ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apsmmrpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apsmmrpatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apsms";                                     ValueData: "{#MyAppName}apsmspatch";    Flags: uninsdeletevalue;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apsmspatch";                     ValueData: "MultiworldGG Super Mario Sunshine Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apsmspatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                      ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apsmspatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";             ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apsotn";                                   ValueData: "{#MyAppName}apsotnpatch";      Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apsotnpatch";                     ValueData: "MultiworldGG SotN Patch"; Flags: uninsdeletekey;      ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apsotnpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";               ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apsotnpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";      ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".aptatk";                                     ValueData: "{#MyAppName}aptatkpatch";        Flags: uninsdeletevalue;     ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}aptatkpatch";                     ValueData: "MultiworldGG Tetris Attack Patch"; Flags: uninsdeletekey;        ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}aptatkpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}aptatkpatch\shell\open\command";  ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apttyd";                                     ValueData: "{#MyAppName}apttydpatch";    Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apttydpatch";                     ValueData: "MultiworldGG TTYD Patch"; Flags: uninsdeletekey;      ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apttydpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGLauncher.exe,0";                    ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apttydpatch\shell\open\command";  ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";           ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apwaffle";                                        ValueData: "{#MyAppName}smwwafflespatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smwwafflespatch";                      ValueData: "MultiworldGG SMW Waffles Patch";     Flags: uninsdeletekey; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smwwafflespatch\DefaultIcon";          ValueData: "{app}\MultiworldGGSNIClient.exe,0";                           ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}smwwafflespatch\shell\open\command";   ValueData: """{app}\MultiworldGGSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apwl";                                     ValueData: "{#MyAppName}apwlpatch";    Flags: uninsdeletevalue;         ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apwlpatch";                     ValueData: "MultiworldGG Wario Land Patch"; Flags: uninsdeletekey;      ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apwlpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                     ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apwlpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";            ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apwl4";                                     ValueData: "{#MyAppName}apwl4patch";    Flags: uninsdeletevalue;          ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apwl4patch";                     ValueData: "MultiworldGG Wario Land 4 Patch"; Flags: uninsdeletekey;      ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apwl4patch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                       ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apwl4patch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";              ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apygoddm";                                     ValueData: "{#MyAppName}apygoddmpatch";    Flags: uninsdeletevalue;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apygoddmpatch";                     ValueData: "MultiworldGG Yu-Gi-Oh! Dungeon Dice Monsters Patch"; Flags: uninsdeletekey;  ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apygoddmpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apygoddmpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";          ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".apz2";                                     ValueData: "{#MyAppName}apz2patch";    Flags: uninsdeletevalue;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apz2patch";                     ValueData: "MultiworldGG Zelda II Patch"; Flags: uninsdeletekey;      ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apz2patch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}apz2patch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";          ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".aptmc";                                     ValueData: "{#MyAppName}aptmcpatch";    Flags: uninsdeletevalue;       ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}aptmcpatch";                     ValueData: "MultiworldGG The Minish Cap Patch"; Flags: uninsdeletekey;      ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}aptmcpatch\DefaultIcon";         ValueData: "{app}\MultiworldGGBizHawkClient.exe,0";                   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}aptmcpatch\shell\open\command";  ValueData: """{app}\MultiworldGGBizHawkClient.exe"" ""%1""";          ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".multiworldgg";                              ValueData: "{#MyAppName}multidata";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}multidata";                     ValueData: "MultiworldGG Server Data";      Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}multidata\DefaultIcon";         ValueData: "{app}\MultiworldGGServer.exe,0";                         ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}multidata\shell\open\command";  ValueData: """{app}\MultiworldGGServer.exe"" ""%1""";                ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apmm3";                                   ValueData: "{#MyAppName}mm3patch";                               Flags: uninsdeletevalue; ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mm3patch";                     ValueData: "Archipelago Mega Man 3 Patch";                    Flags: uninsdeletekey;   ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mm3patch\DefaultIcon";         ValueData: "{app}\ArchipelagoBizHawkClient.exe,0";                                          ValueType: string; ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}mm3patch\shell\open\command";  ValueData: """{app}\ArchipelagoBizHawkClient.exe"" ""%1""";                                 ValueType: string; ValueName: "";

Root: HKCR; Subkey: ".archipelago";                              ValueData: "{#MyAppName}multidata";        Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}multidata";                     ValueData: "MultiworldGG Server Data";      Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}multidata\DefaultIcon";         ValueData: "{app}\MultiworldGGServer.exe,0";                         ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}multidata\shell\open\command";  ValueData: """{app}\MultiworldGGServer.exe"" ""%1""";                ValueType: string;  ValueName: "";

Root: HKCR; Subkey: ".apworld";                                 ValueData: "{#MyAppName}worlddata";  Flags: uninsdeletevalue; ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}worlddata";                    ValueData: "MultiworldGG World Data"; Flags: uninsdeletekey;   ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}worlddata\DefaultIcon";        ValueData: "{app}\MultiworldGGLauncher.exe,0";                 ValueType: string;  ValueName: "";
Root: HKCR; Subkey: "{#MyAppName}worlddata\shell\open\command"; ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";        ValueType: string;  ValueName: "";

Root: HKCR; Subkey: "mwgg"; ValueType: "string"; ValueData: "MultiworldGG Protocol"; Flags: uninsdeletekey;
Root: HKCR; Subkey: "mwgg"; ValueType: "string"; ValueName: "URL Protocol"; ValueData: "";
Root: HKCR; Subkey: "mwgg\DefaultIcon"; ValueType: "string"; ValueData: "{app}\MultiworldGGLauncher.exe,0";
Root: HKCR; Subkey: "mwgg\shell\open\command"; ValueType: "string"; ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";

Root: HKCR; Subkey: "archipelago"; ValueType: "string"; ValueData: "MultiworldGG Protocol"; Flags: uninsdeletekey;
Root: HKCR; Subkey: "archipelago"; ValueType: "string"; ValueName: "URL Protocol"; ValueData: "";
Root: HKCR; Subkey: "archipelago\DefaultIcon"; ValueType: "string"; ValueData: "{app}\MultiworldGGLauncher.exe,0";
Root: HKCR; Subkey: "archipelago\shell\open\command"; ValueType: "string"; ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";

Root: HKCR; Subkey: "multiworldgg"; ValueType: "string"; ValueData: "MultiworldGG Protocol"; Flags: uninsdeletekey;
Root: HKCR; Subkey: "multiworldgg"; ValueType: "string"; ValueName: "URL Protocol"; ValueData: "";
Root: HKCR; Subkey: "multiworldgg\DefaultIcon"; ValueType: "string"; ValueData: "{app}\MultiworldGGLauncher.exe,0";
Root: HKCR; Subkey: "multiworldgg\shell\open\command"; ValueType: "string"; ValueData: """{app}\MultiworldGGLauncher.exe"" ""%1""";


[Code]
// See: https://stackoverflow.com/a/51614652/2287576
function IsVCRedist64BitNeeded(): boolean;
var
  strVersion: string;
begin
  if (RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Version', strVersion)) then
  begin
    // Is the installed version at least the packaged one ?
    Log('VC Redist x64 Version : found ' + strVersion);
    Result := (CompareStr(strVersion, 'v14.38.33130') < 0);
  end
  else
  begin
    // Not even an old version installed
    Log('VC Redist x64 is not already installed');
    Result := True;
  end;
end;

function ShouldShowDeleteLibTask: Boolean;
begin
  Result := DirExists(ExpandConstant('{app}\lib'));
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssInstall then
  begin
    if WizardIsTaskSelected('deletelib') then
      DelTree(ExpandConstant('{app}\lib'), True, True, True);
  end;
end;
