import os
import requests
import asyncio
import logging

logger = logging.getLogger("DisplayStyleEngine")

STYLE_PRESETS = [
    {"key": "sinistre-neon-white", "label": "Sinistre Neon White", "style": {"font_id": 10, "effect_id": 3, "colors": [16777215]}},
    {"key": "ribes-neon-pink", "label": "Ribes Neon Pink", "style": {"font_id": 9, "effect_id": 3, "colors": [16711935]}},
    {"key": "neo-castel-gradient-blue-white", "label": "Neo-Castel Blue/White Gradient", "style": {"font_id": 7, "effect_id": 2, "colors": [5865, 16777215]}},
    {"key": "pixelify-pop-purple", "label": "Pixelify Sans Pop Purple", "style": {"font_id": 8, "effect_id": 5, "colors": [8388736]}},
    {"key": "bangers-glow-pink-purple", "label": "Bangers Pink/Purple Glow", "style": {"font_id": 1, "effect_id": 6, "colors": [16711935, 8388736]}},
    {"key": "cherry-toon-white", "label": "Cherry Bomb Toon White", "style": {"font_id": 3, "effect_id": 4, "colors": [16777215]}},
    {"key": "zilla-solid-blue", "label": "Zilla Slab Solid Blue", "style": {"font_id": 12, "effect_id": 1, "colors": [5865]}}
]

class DiscordProfileAPI:
    def __init__(self, token, base_url="https://discord.com/api/v10"):
        self.token = token
        self.base_url = base_url

    def patch(self, endpoint, body):
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bot {self.token}",
            "User-Agent": "DiscordBot (https://discord.com, 1.0)",
            "Content-Type": "application/json"
        }
        try:
            response = requests.patch(url, json=body, headers=headers)
            return response
        except Exception as e:
            logger.error(f"Network Error: {e}")
            return None

class ProfileStyleService:
    def __init__(self, client, options=None):
        self.client = client
        self.token = os.getenv("TOKEN")
        self.api = DiscordProfileAPI(self.token)
        self.options = options or {}
        
    @staticmethod
    async def initialize(client, options=None):
        service = ProfileStyleService(client, options)
        await service.run()
        return {"endpointSupported": "YES"}

    async def run(self):
        mode = self.options.get("styleMode", "rotate")
        preset_key = self.options.get("stylePreset", "sinistre-neon-white")
        preset = next((p for p in STYLE_PRESETS if p["key"] == preset_key), STYLE_PRESETS[0])
        
        for guild in self.client.guilds:
            await self.apply_style(str(guild.id), self.client.user.name, preset["style"])

    async def apply_style(self, guild_id: str, name: str, style_dict: dict):
        payload = {
            "nick": name,
            "display_name_font_id": style_dict["font_id"],
            "display_name_effect_id": style_dict["effect_id"],
            "display_name_colors": style_dict["colors"]
        }
        loop = asyncio.get_event_loop()
        endpoint = f"/guilds/{guild_id}/members/@me"
        response = await loop.run_in_executor(None, lambda: self.api.patch(endpoint, payload))
        return response and response.status_code in [200, 201, 204]