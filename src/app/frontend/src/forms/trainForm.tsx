import React, { useState } from 'react';
import { sendTrainingRequest, handleCheckResult, TaskType, getStatusLink, BaseResponse, MODELS } from '../api';
import { BtnProps } from '../App';

import CustomSelect from '../components/select';

export const TrainForm: React.FC<BtnProps> = ({ btnClass }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [taskID, setTaskID] = useState<string>('');
  const [taskResult, setTaskResult] = useState<BaseResponse | null>(null);
  const TASK = TaskType.TRAIN;

  const handleTrainingSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage('');

    if (!username || !password || !selectedOption) {
      setErrorMessage('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('model', selectedOption);

    try {
      const taskResponse = await sendTrainingRequest(formData);
      setTaskID(taskResponse.task_id);
      setTaskResult(null);
      handleCheckResult(taskResponse.task_id, setErrorMessage, setTaskResult, TASK);
    } catch (error) {
      setErrorMessage(`Failed to send training request: ${error}`);
    }
  };

  return (
    <section>
      <h2>Start Training</h2>
      <form onSubmit={handleTrainingSubmit}>
          <input
            type="text"
            placeholder='Admin username'
            name="username"
            className='flex-grow'
            required
            autoComplete='username'
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Admin password"
            name="password"
            className='flex-grow'
            required
            autoComplete='current-password'
            onChange={(e) => setPassword(e.target.value)}
          />
          <CustomSelect onSelected={setSelectedOption} options={MODELS} />
          <button className={btnClass} type="submit">Train</button>
      </form>
      {taskID && (
        <div>
          Task ID: <a href={getStatusLink(TASK, taskID)} target="_blank" rel="noopener noreferrer" className='underline'>{taskID}</a>
          <p>
            <button onClick={() => handleCheckResult(taskID, setErrorMessage, setTaskResult, TASK)} className="text-accent-700 hover:underline">Check Result</button>
          </p>
        </div>
      )}
      {taskResult && <div>Result: {taskResult.toString()}</div>}
      {errorMessage && !taskResult && <div>{errorMessage}</div>}
    </section>
  );
};
