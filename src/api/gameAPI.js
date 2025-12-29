const API_BASE = "http://localhost:8000/api";

/**
 * Start a new game
 * @param {"X" | "O"} player
 */
export async function startGame(player) {
  const res = await fetch(`${API_BASE}/start`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ player }),
  });

  if (!res.ok) {
    throw new Error("Failed to start game");
  }

  return res.json();
}

/**
 * Make a move
 * @param {number} row
 * @param {number} col
 */
export async function makeMove(row, col) {
  const res = await fetch(`${API_BASE}/move`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ row, col }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Invalid move");
  }

  return res.json();
}

/**
 * Get current game state
 */
export async function getGameStatus() {
  const res = await fetch(`${API_BASE}/status`);

  if (!res.ok) {
    throw new Error("Failed to get game status");
  }

  return res.json();
}

/**
 * Reset game
 */
export async function resetGame() {
  const res = await fetch(`${API_BASE}/reset`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to reset game");
  }

  return res.json();
}
export async function getEval() {
  const res = await fetch(`${API_BASE}/get_score`, {
    method: "POST",
  });
  if (!res.ok) {
    throw new Error("Failed to get evaluation");
  }
  return res.json();
}
