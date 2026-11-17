#!/usr/bin/env python3

import os
import sys
import threading
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_DIR / ".venv" / "bin" / "python"
if VENV_PYTHON.exists():
    sys.path.insert(0, str(PROJECT_DIR))
    if os.path.realpath(sys.prefix) != os.path.realpath(VENV_PYTHON.parent.parent):
        os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]])

import chess
import engine


ENGINE_NAME = "Bobby Chess"
# SEARCH_DEPTH = 3  # engine.makeMove() currently searches a fixed depth of three.
OUTPUT_LOCK = threading.Lock()
board = chess.Board()
active_search = None


def send(message):
    with OUTPUT_LOCK:
        print(message, flush=True)


def report_error(message):
    send("info string error " + message)


def set_position(command):
    global board

    fields = command.split()
    if len(fields) < 2 or fields[0] != "position":
        raise ValueError("malformed position command")

    if fields[1] == "startpos":
        candidate = chess.Board()
        move_index = 2
    elif fields[1] == "fen":
        try:
            moves_index = fields.index("moves", 2)
        except ValueError:
            moves_index = len(fields)
        fen = " ".join(fields[2:moves_index])
        if not fen:
            raise ValueError("position fen requires a FEN")
        candidate = chess.Board(fen)
        move_index = moves_index
    else:
        raise ValueError("position must use startpos or fen")

    if move_index < len(fields):
        if fields[move_index] != "moves":
            raise ValueError("expected moves after the position")
        for move_text in fields[move_index + 1:]:
            candidate.push_uci(move_text)

    board = candidate


def parse_searchmoves(tokens, position):
    allowed = []
    for token in tokens:
        try:
            move = position.parse_uci(token)
        except ValueError:
            continue
        if move not in allowed:
            allowed.append(move)
    return allowed


def start_search(command):
    global active_search

    stop_search(wait=True)
    position = board.copy(stack=True)
    tokens = command.split()[1:]
    controls = {
        "wtime", "btime", "winc", "binc", "movestogo", "depth",
        "nodes", "mate", "movetime", "infinite", "ponder", "searchmoves",
    }
    searchmoves = None
    collecting_searchmoves = False
    for token in tokens:
        if token in controls:
            collecting_searchmoves = token == "searchmoves"
            if collecting_searchmoves:
                searchmoves = []
        elif collecting_searchmoves:
            searchmoves.append(token)

    allowed_moves = (
        parse_searchmoves(searchmoves, position)
        if searchmoves is not None else None
    )
    defer_output = "infinite" in tokens or "ponder" in tokens
    if any(token in tokens for token in {
        "wtime", "btime", "winc", "binc", "movestogo", "depth",
        "nodes", "mate", "movetime",
    }):
        send("info string engine.makeMove() uses a fixed search depth of 3")
    release = threading.Event()
    suppress_output = threading.Event()

    def search():
        legal_moves = list(position.legal_moves)
        if not legal_moves:
            best_move = "0000"
        elif allowed_moves is not None and not allowed_moves:
            best_move = "0000"
        else:
            try:
                searched_position = position.copy(stack=True)
                engine.makeMove(searched_position)
                selected_move = searched_position.peek()
                if allowed_moves is not None and selected_move not in allowed_moves:
                    selected_move = allowed_moves[0]
                best_move = selected_move.uci()
            except Exception as error:
                report_error("search failed: " + str(error))
                best_move = (allowed_moves or legal_moves)[0].uci()

        if defer_output and best_move != "0000":
            release.wait()
        if not suppress_output.is_set():
            send("info depth " + str(1 if best_move != "0000" else 0)) ## Depth is chosen by engine dynamically
            send("bestmove " + best_move)

    thread = threading.Thread(target=search, name="uci-search", daemon=True)
    active_search = {
        "thread": thread,
        "release": release,
        "suppress": suppress_output,
    }
    thread.start()


def stop_search(wait=False, suppress_output=False):
    global active_search

    if active_search is None:
        return
    active_search["release"].set()
    if suppress_output:
        active_search["suppress"].set()
    thread = active_search["thread"]
    if wait:
        thread.join()
        if active_search is not None and active_search["thread"] is thread:
            active_search = None


def main():
    global board

    for raw_command in sys.stdin:
        command = raw_command.strip()
        if not command:
            continue

        fields = command.split()
        keyword = fields[0]

        if keyword == "uci":
            send("id name " + ENGINE_NAME)
            send("id author 2040pi")
            send("uciok")
        elif keyword == "isready":
            send("readyok")
        elif keyword == "setoption":
            # The current search implementation exposes no configurable options.
            continue
        elif keyword == "ucinewgame":
            stop_search(wait=True)
            board = chess.Board()
        elif keyword == "position":
            stop_search(wait=True)
            try:
                set_position(command)
            except (ValueError, IndexError) as error:
                report_error("invalid position: " + str(error))
        elif keyword == "go":
            start_search(command)
        elif keyword == "stop":
            stop_search(wait=True)
        elif keyword == "ponderhit":
            if active_search is not None:
                active_search["release"].set()
        elif keyword == "debug":
            continue
        elif keyword == "register":
            send("registration ok")
        elif keyword == "quit":
            stop_search(wait=True, suppress_output=True)
            return

    stop_search(wait=True)


if __name__ == "__main__":
    main()
