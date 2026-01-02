import SensorCard from './sensorCards.jsx';
import SensorChart from './charts.jsx';
import { Activity, Droplets, Thermometer } from 'lucide-react';
import './Dashboard.css';
import MotionSensorCard from './motionSensorCard.jsx';
import { useState, useEffect } from 'react';

function Dashboard() {
  const [sensorData, setSensorData] = useState({temperature: '--', humidity: '--', motion: false});
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
          temperature: data.temperature,
          humidity: data.humidity,
          timestamp: data.timestamp
        }];
        return newHistory.slice(-20);
      });


    } catch (error) {
      console.error('Error fetching sensor data:', error);
      // const data = {'timestamp': 0,
      //           'temperature': 0,
      //           'humidity': 0,
      //           'motion': 'false'}
      // setSensorData(data);
    } finally {
      setLoading(false);
    }
  };

  // NEW: Fetch historical data for charts
const fetchHistory = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/sensor/history');
    if (!response.ok) throw new Error('Failed to fetch history');
    
    const data = await response.json();
    
    // Format data for charts
    const formattedHistory = data.map(reading => ({
      time: new Date(reading.timestamp).toLocaleTimeString(),
      temperature: reading.temperature,
      humidity: reading.humidity,
      timestamp: reading.timestamp
    }));
    
    setDataHistory(formattedHistory);
    console.log('Loaded history:', formattedHistory.length, 'readings');
    
  } catch (error) {
    console.error('Error fetching history:', error);
  }
};

  useEffect(() => {
    fetchSensorData();
    fetchHistory();
    const interval = setInterval(() => {
      fetchSensorData();  
    }, 10000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-content">
      <div className="sensor-cards-container">
      <SensorCard icon={Thermometer} title="temperature" value={sensorData.temperature} unit="°C" data={dataHistory} />
      <SensorCard icon={Droplets} title="humidity" value={sensorData.humidity} unit="%" data={dataHistory}/>
      <MotionSensorCard icon={Activity} title="Motion Detected" value={sensorData.motion ? "Motion Detected" : "No Motion Detected"} unit=""/>
      </div>
      
      {/* Chart section will go here later */}
      <div className="chart-section">
        <SensorChart data={dataHistory}  title="Temperature & Humidity Over Time" />
      </div>
    </div>
  );
}

export default Dashboard;