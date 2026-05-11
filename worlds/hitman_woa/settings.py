import settings

class HitmanSettings(settings.Group):
    class PeacockUrl(str):
        """The url on which the Peacock-Server is running. Leave it as \"127.0.0.1\" if the server is hosted on the same machine as the client. You can also append a port if peacock isn't using its default one (ex.: \"127.0.0.1:80\")"""

    peacock_url: PeacockUrl = PeacockUrl("127.0.0.1")
