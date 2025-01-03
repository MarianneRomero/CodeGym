import React, { useState } from 'react'; 
import ContactLeft from '../assets/about.png';
import '../styles/AddWorkout.css';
import {addExercise, addWorkoutPlan} from '../axios.js'

function AddWorkout() {
  const [workoutName, setWorkoutName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [exercises, setExercises] = useState([{ name: '', reps: '' }]);

  const handleWorkoutNameChange = (e) => {
    setWorkoutName(e.target.value);
  };
  const handleStartDateChange = (e) => setStartDate(e.target.value);
  const handleEndDateChange = (e) => setEndDate(e.target.value);

  const handleExerciseChange = (index, e) => {
    const newExercises = [...exercises];
    newExercises[index][e.target.name] = e.target.value;
    setExercises(newExercises);
  };

  const handleAddExercise = () => {
    setExercises([...exercises, { name: '', reps: '' }]);
  };

  const handleRemoveExercise = (index) => {
    const newExercises = exercises.filter((_, i) => i !== index);
    setExercises(newExercises);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await addWorkoutPlan(
      {
        "workout_plan_name": workoutName,
        "start_date": startDate,
        "end_date": endDate,
        "workout_id": 0
      }
    );
    exercises.map((exercise) =>
        addExercise(
        {
          name: exercise.name,
          reps: exercise.reps,
          workout_id: data.workout_id,
          exercise_id: 0
        })
      );
      setWorkoutName('');
      setStartDate('');
      setEndDate('');
      setExercises([{name:'', reps:0}]);
    // Handle form submission (e.g., sending the workout data to an API or storing it)
  };

  return (
    <div className="addWorkout">
      <div className="leftSide" style={{ backgroundImage: `url(${ContactLeft})` }}></div> 
      <div className="rightSide">
        <h1>Workout Form</h1>
        <form id="contact-form" method="POST" onSubmit={handleSubmit}>
          <label htmlFor="workout-name">Workout Name</label>
          <input
            name="workout-name"
            placeholder="Enter workout name..."
            type="text"
            value={workoutName}
            onChange={handleWorkoutNameChange}
            required
          />
          <div className="date-row">
            <div>
              <label htmlFor="start-date">Start Date</label>
              <input
                name="start-date"
                type="date"
                value={startDate}
                onChange={handleStartDateChange}
                required
              />
            </div>
            <div>
              <label htmlFor="end-date">End Date</label>
              <input
                name="end-date"
                type="date"
                value={endDate}
                onChange={handleEndDateChange}
                required
              />
            </div>
          </div>

          
          <h3>Exercises</h3>
          {exercises.map((exercise, index) => (
            <div key={index} className="exercise-row">
              <input
                name="name"
                placeholder="Exercise name"
                type="text"
                value={exercise.name}
                onChange={(e) => handleExerciseChange(index, e)}
                required
              />
              <input
                name="reps"
                placeholder="Reps"
                type="text"
                value={exercise.reps}
                onChange={(e) => handleExerciseChange(index, e)}
                required
              />
              <button className="remove-button" type="button" onClick={() => handleRemoveExercise(index)}>
                Remove
              </button>
            </div>
          ))}

          <button type="button" onClick={handleAddExercise}>Add Exercise</button>
          <button type="submit" onClick={handleSubmit}>Submit Workout</button>
        </form>
      </div>
    </div>
  );
}

export default AddWorkout;
