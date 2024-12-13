import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  useParams,
} from 'react-router-dom';

import './App.css';
import Navbar from './components/Navbar';
import People from './components/People';

function PersonPage() {
  const { name } = useParams();
  return <h1>{name}</h1>
}

function App() {
  return (
    <BrowserRouter>
      <Navbar>
        <Routes>
          <Route path = "people" element={<People />} />
          <Route path = "people/:name" element = {<PersonPage />} />
        </Routes>
      </Navbar>
    </BrowserRouter>
  );
}

export default App;