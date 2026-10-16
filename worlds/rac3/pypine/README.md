# pypine

### Based on https://projects.govanify.com/govanify/pine

This is a client side implementation of the PINE protocol.
It allows for a three-way communication between the emulated game, the emulator and an external
tool, using the external tool as a relay for all communication. It is a socket based IPC that
is _very_ fast.

If you want to draw comparisons you can think of this as an equivalent of the BizHawk LUA API,
although with the logic out of the core and in an external tool. While BizHawk would run a lua
script at each frame in the core of the emulator, PINE opts instead to keep the entire logic out of
the emulator.