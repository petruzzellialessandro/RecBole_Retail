import React, { useEffect, useState } from 'react';
import { sendTrainingRequest, handleCheckResult, copyToClipboard, renderResult } from '../api';
import { BtnProps } from '../App';
import CustomSelect from '../components/select';
import { MODELS, PredictResponse } from '../models';

export const TrainForm: React.FC<BtnProps> = ({ btnClass }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [taskID, setTaskID] = useState<string>('');
  const [taskResponse, setTaskResponse] = useState<PredictResponse>();
  const [showResponse, setShowResponse] = useState<boolean>(false);
  const [showCheckButton, setShowCheckButton] = useState<boolean>(false);

  useEffect(() => {
    if (taskResponse) {
      setShowCheckButton(false);
      setShowResponse(true);
    }
  }, [taskResponse]);
  
  const handleTrainingSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage('');
    setShowResponse(false);
    setShowCheckButton(true);

    if (!username || !password || !selectedOption) {
      setMessage('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('model', selectedOption);

    try {
      const response = await sendTrainingRequest(formData);
      setTaskID(response.task_id);
      handleCheckResult(response.task_id, setMessage, setTaskResponse);
    } catch (error) {
      setMessage(`Failed to send training request: ${error}`);
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
            onChange={(e) => setUsername(e.target.value.trim())}
          />
          <input
            type="password"
            placeholder="Admin password"
            name="password"
            className='flex-grow'
            required
            autoComplete='current-password'
            onChange={(e) => setPassword(e.target.value.trim())}
          />
          <CustomSelect onSelected={setSelectedOption} options={MODELS} />
          <button className={btnClass} type="submit">Train</button>
      </form>
      {/* {taskID && (
          <div className='p-3 pb-0 grid grid-cols-9 gap-x-4 gap-y-2'>
            <div className='col-span-2 font-bold text-lg'>Task ID:</div>
            <div className='col-span-7'>{copyToClipboard(taskID)}</div>
          </div>
      )}
      {message && showResponse && <div className='p-3 font-bold text-lg'>{message}</div>}
      {taskID && showCheckButton && (
        <button onClick={() => handleCheckResult(taskID, setMessage, setTaskResponse)} className="text-accent-700 hover:underline text-2xl font-bold p-3">Check Result</button>       
      )} */}
      {taskID && (
          <div className='p-3 pb-0 grid grid-cols-9 gap-x-4 gap-y-2'>
            <div className='col-span-2 font-bold text-lg'>Task ID:</div>
            <div className='col-span-7'>{copyToClipboard(taskID)}</div>
          </div>
      )}
      {taskResponse && showResponse  && (
        <div className='p-3 grid grid-cols-9 gap-x-4 gap-y-2'>{taskResponse && showResponse ? renderResult(taskResponse) : 'No result available.'}</div>
      )}
      {message && showResponse && <div className='p-3 font-bold text-lg'>{message}</div>}
      {taskID && showCheckButton && (
        <button onClick={() => handleCheckResult(taskID, setMessage, setTaskResponse)} className="text-accent-700 hover:underline text-2xl font-bold p-3">Check Result</button>       
      )}
    </section>
  );
};
