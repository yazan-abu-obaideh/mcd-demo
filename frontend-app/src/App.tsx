import "./styles.css";
import McdDemoUserForm from "./components/McdDemoUserForm";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { READ_MORE } from "./paths";
import { ReadMore } from "./pages/ReadMore";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route index path="/" element={<McdDemoUserForm />} />
          <Route path={READ_MORE} element={<ReadMore />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
