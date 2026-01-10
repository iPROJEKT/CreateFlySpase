[Setup]
AppName=CreateFlySpase
AppVersion=1.0
DefaultDirName={pf}\CreateFlySpase
DefaultGroupName=CreateFlySpase
OutputDir=dist_installer
SetupIconFile=media\ico\ico.ico
OutputBaseFilename=CreateFlySpaseInstaller
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "build\win_amd64\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CreateFlySpase"; Filename: "{app}\CreateFlySpase.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\CreateFlySpase"; Filename: "{app}\CreateFlySpase.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Создать ярлык на рабочем столе"

[Run]
Filename: "{app}\CreateFlySpase.exe"; Description: "Запустить CreateFlySpase"; Flags: nowait postinstall skipifsilent