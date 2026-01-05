import { useEffect, useState } from "react";
import { getEvalPVP, getBestMove } from "../api/gameAPI";
const EvalBar = ({ board, side, showEval }) => {
  const [evalData, setEvalData] = useState(null);

  useEffect(() => {
    if (!showEval || !board) return;

    getEvalPVP(board)
      .then((data) => setEvalData(data.score))
      .catch(console.error);
  }, [board, showEval]);

  if (!showEval || evalData === null) return null;

  const SCALE = 100_000;
  const scaled = Math.tanh(evalData / SCALE); // [-1, 1]
  const topHeight = 50 + scaled * 50;
  const bottomHeight = 100 - topHeight;

  return (
    <div className="flex flex-col h-full w-8 overflow-hidden">
      <div
        className={`${
          side === "X" ? "bg-[#646cff]" : "bg-[#ff4d4f]"
        } transition-[height] duration-500 ease-out`}
        style={{ height: `${side === "X" ? topHeight : bottomHeight}%` }}
      />
      <div
        className={`${
          side === "X" ? "bg-[#ff4d4f]" : "bg-[#646cff]"
        } text-white flex items-end justify-center
           transition-[height] duration-500 ease-out`}
        style={{ height: `${side === "X" ? bottomHeight : topHeight}%` }}
      >
        {(evalData / 100).toFixed(2)}
      </div>
    </div>
  );
};

const SIZE = 5;

const flattenBoard = (board2D) => board2D.flat();
const createEmptyBoard = () =>
  Array.from({ length: SIZE }, () => Array(SIZE).fill("_"));
const checkWin = (board, player) => {
  const WIN_LENGTH = 4;
  const dirs = [
    [0, 1], // →
    [1, 0], // ↓
    [1, 1], // ↘
    [1, -1], // ↙
  ];

  for (let r = 0; r < SIZE; r++) {
    for (let c = 0; c < SIZE; c++) {
      if (board[r][c] !== player) continue;

      for (const [dr, dc] of dirs) {
        let count = 0;
        let rr = r,
          cc = c;

        while (
          rr >= 0 &&
          rr < SIZE &&
          cc >= 0 &&
          cc < SIZE &&
          board[rr][cc] === player
        ) {
          count++;
          if (count === WIN_LENGTH) return true;
          rr += dr;
          cc += dc;
        }
      }
    }
  }
  return false;
};

const isDraw = (board) =>
  board.every((row) => row.every((cell) => cell !== "_"));

export default function PVPBoard({
  onWin,
  side = "X",
  showEval = false,
  showBestMove = false,
}) {
  const [game, setGame] = useState({
    board: createEmptyBoard(),
    game_over: false,
  });
  const [turn, setTurn] = useState(side);
  const [bestMove, setBestMove] = useState(null);

  useEffect(() => {
    if (!showBestMove || !game || game.game_over) return;

    getBestMove(game.board)
      .then((data) => {
        setBestMove(data);
      }) // { row, col }
      .catch(console.error);
  }, [game, showBestMove]);

  // Handle click
  const handleClick = (index) => {
    if (game.game_over) return;

    const row = Math.floor(index / SIZE);
    const col = index % SIZE;

    if (game.board[row][col] !== "_") return;
    let message = null;

    setGame((prev) => {
      const newBoard = prev.board.map((r) => r.slice());
      newBoard[row][col] = turn;

      let game_over = false;

      if (checkWin(newBoard, turn)) {
        game_over = true;
        message = `${turn}`;
        return {
          board: createEmptyBoard(),
          game_over: false,
        };
      } else if (isDraw(newBoard)) {
        game_over = true;
        message = "draw";
        return {
          board: createEmptyBoard(),
          game_over: false,
        };
      }
      return {
        ...prev,
        board: newBoard,
        game_over,
        message,
      };
    });
    if (message) {
      onWin(message);
      setTurn("X");
      return;
    }
    setBestMove(null);

    setTurn((t) => (t === "X" ? "O" : "X"));
  };

  if (!game) return <p>Loading...</p>;

  const board = flattenBoard(game.board);

  return (
    <div style={styles.container}>
      <EvalBar board={game.board} side={side} showEval={showEval} />

      <div
        style={{
          ...styles.board,
          gridTemplateColumns: `repeat(${SIZE}, 80px)`,
          gridTemplateRows: `repeat(${SIZE}, 80px)`,
        }}
      >
        {board.map((cell, i) => {
          const isBestMove =
            showBestMove &&
            bestMove &&
            i === bestMove.row * SIZE + bestMove.col;
          if (isBestMove) {
            console.log("Found bestMove:", i);
          }

          return (
            <div
              key={i}
              onClick={() => handleClick(i)}
              className={`cell ${cell !== "_" ? "filled" : ""}`}
              style={{
                ...styles.cell,
                ...(cell === "X" ? styles.neonX : {}),
                ...(cell === "O" ? styles.neonO : {}),
                ...(isBestMove ? styles.bestMove : {}),
                cursor:
                  cell !== "_" || game.game_over ? "not-allowed" : "pointer",
              }}
            >
              {cell == "_" ? "" : cell}
            </div>
          );
        })}
      </div>

      <style>{css}</style>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    marginTop: "40px",
    gap: "50px",
  },
  board: {
    display: "grid",
    gap: "8px",
  },
  cell: {
    background: "#0f0f1a",
    borderRadius: "12px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "2.6rem",
    fontWeight: "900",
    cursor: "pointer",
    userSelect: "none",
    transition: "transform 0.15s ease, box-shadow 0.15s ease",
  },
  neonX: {
    color: "#646cff",
    textShadow: `
      0 0 4px #646cff,
      0 0 8px #646cff,
      0 0 18px rgba(100, 108, 255, 0.8)
    `,
  },
  neonO: {
    color: "#ff4d4f",
    textShadow: `
      0 0 4px #ff4d4f,
      0 0 8px #ff4d4f,
      0 0 18px rgba(255, 77, 79, 0.8)
    `,
  },
  bestMove: {
    boxShadow: `
    0 0 12px rgba(0, 255, 150, 0.9),
    inset 0 0 10px rgba(0, 255, 150, 0.4) 
  `,
    animation: "pulse 1.5s infinite",
  },
};

const css = `
.cell:hover:not(.filled) {
  transform: scale(1.08);
  box-shadow:
    0 0 12px rgba(255, 255, 255, 0.15),
    inset 0 0 8px rgba(255, 255, 255, 0.1);
}

.cell:active:not(.filled) {
  transform: scale(0.95);
}

.filled {
  cursor: not-allowed;
}
  @keyframes pulse {
  0% { box-shadow: 0 0 8px rgba(0,255,150,0.5); }
  50% { box-shadow: 0 0 16px rgba(0,255,150,1); }
  100% { box-shadow: 0 0 8px rgba(0,255,150,0.5); }
}

`;
