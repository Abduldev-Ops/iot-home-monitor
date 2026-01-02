import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Charts.css';

function SensorChart({ data, title }) {
  return (
    <div className="chart-container">
      <h3 className="chart-title">{title}</h3>
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={data}>
          <CartesianGrid stroke="#eee" strokeDasharray='3 3' />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="temperature" stroke="#FF6B6B" name="Temperature (°C)" />
          <Line type="monotone" dataKey="humidity" stroke="#4ECDC4" name="Humidity (%)" />

        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SensorChart;