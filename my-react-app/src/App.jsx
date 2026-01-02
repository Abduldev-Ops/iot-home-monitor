import React, { useState, useEffect } from 'react';
import { Activity, Droplets, Thermometer } from 'lucide-react';
import Header from './components/header';
import Dashboard from './components/Dashboard';
import './App.css'

const App = () => {
  return (
    <div className='app'>
      <Header />
      <div className='app-body'>
          <Dashboard />
        </div>

      </div>
  );
};

export default App;

