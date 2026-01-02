import React from "react";  
import './Header.css';
import {MapPin, RotateCcw} from 'lucide-react';
import { useState, useEffect } from 'react';

const Header = ({onRefresh}) => {
    const [sensorData, setSensorData] = useState ({timestamp:'--'});
    const [dataHistory, setDataHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchSensorData = async () => {
        setLoading(true);
        try{
          const response = await fetch('http://localhost:5000/api/sensor');
    
          if (!response.ok) {
            throw new Error('Failed to fetch sensor data');
          }
    
          const data = await response.json();
          console.log('Fetched data:', data);
    
          setSensorData(data);

          setDataHistory(prevHistory => {
            const newHistory = [...prevHistory, {
              time: new Date(data.timestamp).toLocaleTimeString(),
              timestamp: data.timestamp
            }];
            return newHistory.slice(-20);
          });
        } catch (error) {
          console.error('Error fetching sensor data:', error);
        } finally {
            setLoading(false);
          }
      };
    
      useEffect(() => {
        fetchSensorData();
        const interval = setInterval(() => {
            fetchSensorData();  
          }, 10000);
          
          return () => clearInterval(interval);
      }, []);

    return (
        <header className="flex-container1">
            <div className="head">
                <div className="location">
                    <MapPin size={17} color="#5695E1" className='map-pin'/>
                    <p className="location-hero">Winnipeg</p> 
                </div>
                <div className="lastUp">
                    <p className="lastUp-hero-txt">
                        Last Updated: <span className="time">{sensorData.timestamp}</span>
                    </p>
                </div>
                <div className="ref-btn">
                    <button onClick={() => window.location.reload()}> <RotateCcw size={17} color="#ffffff" className="rotate-ccw" /> Refresh </button>
                </div>
            </div>
            
        </header>
    );
};

export default Header;