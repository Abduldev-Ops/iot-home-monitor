import React from "react";  
import './motionSensorCard.css';
import {Thermometer,Droplet, Activity} from 'lucide-react';


const MotionSensorCard = ({icon: Icon, title, value, unit}) => {
    return(
        <div className="sensor-card">
            <div className="card-title">
                <div className="icon-bgg"><Icon size={24} color="#4D84C8" className='icon-bg' /></div>
                <p className="title-hero">{title}</p>
            </div>

            <div className="card-data">
                <p className="cd-hero">{value}{unit}</p>
            </div>
                
        </div>
    );
};

export default MotionSensorCard;