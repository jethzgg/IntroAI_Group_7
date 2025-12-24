import { useNavigate } from "react-router";
import Particles from "../components/Particle";
import { useState } from "react";
import { IoMdArrowRoundBack } from "react-icons/io";

export default function WithPlayer() {
  const [timeMinute, setTimeMinute] = useState(5);
  const [timeSecond, setTimeSecond] = useState(0);
  const [selectedRounds, setSelectedRounds] = useState(1);
  const navigate = useNavigate();
  return (
    <div
      className="h-screen w-screen animated-gradient bg-gradient-to-br from-gray-900 via-gray-800 to-gray-500
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
      <h1 className="font-extrabold">Game setup</h1>
      <p className="font-bold text-xl my-5">Number of rounds:</p>
      <div className="gap-5 flex-row w-screen">
        <button
          className={
            "hover:shadow-lg hover:shadow-[#646cff]" +
            (selectedRounds === 1
              ? " shadow-lg shadow-[#646cff] border-[#646cff] border-2"
              : "")
          }
          onClick={() => {
            setSelectedRounds(1);
          }}
        >
          1
        </button>
        <button
          className={
            "hover:shadow-lg hover:shadow-[#646cff] ml-5" +
            (selectedRounds === 3
              ? " shadow-lg shadow-[#646cff] border-[#646cff] border-2"
              : "")
          }
          onClick={() => {
            setSelectedRounds(3);
          }}
        >
          3
        </button>
        <button
          className={
            "hover:shadow-lg hover:shadow-[#646cff] ml-5" +
            (selectedRounds === 5
              ? " shadow-lg shadow-[#646cff] border-[#646cff] border-2"
              : "")
          }
          onClick={() => {
            setSelectedRounds(5);
          }}
        >
          5
        </button>
      </div>
      <p className="font-bold text-xl my-5">Total time for each person:</p>
      <div className="gap-5 flex-row w-screen">
        <button
          className="hover:shadow-lg hover:shadow-[#646cff]"
          onClick={() => {
            //add Time by 30 sec
            const time = timeMinute * 60 + parseInt(timeSecond) + 30;
            setTimeMinute(Math.floor(time / 60));
            setTimeSecond(time % 60);
          }}
        >
          +
        </button>
        <input
          type="text"
          className="w-16 text-lg h-full text-center bg-gray-900 rounded mx-2"
          value={timeMinute}
          onChange={(e) => {
            setTimeMinute(e.target.value);
          }}
        />
        <span className="mx-2">:</span>
        <input
          type="text"
          className="w-16 text-lg h-full text-center bg-gray-900 rounded mx-2"
          value={timeSecond}
          onChange={(e) => {
            setTimeSecond(e.target.value);
          }}
        />
        <button
          onClick={() => {
            const time = timeMinute * 60 + parseInt(timeSecond) - 30;
            setTimeMinute(Math.floor(time / 60));
            setTimeSecond(time % 60);
          }}
          className="hover:shadow-lg hover:shadow-[#646cff]"
        >
          -
        </button>
      </div>
      <button
        onClick={() => {
          navigate(
            `/playerGame?rounds=${selectedRounds}&time=${
              timeMinute * 60 + parseInt(timeSecond)
            }`
          );
        }}
        className="mt-4 px-4 py-2 bg-blue-600 rounded hover:shadow-lg hover:shadow-[#646cff]"
      >
        Start Game
      </button>
    </div>
  );
}
