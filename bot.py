# 👉 Run "./connect" (or "connect.cmd" on Windows) in the terminal to get started

class Bot:
    def __init__(self, config):
        print("Hello World!", config)
        self.config = config

    def move(self, eastPaddle, westPaddle, ball):
        # Determine which paddle you control.
        paddle = eastPaddle if self.config["paddle"] == "east" else westPaddle

        # This prints the position of your paddle and the ball to the bot terminal.
        # Use these values to determine which direction your paddle should move so
        # you hit the ball!
        print("paddle", paddle["x"], paddle["y"])
        print("ball", ball["x"], ball["y"])

        # Return the direction you'd like to move here:
        # "north" "south" "east" "west" or "none"
        return "none"

    def end(self, eastPaddle, westPaddle, ball):
        print("Good game!")
