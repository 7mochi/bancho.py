"""Discord utilities that use pycord (Thanks to nekoraw) """

import app.settings
import app.state.services
from app.objects.beatmap import Beatmap, BeatmapSet, RankedStatus
from app.objects.player import Player

from discord.colour import Colour
from discord import Webhook, Embed

import aiohttp


def create_beatmap_changes_embed(beatmap:Beatmap, new_status:RankedStatus) -> Embed:
    new_status_string = f"{new_status!s}"
    embed = Embed(title=f"New beatmap added to {new_status_string}:")
    embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{beatmap.set_id}l.jpg")
    star_rating = f"{int(beatmap.diff*100)/100}🌟"

    embed.add_field(
        name=f"{beatmap.artist} - {beatmap.title} [{beatmap.version}]",
        value=(f"**{star_rating}** - **CS** {beatmap.cs} - **AR** {beatmap.ar} - **BPM** {beatmap.bpm}\
        \n **Link:** https://osu.ppy.sh/beatmapsets/{beatmap.set_id}"),
        inline=False
    )

    return embed

def create_beatmapset_changes_embed(beatmapset:BeatmapSet, new_status:RankedStatus) -> Embed:
    new_status_string = f"{new_status!s}"
    embed = Embed(title=f"New beatmapset added to {new_status_string}:")
    embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{beatmapset.id}l.jpg")

    embed.add_field(
        name=f"{beatmapset.maps[0].artist} - {beatmapset.maps[0].title}",
        value=(f"**Difficulties: ** {len(beatmapset.maps)}\
        \n **Link:** https://osu.ppy.sh/beatmapsets/{beatmapset.id}"),
        inline=False
    )

    return embed

async def send_webhook(webhook_url:str, embed:Embed) -> None:
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        await webhook.send(embed=embed)


async def send_beatmap_status_change(webhook_url:str, beatmap:Beatmap, new_status:RankedStatus, player_info:Player) -> None:
    """Send new ranked status from the beatmap to discord."""
    embed = create_beatmap_changes_embed(beatmap, new_status)
    embed.set_footer(text=f"Nominator: {player_info.name}", icon_url=f"https://a.{app.settings.DOMAIN}/{player_info.id}")

    await send_webhook(webhook_url, embed)
    

async def send_beatmapset_status_change(webhook_url:str, beatmapset:BeatmapSet, new_status:RankedStatus, player_info:Player) -> None:
    """Send new ranked status from the beatmapset to discord."""
    embed = create_beatmapset_changes_embed(beatmapset, new_status)
    embed.set_footer(text=f"Nominator: {player_info.name}", icon_url=f"https://a.{app.settings.DOMAIN}/{player_info.id}")

    await send_webhook(webhook_url, embed)
    
