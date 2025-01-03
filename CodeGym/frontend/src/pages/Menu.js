import React from 'react';
import MenuItem from '../components/MenuItem';
import { useNavigate } from "react-router-dom";
import '../styles/Menu.css';
import {useWorkoutPlans} from "../axios.js";

function Menu() {
  const navigate = useNavigate();

  //const handleMenuItemClick = (menuName) => {navigate(`/menu/${menuName}`);};

  const handleMenuTrackProgress = (workout_name, workout_id) => {navigate("/workoutprogress", { state: { workout_name, workout_id } })};

  //const handleMenuTrackProgress = ()=>{navigate("/workoutprogress")}
  const handleAddWorkoutClick = () => {
    navigate("/addworkout"); 
  };
  const ServiceList = useWorkoutPlans();
  return (
    <div>
      <div className="menu">
        <div className = "leftSide">
        <h1 className="serviceTitle">Our services</h1>
        <form id = "addworkout1" onSubmit={(e) => e.preventDefault()}>
            <button type="submit" onClick={handleAddWorkoutClick}> Add New Session! </button>
        </form>
        <div className="serviceList">
            {ServiceList.map((menuItem, key)=>(
                <button key={key} className = "workoutPlanButton" onClick={() => handleMenuTrackProgress(menuItem.name, menuItem.workout_id)}>
                <MenuItem 
                key = {key} 
                image={menuItem.image} 
                name ={menuItem.name} 
                description ={menuItem.description}/>
            </button> 
            ))}
        </div>
        </div>
      </div>
    </div>
  )
}

export default Menu

