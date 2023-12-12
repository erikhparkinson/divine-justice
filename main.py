import sys
from bot import Bot

def send(channel: str, *args):
    bot_instance_id = args[0] if len(args) > 0 else None
    payload = args[1] if len(args) > 1 else None

    message = "\n<<zilch>>." + channel

    if bot_instance_id is not None:
        message += "." + bot_instance_id

    if payload is not None:
        message += "." + payload

    message += "\n"

    print(message, end="", file=sys.stderr)

def parse_payload(payload):
    parts = payload.split(",")
    return [
        {
            "x": float(parts[0]),
            "y": float(parts[1])
        },
        {
            "x": float(parts[2]),
            "y": float(parts[3])
        },
        {
            "x": float(parts[4]),
            "y": float(parts[5])
        }
    ]

send("ready")

bots: "dict[str, Bot]" = dict([])

while True:
    data = sys.stdin.readline().strip()
    channel, bot_instance_id, payload = data.split(".", 2)

    if channel == "start":
        standard_config, custom_config = payload.split(".", 1)
        game_time_limit, turn_time_limit, player = standard_config.split(",", 2)
        config = {
            "bot_instance_id": bot_instance_id,
            "game_time_limit": int(game_time_limit),
            "turn_time_limit": int(turn_time_limit),
            "paddle": "east" if player == "0" else "west"
        }
        bots[bot_instance_id] = Bot(config)
        send("start", bot_instance_id)
        continue

    if channel == "move":
        bot = bots[bot_instance_id]
        move = bot.move(*parse_payload(payload))
        send("move", bot_instance_id, move)
        continue

    if channel == "end":
        bot = bots[bot_instance_id]
        bot.end(*parse_payload(payload))
        bots.pop(bot_instance_id)
        continue
