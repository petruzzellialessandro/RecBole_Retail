import React, { useState } from 'react';
import {
  sendPredictionRequest,
  handleCheckResult,
  TaskType,
  PredictResponse,
  MODELS
} from '../api';
import { BtnProps } from '../App';

import InputFile from '../components/inputFile';
import ModelSelect from '../components/modelSelect';

export const PredictForm: React.FC<BtnProps> = ({ btnClass }) => {
  const [userID, setUserID] = useState<string>('');
  const [k, setK] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);
  const [taskID, setTaskID] = useState<string>('');
  const [taskResult, setTaskResult] = useState<PredictResponse | null>(null);
  const TASK = TaskType.PREDICT;

  const handlePredictionSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage('');

    if (!userID || !k || !file || !selectedOption) {
      setErrorMessage('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.append('model', selectedOption);
    formData.append('k', k);
    formData.append('user_id', userID);
    formData.append('file', file);

    try {
      const taskResponse = await sendPredictionRequest(formData);
      setTaskID(taskResponse.task_id);
      setTaskResult(null);
      handleCheckResult(taskResponse.task_id, setErrorMessage, setTaskResult, TASK);
    } catch (error) {
      setErrorMessage(`Failed to send recommendation request: ${error}`);
    }
  };

  return (
    <section>
      <h2>Request User Recommendation</h2>
      <form onSubmit={handlePredictionSubmit}>
        <input placeholder="User ID" type="text" name="user_id" required className='flex-grow' onChange={(e) => setUserID(e.target.value)} />
        <input placeholder='N.Recommendations' type="number" min="1" name="k" required className='flex-grow' onChange={(e) => setK(e.target.value)} />
        <InputFile onFileSelect={(f) => setFile(f)} />
        <ModelSelect onSelected={setSelectedOption} options={MODELS} />
        <button type="submit" className={btnClass}>Send</button>
      </form>
      {taskID && (
        <div>
          <p>
            <button onClick={() => handleCheckResult(taskID, setErrorMessage, setTaskResult, TASK)} className="text-accent-700 hover:underline">Check Result</button>
          </p>
          Task ID: {taskID}
        </div>
      )}
      {taskResult && <div>Result: {JSON.stringify(taskResult.result)}</div>}
      {errorMessage && !taskResult && <div>{errorMessage}</div>}
    </section>
  );
};
