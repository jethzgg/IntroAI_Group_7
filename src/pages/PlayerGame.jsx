import Particles from "../components/Particle";
import PlayerCard from "../components/PlayerCard";
import TicTacToeBoard from "../components/TicTacToeBoard";
import { IoMdArrowRoundBack } from "react-icons/io";
import { useNavigate } from "react-router";
import { useState } from "react";
export default function PlayerGame() {
  const navigate = useNavigate();
  const [turn, setTurn] = useState("X");
  return (
    <div
      className="grid grid-cols-3 h-screen w-screen animated-gradient bg-gradient-to-br from-gray-900 via-gray-800 to-gray-500
 flex flex-col items-center justify-center text-white"
    >
      <div className="absolute top-5 left-5 border-2 rounded-full w-12 h-12 flex items-center justify-center hover:bg-white hover:text-black">
        <IoMdArrowRoundBack
          className="text-2xl hover:cursor-pointer"
          onClick={() => {
            navigate(-1);
          }}
        />
      </div>

      <Particles />
      <div className="col-span-2 flex-col border-r-2 h-full flex items-center justify-center">
        <PlayerCard
          playerName={"Player 1"}
          playerSide={"X"}
          timeLeft={300}
          playerSideActive={turn === "X"}
        />
        <TicTacToeBoard />
        <PlayerCard
          playerName={"Player 2"}
          playerSide={"O"}
          timeLeft={300}
          playerSideActive={turn === "O"}
        />
      </div>
      <div className="bg-gray-900 h-full">
        <h1 className="font-extrabold text-3xl mb-5">Player vs Player</h1>
        <p className="font-bold text-xl">Instructions:</p>
        <ul className="list-disc list-inside mt-2 text-left px-10">
          <li>Player 1 is "X" and Player 2 is "O".</li>
          <li>Take turns to place your marks on the board.</li>
          <li>
            The first player to align 4 marks horizontally, vertically, or
            diagonally wins.
          </li>
          <li>
            If the board is filled without a winner, the game ends in a draw.
          </li>
        </ul>
      </div>
    </div>
  );
}
