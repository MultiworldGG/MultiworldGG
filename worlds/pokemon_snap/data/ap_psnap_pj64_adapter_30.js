var port = 48080;
var CONFIG_CANDIDATES = ["Config\\Project64.cfg", ".\\Config\\Project64.cfg"];

(function loadPort() {
    for (var c = 0; c < CONFIG_CANDIDATES.length; c++) {
        try {
            var file = fs.readFile(CONFIG_CANDIDATES[c]).toString();
            var lines = file.split("\n");
            for (var i = 0; i < lines.length; i++) {
                if (lines[i].trim().toLowerCase().indexOf("psnap_ap_port=") === 0) {
                    var parsedPort = parseInt(lines[i].split("=")[1].trim(), 10);
                    if (!isNaN(parsedPort)) {
                        port = parsedPort;
                        console.log("Using AP port from Project64.cfg: " + port);
                    }
                    return;
                }
            }
        } catch (e) {}
    }
    console.log("Could not read psnap_ap_port from Project64.cfg, using fallback port: " + port);
})();

function getRomInfo() {
    try {
        var name = rom.getstring(0x20, 20).replace(/\0/g, "").trim();
        return {
            name: name,
            goodName: name,
            id: rom.getstring(0x3B, 4),
            countryCode: rom.u8[0x3E],
            crc1: rom.u32[0x10] >>> 0,
            crc2: rom.u32[0x14] >>> 0
        };
    } catch (e) {
        return null;
    }
}

var MemoryBridge = {
    read: function(type, address, size) {
        var result = [];
        if (type === "bytestring") {
            for (var i = 0; i < size; i++) {
                result.push(String.fromCharCode(mem.u8[address + i]));
            }
            return result.join("");
        }

        var step = (type === "u32" || type === "s32") ? 4 : (type === "u16" || type === "s16") ? 2 : 1;
        var view = mem[type];

        for (var i = 0; i < size; i += step) {
            result.push(view[address + i]);
        }
        return result;
    },

    write: function(type, address, value) {
        if (type === "bytestring") {
            for (var i = 0; i < value.length; i++) {
                mem.u8[address + i] = value.charCodeAt(i);
            }
            return true;
        }

        var step = (type === "u32" || type === "s32") ? 4 : (type === "u16" || type === "s16") ? 2 : 1;
        var view = mem[type];

        for (var i = 0; i < value.length; i++) {
            view[address + (i * step)] = value[i];
        }
        return true;
    }
};

function handleMessage(client, data) {
    var message = data.toString().trim();
    var parts = message.split(':');
    if (parts.length < 2) {
        client.write("ERR:Invalid message format\n");
        return;
    }

    var messageId = parts[0];
    var payload = parts.slice(1).join(':').trim();
    var args = payload.split(" ");
    var command = args[0].toLowerCase();

    switch (command) {
        case "rominfo":
            client.write(messageId + ":" + JSON.stringify(getRomInfo()) + "\n");
            break;

        case "read":
            var type = args[1];
            var address = parseInt(args[2], 16);
            var size = parseInt(args[3], 10);

            if (isNaN(address) || isNaN(size) || size <= 0) {
                client.write(messageId + ":Invalid read parameters\n");
                break;
            }

            var dataOut = MemoryBridge.read(type, address, size);
            var response = (type === "bytestring") ? dataOut : JSON.stringify(dataOut);
            client.write(messageId + ":" + response + "\n");
            break;

        case "dict":
            var rawJson = payload.substring(5).trim();
            try {
                var dict = JSON.parse(rawJson);
                var result = {};
                for (var key in dict) {
                    var item = dict[key];
                    if (typeof item !== "object") item = { "adr": item };
                    var dtype = item.type || "u8";
                    var dsize = item.size || 1;
                    result[key] = MemoryBridge.read(dtype, item.adr, dsize);
                }
                client.write(messageId + ":" + JSON.stringify(result) + "\n");
            } catch (e) {
                client.write(messageId + ":Invalid Dict JSON Format\n");
            }
            break;

        case "write":
            var wtype = args[1];
            var waddress = parseInt(args[2], 16);
            var rawValue = args.slice(3).join(" ");

            if (isNaN(waddress)) {
                client.write(messageId + ":Invalid Target Address\n");
                return;
            }

            var parsedValue;
            if (wtype === "bytestring") {
                parsedValue = rawValue;
            } else {
                try {
                    parsedValue = JSON.parse(rawValue);
                    if (!Array.isArray(parsedValue)) throw new Error();
                } catch (e) {
                    client.write(messageId + ":Value must be a valid JSON Array\n");
                    return;
                }
            }

            MemoryBridge.write(wtype, waddress, parsedValue);
            client.write(messageId + ":Write successful\n");
            break;

        default:
            client.write(messageId + ":Unknown command\n");
            break;
    }
}

function startServer() {
    console.log("Starting Pokemon Snap AP server on port " + port + "...");
    var server = new Server({ port: port });

    server.on('connection', function(client) {
        console.log("Client connected");
        var isConnected = true;

        client.on('data', function(data) {
            if (!isConnected) return;
            handleMessage(client, data);
        });

        client.on('close', function() {
            if (isConnected) {
                isConnected = false;
                console.log("Client disconnected");
            }
        });
    });
}

try {
    startServer();
} catch (e) {
    console.log("Failed to start Pokemon Snap AP server: " + e.message);
    alert("Pokemon Snap AP failed to start the server on port " + port + ".\n" + e.message,
        "Pokemon Snap AP");
}
