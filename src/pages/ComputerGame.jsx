import Particles from "../components/Particle";
import PlayerCard from "../components/PlayerCard";
import TicTacToeBoard from "../components/TicTacToeBoard";
import { IoMdArrowRoundBack } from "react-icons/io";
import { useNavigate } from "react-router";
import { useState } from "react";
import { FaStepForward } from "react-icons/fa";
import { FaStepBackward } from "react-icons/fa";
import { FaAngleLeft } from "react-icons/fa6";
import { FaAngleRight } from "react-icons/fa6";
import WinningModal from "../components/WinningModal";
import { MdReplay } from "react-icons/md";
import { resetGame } from "../api/gameAPI";
export default function computerGame() {
  const navigate = useNavigate();
  const [turn, setTurn] = useState("X");
  const params = new URLSearchParams(window.location.search);
  const rounds = params.get("rounds") || 1;
  const time = params.get("time") || 300;
  const side = params.get("side") || "X";
  const [score, setScore] = useState({ X: 0, O: 0 });
  const [winner, setWinner] = useState(null);
  const [gameKey, setGameKey] = useState(0);

  const onWin = (result) => {
    if (result === "AI won") result = side === "X" ? "O" : "X";
    if (result === "You won") result = side;
    setWinner(result);
    setScore((prev) => {
      if (result === "draw") return prev;
      return { ...prev, [result]: prev[result] + 1 };
    });
  };
  const handleComputerThinking = (thinking) => {
    setTurn(thinking ? (side === "X" ? "O" : "X") : side);
  };
  return (
    <div
      className="grid grid-cols-3 h-screen w-screen animated-gradient bg-gradient-to-br from-gray-900 via-gray-800 to-gray-500
 flex flex-col items-center justify-center text-white"
    >
      {winner && (
        <WinningModal
          winner={winner}
          score={score}
          rounds={rounds}
          onClose={() => {
            resetGame().then(() => {
              setWinner(null);
              setGameKey((k) => k + 1); // 👈 trigger board reset
            });
          }}
        />
      )}
      <div
        onClick={() => {
          navigate(-1);
        }}
        className="absolute cursor-pointer top-5 left-5 border-2 rounded-full w-12 h-12 flex items-center justify-center hover:bg-white hover:text-black"
      >
        <IoMdArrowRoundBack className="text-2xl hover:cursor-pointer" />
      </div>

      <Particles />
      <div className="col-span-2 flex-col border-r-2 h-full flex items-center justify-center">
        <PlayerCard
          playerName={"Computer"}
          playerSide={side === "X" ? "O" : "X"}
          timeLeft={time}
          playerSideActive={turn === (side === "X" ? "O" : "X")}
        />
        <TicTacToeBoard
          onWin={onWin}
          computer={true}
          side={side}
          handleComputerThinking={handleComputerThinking}
          key={gameKey}
        />
        <PlayerCard
          playerName={"Player"}
          playerSide={side}
          timeLeft={time}
          playerSideActive={turn === side}
        />
      </div>
      <div className="bg-gray-900 h-full">
        <h1 className="font-extrabold text-3xl mb-5 mt-10">
          Computer vs Player
        </h1>
        <p className="font-bold text-xl">Number of rounds: {rounds}</p>
        <p className="font-bold text-2xl mb-5">Score</p>
        <p className="font-bold text-5xl mb-10">
          <span className="text-[#646cff]">{score.X}</span> -{" "}
          <span className="text-[#ff6b6b]">{score.O}</span>
        </p>

        <p className="font-bold text-xl">Instructions:</p>
        <ul className="list-disc list-inside mt-2 text-left px-10">
          <li>
            You are "{side}" and computer is "{side === "X" ? "O" : "X"}".
          </li>
          <li>Take turns to place your marks on the board.</li>
          <li>
            The first player to align 4 marks horizontally, vertically, or
            diagonally wins.
          </li>
          <li>
            If the board is filled without a winner, the game ends in a draw.
          </li>
        </ul>
        <div className="flex gap-2 justify-center items-center mt-10">
          <button className=" bg-gray-700 rounded-md  hover:bg-gray-600 flex items-center justify-center hover:border-[#646cff] hover:border-2 transition-all duration-50">
            <FaStepBackward className="text-3xl hover:cursor-pointer" />
          </button>
          <button className=" bg-gray-700 rounded-md  hover:bg-gray-600 flex items-center justify-center hover:border-[#646cff] hover:border-2 transition-all duration-50">
            <FaAngleLeft className="text-3xl hover:cursor-pointer" />
          </button>
          <button
            onClick={() => {
              resetGame().then(() => {
                window.location.reload();
              });
            }}
            className=" bg-gray-700 rounded-md  hover:bg-gray-600 flex items-center justify-center hover:border-[#646cff] hover:border-2 transition-all duration-50"
          >
            <MdReplay className="text-3xl hover:cursor-pointer" />
          </button>
          <button className="bg-gray-700 rounded-md  hover:bg-gray-600 flex items-center justify-center hover:border-[#646cff] hover:border-2 transition-all duration-50">
            <FaAngleRight className="text-3xl hover:cursor-pointer" />
          </button>
          <button className="bg-gray-700 rounded-md  hover:bg-gray-600 flex items-center justify-center hover:border-[#646cff] hover:border-2 transition-all duration-50">
            <FaStepForward className="text-3xl hover:cursor-pointer" />
          </button>
        </div>
      </div>
    </div>
  );
}
