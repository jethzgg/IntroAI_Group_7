import { useState } from "react";
import { GiTicTacToe } from "react-icons/gi";
import { FaComputer } from "react-icons/fa6";
import { SlPeople } from "react-icons/sl";
import { IoIosSettings } from "react-icons/io";
import Particles from "../components/Particle";
import "../App.css";
import { useNavigate } from "react-router";
function App() {
  const navigate = useNavigate();
  return (
    <div
      className="h-screen w-screen animated-gradient bg-gradient-to-br from-gray-900 via-gray-800 to-gray-500
 flex flex-col items-center justify-center text-white"
    >
      <Particles />
      <div>
        <GiTicTacToe className="w-40 h-40 mx-auto" />
      </div>
      <h1 className="font-extrabold">Tic Tac Toe Game</h1>
      <div className="card">
        <button
          className="hover:shadow-lg hover:shadow-[#646cff] 
"
          onClick={() => {
            navigate("/computer");
          }}
        >
          <FaComputer className="inline-block mr-2 text-xl" /> Play With
          Computer
        </button>
        <button
          className="hover:shadow-lg hover:shadow-[#646cff]"
          onClick={() => {
            navigate("/withPlayer");
          }}
        >
          <SlPeople className="inline-block mr-2 text-xl" /> Play With Player
        </button>
        <button className="hover:shadow-lg hover:shadow-[#646cff]">
          <IoIosSettings className="inline-block mr-2 text-xl" /> Cài đặt
        </button>
      </div>
    </div>
  );
}

export default App;
