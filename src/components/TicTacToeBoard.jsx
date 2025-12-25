import { useState } from "react";
import Particles from "./Particle";

const checkWinner = (board, size = 5, winLength = 4) => {
  const directions = [
    [1, 0], // horizontal
    [0, 1], // vertical
    [1, 1], // diagonal down-right
    [1, -1], // diagonal up-right
  ];

  for (let row = 0; row < size; row++) {
    for (let col = 0; col < size; col++) {
      const index = row * size + col;
      const player = board[index];
      if (!player) continue;

      for (const [dx, dy] of directions) {
        let count = 1;

        for (let step = 1; step < winLength; step++) {
          const r = row + dy * step;
          const c = col + dx * step;

          if (r < 0 || r >= size || c < 0 || c >= size) break;
          if (board[r * size + c] !== player) break;

          count++;
        }

        if (count === winLength) {
          return player;
        }
      }
    }
  }

  return null;
};

const EvalBar = ({ board, isXTurn }) => {
  const testEval = 78; // 0–100

  return (
    <div className="flex flex-col h-full w-8">
      <div
        className="bg-[#646cff] text-white flex items-end justify-center"
        style={{ height: `${testEval}%` }}
      >
        {testEval / 100}
      </div>

      <div
        className="bg-[#ff6f91] text-black"
        style={{ height: `${100 - testEval}%` }}
      />
    </div>
  );
};
import { useNavigate } from "react-router";
export default function TicTacToeBoard({ onWin }) {
  const SIZE = 5;
  const [board, setBoard] = useState(Array(SIZE * SIZE).fill(null));
  const [isXTurn, setIsXTurn] = useState(true);
  const navigate = useNavigate();
  const handleClick = (index) => {
    if (board[index]) return;

    const newBoard = [...board];
    newBoard[index] = isXTurn ? "X" : "O";

    const winner = checkWinner(newBoard, SIZE, 4);

    setBoard(newBoard);

    if (winner) {
      handleWin(winner);
      return;
    }

    if (newBoard.every((cell) => cell !== null)) {
      handleWin("draw");
      return;
    }

    setIsXTurn(!isXTurn);
  };

  const handleWin = (winner) => {
    if (onWin) {
      onWin(winner);
    }
    setBoard(Array(SIZE * SIZE).fill(null));
    setIsXTurn(true);
  };
  return (
    <div style={styles.container}>
      <EvalBar board={board} isXTurn={isXTurn} />
      <div
        style={{
          ...styles.board,
          gridTemplateColumns: `repeat(${SIZE}, 80px)`,
          gridTemplateRows: `repeat(${SIZE}, 80px)`,
        }}
      >
        {board.map((cell, i) => (
          <div
            key={i}
            onClick={() => handleClick(i)}
            className={`cell ${cell ? "filled" : ""}`}
            style={{
              ...styles.cell,
              ...(cell === "X" ? styles.neonX : {}),
              ...(cell === "O" ? styles.neonO : {}),
            }}
          >
            {cell}
          </div>
        ))}
      </div>

      {/* Inline CSS for hover & neon */}
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
    color: "#ff4d4f",
    textShadow: `
      0 0 4px #ff4d4f,
      0 0 8px #ff4d4f,
      0 0 18px rgba(255, 77, 79, 0.8)
    `,
  },
  neonO: {
    color: "#646cff",
    textShadow: `
      0 0 4px #646cff,
      0 0 8px #646cff,
      0 0 18px rgba(100, 108, 255, 0.8)
    `,
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
`;
