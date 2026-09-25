
import os
import sys

sys.path.append(os.path.abspath("."))
from backend.services.agent_services.tools_calls import (
    get_temperature,
    get_persons_registered,
    get_home_status,
    get_humidity,
    get_music_played,
    get_light_status,
    turn_on_light,
    turn_off_light,
    play_music,
    get_luminosity
)


TOOL_FUNCTIONS = {
    "get_temperature": get_temperature.get_temperature,
    "get_persons_registered":  get_persons_registered.get_persons_registered,
    "get_home_status": get_home_status.get_home_status,
    "get_humidity": get_humidity.get_humidity,
    "get_music_played": get_music_played.get_music_played,
    "get_light_status": get_light_status.get_light_status,
    "turn_on_light": turn_on_light.turn_on_light,
    "turn_off_light": turn_off_light.turn_off_light,
    "play_music": play_music.play_music,
    "get_luminosity": get_luminosity.get_luminosity
}