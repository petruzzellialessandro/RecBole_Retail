import React, { useState } from 'react';
import { sendTrainingRequest, checkTaskStatus, fetchTaskResult  } from '../api';
import { BtnProps } from '../App';
import ModelSelect from '../components/select';

export const TrainForm: React.FC<BtnProps> = ({ btnClass }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [trainingResponse, setTrainingResponse] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [taskID, setTaskID] = useState<string>('');
  const [taskResult, setTaskResult] = useState<string | null>(null);
  const TASK = 'train';

  const handleTrainingSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage('');

    if (!username || !password || !selectedOption) {
      setErrorMessage('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.set('username', username);
    formData.set('password', password);
    formData.set('model', selectedOption);

    try {
      const taskResponse = await sendTrainingRequest(formData);
      setTaskID(taskResponse.task_id);
      setTaskResult(null);
      handleCheckResult(taskResponse.task_id);
    } catch (error) {
      setErrorMessage(`Failed to send recommendation request: ${error}`);
    }
  };

  const handleCheckResult = async (taskId: string) => {
    try {
      const statusResponse = await checkTaskStatus(TASK, taskId);
      if (statusResponse === 'completed') {
        const result = await fetchTaskResult(TASK, taskId); 
        setTaskResult(JSON.stringify(result));
      } else if (statusResponse.status === 'failed') {
        setErrorMessage('Task failed.');
      } else {
        setErrorMessage('Task is not completed yet.');
      }
    } catch (error) {
      setErrorMessage(`Failed to fetch task result: ${error}`);
    }
  };

  const taskStatusLink = taskID ? `http://localhost:8000/${TASK}/task-status/${taskID}` : '';

  return (
    <section>
      <h2>Start Training</h2>
      <form onSubmit={handleTrainingSubmit} className='flex flex-wrap gap-y-3 2xl:flex-nowrap 2xl: gap-x-3 items-center'>
          <input
            type="text"
            placeholder='Admin username'
            name="username"
            className='flex-grow'
            required
            autoComplete='true'
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Admin password"
            name="password"
            className='flex-grow'
            required
            autoComplete='true'
            onChange={(e) => setPassword(e.target.value)}
          />
          <ModelSelect onSelected={setSelectedOption} />
          <button className={btnClass} type="submit">Train</button>
      </form>
      {taskID && (
        <div>
          Task ID: <a href={taskStatusLink} target="_blank" rel="noopener noreferrer" className='underline'>{taskID}</a>
          <p>
            <button onClick={() => handleCheckResult(taskID)} className="text-accent-700 hover:underline">Check Result</button>
          </p>
        </div>
      )}
      {taskResult && <div>Result: {taskResult}</div>}
      {errorMessage && <div>{errorMessage}</div>}
    </section>
  );
};
