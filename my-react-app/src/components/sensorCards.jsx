import React from "react";  
import './sensorCards.css';
import {Thermometer,Droplet, Activity} from 'lucide-react';
import { AreaChart, ResponsiveContainer, Area, Tooltip } from 'recharts';
import './Charts.css';


const SensorCard = ({icon: Icon, title, value, unit, data}) => {
    return(
        <div className="sensor-card">
            <div className="card-title">
                <div className="icon-bgg"><Icon size={24} color="#4D84C8" className='icon-bg' /></div>
                <p className="title-hero">{title}</p>
            </div>

            <div className="card-details">
                <div className="card-data">
                    <p className="cd-hero">{value}{unit}</p>
                </div>
                <div className="chart-container">
                    <ResponsiveContainer width="100%" height={107}>
                        <AreaChart data={data}>
                            <Tooltip />
                            <Area type="monotone" dataKey={title} fill="#04BFDA" stroke="#5695E1" fillOpacity={0.05} connectNulls dot = {false} /> 
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default SensorCard;