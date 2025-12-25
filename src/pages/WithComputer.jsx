import { useNavigate } from "react-router";
import Particles from "../components/Particle";
import { useState } from "react";
import { IoMdArrowRoundBack } from "react-icons/io";
export default function WithComputer() {
  const [timeMinute, setTimeMinute] = useState(5);
  const [timeSecond, setTimeSecond] = useState(0);
  const [selectedRounds, setSelectedRounds] = useState(1);
  const [sideChosen, setSideChosen] = useState("X");
  const navigate = useNavigate();
  return (
    <div
      className="h-screen w-screen animated-gradient bg-gradient-to-br from-gray-900 via-gray-800 to-gray-500
 flex flex-col items-center justify-center text-white"
    >
      <div
        onClick={() => {
          navigate(-1);
        }}
        className="absolute cursor-pointer top-5 left-5 border-2 rounded-full w-12 h-12 flex items-center justify-center hover:bg-white hover:text-black"
      >
        <IoMdArrowRoundBack className="text-2xl hover:cursor-pointer" />
      </div>
      <Particles />
      <h1 className="font-extrabold">Game setup</h1>
      <p className="font-bold text-xl my-5">Number of rounds:</p>
      <div className="gap-5 flex-row w-screen">
        <button
          className={
            "hover:shadow-lg hover:shadow-[#646cff] hover:border-[#646cff] hover:border-2 transition-all duration-50" +
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
            "hover:shadow-lg hover:shadow-[#646cff] ml-5 hover:border-[#646cff] hover:border-2 transition-all duration-50" +
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
            "hover:shadow-lg hover:shadow-[#646cff] ml-5 hover:border-[#646cff] hover:border-2 transition-all duration-50" +
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
      <p className="font-bold text-xl my-5">Total time for you:</p>
      <div className="gap-5 flex-row w-screen">
        <button
          className="hover:shadow-lg hover:shadow-[#646cff] hover:border-[#646cff] hover:border-2 transition-all duration-50"
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
          className="hover:shadow-lg hover:shadow-[#646cff] hover:border-[#646cff] hover:border-2 transition-all duration-50"
        >
          -
        </button>
      </div>
      <div>
        <p className="font-bold text-xl my-5">Side chosen:</p>
        <div>
          <button
            onClick={() => setSideChosen("X")}
            className={`text-[#646cff] hover:border-[#646cff] hover:border-2 transition-all duration-50 ${
              sideChosen === "X" ? "border-[#646cff] border-2" : ""
            }`}
          >
            <span className="font-extrabold">X</span>
          </button>
          <button
            onClick={() => setSideChosen("O")}
            className={`ml-5 text-[#ff6f91] hover:border-[#ff6f91] hover:border-2 transition-all duration-50 ${
              sideChosen === "O" ? "border-[#ff6f91] border-2" : ""
            }`}
          >
            <span className="font-extrabold">O</span>
          </button>
        </div>
      </div>
      <button
        onClick={() => {
          navigate(
            `/computerGame?rounds=${selectedRounds}&time=${
              timeMinute * 60 + parseInt(timeSecond)
            }&side=${sideChosen}`
          );
        }}
        className="mt-4 px-4 py-2 bg-blue-600 rounded hover:shadow-lg hover:shadow-[#646cff] hover:border-[#646cff] hover:border-2 transition-all duration-50"
      >
        Start Game
      </button>
    </div>
  );
}
