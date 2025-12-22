from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tictactoe as ttt
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game state
game_state = {
    "board": ttt.initialState(),
    "user": None,
    "game_over": False
}

class StartGameRequest(BaseModel):
    player: str

class MoveRequest(BaseModel):
    row: int
    col: int

class GameState(BaseModel):
    board: list
    user: str
    game_over: bool
    message: str

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("index.html")

@app.post("/api/start")
async def start_game(request: StartGameRequest):
    """Start a new game"""
    player = request.player
    if player not in [ttt.X, ttt.O]:
        raise HTTPException(status_code=400, detail="Invalid player")
    
    game_state["board"] = ttt.initialState()
    game_state["user"] = player
    game_state["game_over"] = False
    
    return {"status": "success", "message": f"Game started. You are {player}"}

@app.post("/api/move")
async def make_move(request: MoveRequest):
    """Make a player move"""
    row, col = request.row, request.col
    
    if game_state["game_over"]:
        raise HTTPException(status_code=400, detail="Game is over")
    
    if not (0 <= row < ttt.N and 0 <= col < ttt.N):
        raise HTTPException(status_code=400, detail="Invalid position")
    
    if game_state["board"][row][col] != ttt.EMPTY:
        raise HTTPException(status_code=400, detail="Cell already occupied")
    
    # Check if it's player's turn
    current_player = ttt.whoseTurn(game_state["board"])
    if current_player != game_state["user"]:
        raise HTTPException(status_code=400, detail="Not your turn")
    
    # Make player move
    game_state["board"][row][col] = game_state["user"]
    ttt.lastX, ttt.lastY = row, col
    
    # Check if player won or game is over
    if ttt.isTerminal(game_state["board"]):
        game_state["game_over"] = True
        return build_game_status()
    
    # AI move
    ai_player = ttt.O if game_state["user"] == ttt.X else ttt.X
    ai_row, ai_col = ttt.bestMove(game_state["board"])
    game_state["board"][ai_row][ai_col] = ai_player
    ttt.lastX, ttt.lastY = ai_row, ai_col
    
    # Check if AI won or game is over
    if ttt.isTerminal(game_state["board"]):
        game_state["game_over"] = True
    
    return build_game_status()

def build_game_status():
    """Build the current game status"""
    board = game_state["board"]
    game_over = game_state["game_over"]
    
    message = ""
    if not game_over:
        current_player = ttt.whoseTurn(board)
        if current_player == game_state["user"]:
            message = "Lượt của bạn"
        else:
            message = "AI đang suy nghĩ..."
    else:
        if ttt.winner(board, game_state["user"]):
            message = "You win"
        elif ttt.winner(board, ttt.O if game_state["user"] == ttt.X else ttt.X):
            message = "AI wins"
        else:
            message = "Tie"
    
    return GameState(
        board=board,
        user=game_state["user"],
        game_over=game_over,
        message=message
    )

@app.get("/api/status")
async def get_game_status():
    """Get current game status"""
    return build_game_status()

@app.post("/api/reset")
async def reset_game():
    """Reset the game"""
    game_state["board"] = ttt.initialState()
    game_state["user"] = None
    game_state["game_over"] = False
    
    return {"status": "success", "message": "Game reset"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
