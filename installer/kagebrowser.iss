; Inno Setup script for KageBrowser
; Version is injected by build.py via /DAppVersion=

#define MyAppName "KageBrowser"
#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif
#define MyAppVersion AppVersion
#define MyAppPublisher "denis-charnetskiy"
#define MyAppURL "https://github.com/dencusman-ux/KageBrowser"
#define MyAppExeName "KageBrowser.exe"

[Setup]
AppId={{8F3C1D2A-6B4E-4C7A-9E11-KAGEBUILDER01}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\KageBrowser
DefaultGroupName=KageBrowser
DisableProgramGroupPage=yes
OutputDir=..\artifacts
OutputBaseFilename=KageBrowser-{#MyAppVersion}-Setup
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\{#MyAppExeName}
ChangesAssociations=yes

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
