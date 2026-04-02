import sys








def getgame():
    return str(sys.argv[-1]) if len(sys.argv) > 1 else ""





if __name__ == "__main__":
    from .xgame import XGame
    game = getgame() 
    print(f"Selected game: {game}")  
    XGame(game=game)

