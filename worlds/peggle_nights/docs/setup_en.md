# Peggle Nights Randomizer Setup Guide

## Requirements
- Windows OS (Hard required. Client is using memory reading / writing / allocation through Windows APIs)
- Peggle Nights installed through Steam
  - Only the English version is supported. Other languages use different executables. 
  - The language can be changed in Properties -> General on Steam
- MultiworldGG 0.7.150+

**Hashes of expected PeggleNights.exe**

```
Name: PeggleNights.exe
Size: 5278776 bytes (5155 KiB)
CRC32: AA0A91B1
CRC64: 7CA74E22A9D8FDA1
SHA256: 98bb17b774eaf6eeb07df5979e1f008846722c73dd31c0a6e2eede6933c38352
SHA1: e4edd172fcca6fd091c1c06d24aee571c127eeac
BLAKE2sp: 4f3d9397bc243eb2c03943c64a2e4ec21c99c7fd797b27fa85bec95f083dec23
```

## Game Setup Instructions
No manual mod installation or other configuration is required to play Peggle Nights with MultiworldGG. The client included with the APWorld does all the work by attaching to the game process and monitoring and manipulating the game state in real-time.

**IMPORTANT**

Once the MultiworldGG client is connected, hooks and patches will be set up in the game's memory. _**If the client is ever closed, Peggle Nights will NEED to be restarted before connecting another client**_ for everything to function as expected. If you don't restart the game, the previous hooks and patches will remain installed with no way for the new client to detect and use them.

**Notes** 
- You don't need to have completed Adventure Mode to play. The client will be able to unlock the Quick Play levels as needed regardless of Adventure progress.
- Fever Meter Multiplier location checks will send when you hit the next peg after reaching the multiplier in the fever meter

## Joining a Multiworld Game
- Launch Peggle Nights and either sit on the splash screen or advance to the main menu
- Open the MultiworldGG Launcher. Find and click _Peggle Nights Client_
- Using the _Peggle Nights Client_:
  - Enter the room's hostname and port number (e.g. multiworld.gg:54321) in the top box and click Connect
  - Input your player name at the bottom when prompted and press Enter
  - You should now be connected to the MultiworldGG room
  - After a few seconds, you should see a message in the client that says `Peggle Nights process found!`
  - You are now ready to play Peggle Nights with MultiworldGG. Make sure to check out the `Peggle Nights` tab in the client

## Continuing a Multiworld Game
- Perform the same steps as above