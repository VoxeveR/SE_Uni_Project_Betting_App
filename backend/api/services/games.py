from api.database.models.betsgames import BetsGames
from api.database.models.games import Games, GameStatus
from api.database.models.odds import Odds
from api.database.models.gameReslut import GameResult
from typing_extensions import Optional
from sqlalchemy.orm import Session
from api.core.logging import logger
from collections import defaultdict

from api.schemas.games import (
    NewGame,
    GameUpdate,
    Result,
)


def checkGameExistByDict(games: dict, db: Session) -> bool:
    for game_id in games.keys():
        game = db.query(Games).filter(Games.game_id == int(game_id)).first()
        if not game:
            return False
    return True


def checkGameExistById(game_id: int, db: Session) -> bool:
    game = db.query(Games).filter(Games.game_id == int(game_id)).first()

    return True if not game else False


def checkGameExistsByHomeAway(home: str, away: str, event_name: str, db: Session) -> bool:
    game = db.query(Games).filter(Games.home == home and Games.away == away and  Games.event_name == event_name).first()

    return True if not game else False

def checkGameHaveBets(game_id: int, db: Session) -> bool:
    games = db.query(BetsGames).filter(BetsGames.game_id == game_id).all()

    return True if games else False

def checkGameNotPlaying(game_id: int, db: Session) -> bool:
    game = db.query(Games).filter(Games.game_id == game_id).first()

    return True if game.game_status != GameStatus.PLAYING else False

def get_games_categories(db: Session) -> Optional[defaultdict]:
    try:
        result = db.query(Games.sport_type, Games.event_name).filter(Games.game_status != GameStatus.FINISHED).all()

        categories = defaultdict(set)

        for sport_type, event_name in result:
            categories[sport_type].add(event_name)

        return categories
    except Exception as e:
        logger.error(e)
        return None


def get_games_by_event_name(event_name: str, db: Session) -> Optional[dict]:
    try:
        result = db.query(Games.game_id, Games.home, Games.away, Games.start_time, Games.game_status, Odds.odds, Odds.odds_type).join(Odds).filter((Games.event_name == event_name) & (Games.game_status != GameStatus.FINISHED)).all()

        grouped_games = {}

        for game_id, home, away, start_time, game_status, odds, odds_type in result:

            if game_id not in grouped_games:
                grouped_games[game_id] = {
                    'home': home,
                    'away': away,
                    'start_time': start_time.time(),
                    'start_date': start_time.date(),
                    'game_status': game_status,
                    'odds1': None,
                    'oddsX': None,
                    'odds2': None
                }

            if odds_type == GameResult.One:
                grouped_games[game_id]['odds1'] = odds
            elif odds_type == GameResult.Two:
                grouped_games[game_id]['odds2'] = odds
            elif odds_type == GameResult.X:
                grouped_games[game_id]['oddsX'] = odds

        return grouped_games

    except Exception as e:
        logger.error(e)
        return None


def add_new_game(newGame: NewGame, db: Session) -> bool:
    try:
        print(newGame)
        game = Games(
            home=newGame.home,
            away=newGame.away,
            event_name=newGame.event_name,
            start_time=newGame.start_time,
            game_status=GameStatus.BEFORE,
            sport_type=newGame.sport_type,
        )

        db.add(game)
        db.flush()

        oddsOne = Odds(
            game_id=game.game_id,
            odds_type=GameResult.One,
            odds=newGame.odds1,
        )

        db.add(oddsOne)

        oddsTwo = Odds(
            game_id=game.game_id,
            odds_type=GameResult.Two,
            odds=newGame.odds2,
        )

        db.add(oddsTwo)

        if newGame.oddsX:
            oddsX = Odds(
                game_id=game.game_id,
                odds_type=GameResult.X,
                odds=newGame.oddsX,
            )
            db.add(oddsX)

        db.commit()

        return True
    except Exception as e:
        logger.error(e)
        db.rollback()
        return False


def update_game_by_id(game_id: int, game_update: GameUpdate, db: Session) -> bool:
    try:
        game = db.query(Games).filter(Games.game_id == game_id).first()

        for key, value in game_update.dict(exclude_unset=True).items():
            if value is not None:
                setattr(game, key, value)

        db.commit()

        return True
    except Exception as e:
        logger.error(e)
        db.rollback()
        return False

def delete_game(game_id: int, db: Session) -> bool:
    try:
        db.query(Odds).filter(Odds.game_id == game_id).delete()
        db.flush()

        db.query(Games).filter(Games.game_id == game_id).delete()
        db.commit()

        return True
    except Exception as e:
        logger.error(e)
        db.rollback()
        return False

def set_game_result(game_id: int, game_result: Result, db: Session) -> bool:
    try:
        db.query(Games).filter(Games.game_id == game_id).update(
            {Games.game_result: game_result.result, Games.game_status: GameStatus.FINISHED}
        )

        db.commit()

        return True
    except Exception as e:
        logger.error(e)
        db.rollback()
        return False