from datetime import datetime
from uuid import UUID, uuid4
from pony.orm import Database, PrimaryKey, Required, Set, Optional, buffer, LongStr, db_session

from Utils import utcnow

db = Database()

STATE_QUEUED = 0
STATE_STARTED = 1
STATE_ERROR = -1


class Slot(db.Entity):
    id = PrimaryKey(int, auto=True)
    player_id = Required(int)
    player_name = Required(str)
    data = Optional(bytes, lazy=True)
    seed = Optional('Seed', index=True)
    game = Required(str, index=True)


class Room(db.Entity):
    id = PrimaryKey(UUID, default=uuid4)
    last_activity: datetime = Required(datetime, default=lambda: utcnow(), index=True)
    creation_time: datetime = Required(datetime, default=lambda: utcnow(), index=True)  # index used by landing page
    owner = Required(UUID, index=True)
    commands = Set('Command')
    seed = Required('Seed', index=True)
    multisave = Optional(buffer, lazy=True)
    show_spoiler = Required(int, default=0)  # 0 -> never, 1 -> after completion, -> 2 always
    timeout = Required(int, default=lambda: 4 * 60 * 60)  # seconds since last activity to shutdown
    tracker = Optional(UUID, index=True)
    # Port special value -1 means the server errored out. Another attempt can be made with a page refresh
    last_port = Optional(int, default=lambda: 0)
    lobby = Optional('Lobby')  # back-reference from Lobby.room


class Seed(db.Entity):
    id = PrimaryKey(UUID, default=uuid4)
    rooms = Set(Room)
    multidata = Required(bytes, lazy=True)
    owner = Required(UUID, index=True)
    creation_time: datetime = Required(datetime, default=lambda: utcnow(), index=True)  # index used by landing page
    slots = Set(Slot)
    spoiler = Optional(LongStr, lazy=True)
    meta = Required(LongStr, default=lambda: "{\"race\": false}")  # additional meta information/tags
    lobbies = Set('Lobby')  # back-reference from Lobby.seed


class Command(db.Entity):
    id = PrimaryKey(int, auto=True)
    room = Required(Room)
    commandtext = Required(str)


class Generation(db.Entity):
    id = PrimaryKey(UUID, default=uuid4)
    owner = Required(UUID)
    options = Required(buffer, lazy=True)
    meta = Required(LongStr, default=lambda: "{\"race\": false}")
    state = Required(int, default=0, index=True)


class GameDataPackage(db.Entity):
    checksum = PrimaryKey(str)
    data = Required(bytes)


# Lobby states
LOBBY_OPEN = 0
LOBBY_GENERATING = 1
LOBBY_DONE = 2
LOBBY_CLOSED = -1
LOBBY_LOCKED = 3


class Lobby(db.Entity):
    id = PrimaryKey(UUID, default=uuid4)
    title = Required(str)
    owner = Required(UUID, index=True)
    password_hash = Optional(str)
    creation_time = Required(datetime, default=lambda: utcnow(), index=True)
    last_activity = Required(datetime, default=lambda: utcnow(), index=True)
    timeout_minutes = Required(int, default=60)  # max 40320 (4 weeks)
    max_yamls_per_player = Required(int, default=1)
    race = Required(bool, default=False)
    meta = Required(LongStr, default=lambda: "{}")  # generation settings (server_options, plando_options, etc.)
    state = Required(int, default=0, index=True)  # LOBBY_OPEN, LOBBY_GENERATING, LOBBY_DONE, LOBBY_CLOSED, LOBBY_LOCKED
    max_players = Required(int, default=0) # 0 = unlimited
    allow_custom_apworlds = Required(bool, default=False)
    seed = Optional('Seed')
    room = Optional(Room)
    players = Set('LobbyPlayer')
    messages = Set('LobbyMessage')
    yamls = Set('LobbyYaml')
    apworlds = Set('LobbyApworld')
    apworld_requests = Set('LobbyApworldRequest')
    generation_id = Optional(UUID)  # ID of the Generation/Seed (they share the same UUID)


class LobbyPlayer(db.Entity):
    id = PrimaryKey(int, auto=True)
    lobby = Required(Lobby, index=True)
    session_id = Required(UUID, index=True)
    player_name = Required(str)
    joined_at = Required(datetime, default=lambda: utcnow())
    is_ready = Required(bool, default=False)
    yamls = Set('LobbyYaml')
    messages = Set('LobbyMessage')
    apworld_requests = Set('LobbyApworldRequest')


class LobbyYaml(db.Entity):
    id = PrimaryKey(int, auto=True)
    lobby = Required(Lobby, index=True)
    player = Required(LobbyPlayer, index=True)
    filename = Required(str)
    yaml_player_name = Optional(str)  # resolved "name" field from the YAML
    yaml_game = Optional(str)  # resolved "game" field from the YAML
    is_custom = Required(bool, default=False)  # game not in AutoWorldRegister
    requires_game_version = Optional(str, nullable=True)  # JSON-encoded version constraint from requires.game
    content = Required(bytes, lazy=True)
    uploaded_at = Required(datetime, default=lambda: utcnow())
    apworld = Optional('LobbyApworld')
    apworld_requests = Set('LobbyApworldRequest')


class LobbyApworld(db.Entity):
    id = PrimaryKey(int, auto=True)
    lobby = Required(Lobby, index=True)
    yaml = Required(LobbyYaml)
    game_name = Required(str, index=True)
    original_filename = Required(str)
    storage_path = Required(str)
    file_size = Required(int, default=0)
    world_version = Optional(str, nullable=True) # extracted from archipelago.json in the apworld
    uploaded_at = Required(datetime, default=lambda: utcnow())


class LobbyApworldRequest(db.Entity):
    id = PrimaryKey(int, auto=True)
    lobby = Required(Lobby, index=True)
    yaml = Required(LobbyYaml, index=True)
    requester = Required(LobbyPlayer, index=True)
    game_name = Required(str, index=True)
    original_filename = Required(str)
    storage_path = Required(str)
    file_size = Required(int, default=0)
    world_version = Optional(str, nullable=True)
    submitted_at = Required(datetime, default=lambda: utcnow())


class LobbyMessage(db.Entity):
    id = PrimaryKey(int, auto=True)
    lobby = Required(Lobby, index=True)
    player = Optional(LobbyPlayer)  # null = system message
    sender_name = Required(str)
    content = Required(str)
    sent_at = Required(datetime, default=lambda: utcnow())
