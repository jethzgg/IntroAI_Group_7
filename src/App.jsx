import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainMenu from "./pages/MainMenu";
import WithPlayer from "./pages/WithPlayer";
import PlayerGame from "./pages/PlayerGame";
import WithComputer from "./pages/WithComputer";
import ComputerGame from "./pages/ComputerGame";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainMenu />} />
        <Route path="/computer" element={<WithComputer />} />
        <Route path="/withPlayer" element={<WithPlayer />} />
        <Route path="/playerGame" element={<PlayerGame />} />
        <Route path="/computerGame" element={<ComputerGame />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
