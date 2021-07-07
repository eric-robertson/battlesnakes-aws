import os

import cherrypy

import server_logic

class BattlesnakeServer(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        """
        This function is called when you register your Battlesnake on play.battlesnake.com
        See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake

        It controls your Battlesnake appearance and author permissions.
        For customization options, see https://docs.battlesnake.com/references/personalization
        
        TIP: If you open your Battlesnake URL in browser you should see this data.
        """
        return {
            "apiversion": "1",
            "author": "hmmoro",
            "color": "#777777",
            "secondary_color": "f5a422",
            "head": "default",
            "tail": "default",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        """
        Called everytime Robeworm is entered into a game.
        """
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        """
        Called on every turn of a game.
        Valid moves are "up", "down", "left", or "right".
        """
        data = cherrypy.request.json

        # TODO - look at the server_logic.py file to see how we decide what move to return!
        move = server_logic.choose_move(data)

        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        """
        This function is called when a game your snake was in ends.
        It's purely for informational purposes, you don't have to make any decisions here.
        """
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = BattlesnakeServer()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)