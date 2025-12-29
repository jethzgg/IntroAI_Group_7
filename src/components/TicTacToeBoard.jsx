import { useEffect, useState } from "react";
import { getEval } from "../api/gameAPI";

const EvalBar = ({ game, side }) => {
  const [evalData, setEvalData] = useState(null);

  useEffect(() => {
    if (!game || game.game_over) return;

    getEval()
      .then((data) => {
        setEvalData(data.score);
      })
      .catch(console.error);
  }, [game]);

  if (evalData === null) return null;

  const SCALE = 100_000;
  const scaled = Math.tanh(evalData / SCALE); // [-1, 1]
  const topHeight = 50 + scaled * 50;
  const bottomHeight = 100 - topHeight;

  return (
    <div className="flex flex-col h-full w-8 overflow-hidden">
      <div
        className={`${
          side === "X" ? "bg-[#ff4d4f]" : "bg-[#646cff]"
        } text-white flex items-end justify-center
           transition-[height] duration-500 ease-out`}
        style={{ height: `${side === "X" ? bottomHeight : topHeight}%` }}
      >
        {(evalData / 100).toFixed(2)}
      </div>

      <div
        className={`${
          side === "X" ? "bg-[#646cff]" : "bg-[#ff4d4f]"
        } transition-[height] duration-500 ease-out`}
        style={{ height: `${side === "X" ? topHeight : bottomHeight}%` }}
      />
    </div>
  );
};

import { startGame, makeMove, getGameStatus } from "../api/gameAPI";
const SIZE = 5;

const flattenBoard = (board2D) => board2D.flat();

export default function TicTacToeBoard({
  onWin,
  computer = true,
  side = "X",
  handleComputerThinking,
}) {
  const [game, setGame] = useState(null);
  const [turn, setTurn] = useState(side);
  // 🔹 Start game
  useEffect(() => {
    if (!computer) return;

    startGame(side)
      .then(() => getGameStatus())
      .then(setGame)
      .catch(console.error);
  }, []);

  // Handle click
  const handleClick = async (index) => {
    if (!game || game.game_over || turn !== side) return;

    const row = Math.floor(index / SIZE);
    const col = index % SIZE;

    try {
      // Change X first in local state for responsiveness
      setGame((prev) => {
        const newBoard = prev.board.map((r) => r.slice());
        newBoard[row][col] = "X";
        return { ...prev, board: newBoard };
      });
      setTurn(side === "X" ? "O" : "X");
      handleComputerThinking && handleComputerThinking(true);
      const updated = await makeMove(row, col);
      handleComputerThinking && handleComputerThinking(false);
      setGame(updated);
      setTurn(side);
      if (updated.game_over) {
        handleWin(updated.message);
      }
    } catch (err) {
      alert(err.message);
    }
  };

  const handleWin = (result) => {
    console.log("Game over:", result);
    if (onWin) onWin(result);
  };

  if (!game) return <p>Loading...</p>;

  const board = flattenBoard(game.board);

  return (
    <div style={styles.container}>
      <EvalBar game={game} side={side} />

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
            className={`cell ${cell !== "_" ? "filled" : ""}`}
            style={{
              ...styles.cell,
              ...(cell === "X" ? styles.neonX : {}),
              ...(cell === "O" ? styles.neonO : {}),
              cursor:
                cell !== "_" || game.game_over || turn !== side
                  ? "not-allowed"
                  : "pointer",
            }}
          >
            {cell == "_" ? "" : cell}
          </div>
        ))}
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
