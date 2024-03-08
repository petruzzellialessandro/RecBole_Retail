import React, { useState } from 'react';
import { sendPredictionRequest, checkTaskStatus, fetchTaskResult } from '../api';
import { BtnProps } from '../App';
import InputFile from '../components/inputFile';
import ModelSelect from '../components/select';

export const PredictForm: React.FC<BtnProps> = ({ btnClass }) => {
  const [userID, setUserID] = useState<string>('');
  const [k, setK] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [file, setFile] = useState<File>();
  const [taskID, setTaskID] = useState<string>('');
  const [taskResult, setTaskResult] = useState<string | null>(null);
  const TASK = 'predict';


  const handlePredictionSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage('');

    if (!userID || !k || !file || !selectedOption) {
      setErrorMessage('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.set('model', selectedOption);
    formData.set('k', k);
    formData.set('user_id', userID);
    formData.set('file', file as Blob);
    
    try {
      const taskResponse = await sendPredictionRequest(formData);
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
      <h2>Request User Recommendation</h2>
      <form onSubmit={handlePredictionSubmit} className='flex flex-wrap gap-y-3 2xl:flex-nowrap 2xl: gap-x-3 items-center'>
        <input placeholder="User ID" type="text" name="user_id" required  className='flex-grow' onChange={(e) => setUserID(e.target.value)} />
        <input placeholder='N.Recommendations' type="number" name="k" required  className='flex-grow' onChange={(e) => setK(e.target.value)} />
        <InputFile onFileSelect={setFile} />
        <ModelSelect onSelected={setSelectedOption} />
        <button type="submit" className={btnClass}>Send</button>
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
