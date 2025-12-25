import { FaHome } from "react-icons/fa";
import { useNavigate } from "react-router";
export default function WinningModal({ winner, score, rounds, onClose }) {
  const navigate = useNavigate();
  return (
    <div className="fixed inset-0 bg-[rgba(0,0,0,0.5)] flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 w-80 text-center">
        {score.X + score.O < rounds ? (
          <div>
            <h2 className="text-2xl font-bold mb-4 text-black">
              {winner != "draw" ? `${winner} Wins!` : "It's a Draw!"}
            </h2>
            <p className="text-black text-xl">Current Score</p>
            <p className="font-bold text-5xl mb-10 text-black">
              <span className="text-[#646cff]">{score.X}</span> -{" "}
              <span className="text-[#ff6b6b]">{score.O}</span>
            </p>
          </div>
        ) : (
          <div>
            <h2 className="text-2xl font-bold mb-4 text-black">
              {score.X > score.O
                ? `X Wins the Match!`
                : score.O > score.X
                ? `O Wins the Match!`
                : "The Match is a Draw!"}
            </h2>
          </div>
        )}
        <div className="flex">
          <button
            className="mt-4 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 mr-2"
            onClick={() => {
              navigate("/");
            }}
          >
            <FaHome />
          </button>
          {score.X + score.O < rounds ? (
            <button
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              onClick={onClose}
            >
              Next Round
            </button>
          ) : (
            <button
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              onClick={() => {
                window.location.reload();
              }}
            >
              Play Again
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
