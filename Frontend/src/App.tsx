import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import About from "./pages/About";
import { Routes, Route } from 'react-router-dom'
export default function App() {
  return (

    <div>
      <Routes>

        <Route path="/" element={<>

          <Navbar />
          <Home />
        </>} />
        <Route path="/about" element={<About />} />
      </Routes>
    </div>

  );
}