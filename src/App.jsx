import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainMenu from "./pages/MainMenu";
import WithPlayer from "./pages/WithPlayer";
import PlayerGame from "./pages/PlayerGame";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainMenu />} />
        <Route path="/withPlayer" element={<WithPlayer />} />
        <Route path="/playerGame" element={<PlayerGame />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
