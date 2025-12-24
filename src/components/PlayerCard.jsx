import { useEffect, useState } from "react";
import {
  LuClock12,
  LuClock1,
  LuClock2,
  LuClock3,
  LuClock4,
  LuClock5,
  LuClock6,
  LuClock7,
  LuClock8,
  LuClock9,
  LuClock10,
  LuClock11,
} from "react-icons/lu";

export default function PlayerCard({
  playerName,
  playerSide,
  timeLeft,
  playerSideActive,
}) {
  const [timer, setTimer] = useState(timeLeft);
  useEffect(() => {
    if (playerSideActive) {
      const interval = setInterval(() => {
        setTimer((prev) => (prev > 0 ? prev - 1 : 0));
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [playerSideActive]);
  return (
    <div className="p-5 text-center flex justify-between w-[80%] items-center">
      <div className="flex justify-center items-baseline gap-5">
        {playerSide === "X" ? (
          <div className="rounded-full p-1 border border-[#646cff] w-12 h-12 text-3xl text-[#646cff] font-extrabold justify-center">
            X
          </div>
        ) : (
          <div className="rounded-full p-1 border border-[#ff6f91] w-12 h-12 text-3xl text-[#ff6f91] font-extrabold flex items-center justify-center">
            O
          </div>
        )}

        <h2 className="text-2xl font-bold mb-2">{playerName}</h2>
      </div>
      <div
        className={
          "text-2xl  h-full px-3 rounded-md font-mono font-bold flex items-center w-40 justify-between " +
          (playerSideActive
            ? timer <= 30
              ? "bg-red-500 text-white"
              : "bg-white text-black"
            : "bg-gray-900 text-gray-400 justify-end")
        }
      >
        {playerSideActive &&
          (timer % 12 === 0 ? (
            <LuClock12 />
          ) : timer % 12 === 1 ? (
            <LuClock11 />
          ) : timer % 12 === 2 ? (
            <LuClock10 />
          ) : timer % 12 === 3 ? (
            <LuClock9 />
          ) : timer % 12 === 4 ? (
            <LuClock8 />
          ) : timer % 12 === 5 ? (
            <LuClock7 />
          ) : timer % 12 === 6 ? (
            <LuClock6 />
          ) : timer % 12 === 7 ? (
            <LuClock5 />
          ) : timer % 12 === 8 ? (
            <LuClock4 />
          ) : timer % 12 === 9 ? (
            <LuClock3 />
          ) : timer % 12 === 10 ? (
            <LuClock2 />
          ) : (
            <LuClock1 />
          ))}
        <p>
          {Math.floor(timer / 60)}:
          {timer % 60 < 10 ? `0${timer % 60}` : timer % 60}{" "}
        </p>
      </div>
    </div>
  );
}
