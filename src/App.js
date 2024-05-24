// src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [result, setResult] = useState(null);

  const handleImage1Change = (event) => {
    setImage1(event.target.files[0]);
  };

  const handleImage2Change = (event) => {
    setImage2(event.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('image1', image1);
    formData.append('image2', image2);

    const response = await fetch('http://localhost:5000/compare-faces', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    setResult(data.result);
  };

  return (
    <div className="App">
      <h1>Comparador de Rostros</h1>
      <div>
        <input type="file" onChange={handleImage1Change} />
        <input type="file" onChange={handleImage2Change} />
        <button onClick={handleSubmit}>Comparar Rostros</button>
      </div>
      {result && <p>{result}</p>}
    </div>
  );
}

export default App;
