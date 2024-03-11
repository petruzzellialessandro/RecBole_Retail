import React, { useState } from 'react';
import {
  sendPredictionRequest,
  handleCheckResult,
  TaskType,
  PredictResponse,
  MODELS,
  renderResult
} from '../api';
import { BtnProps } from '../App';

import InputFile from '../components/inputFile';
import CustomSelect from '../components/select';

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
        <input placeholder='K' type="number" min="1" name="k" required className='w-32' onChange={(e) => setK(e.target.value)} />
        <InputFile onFileSelect={(f) => setFile(f)} />
        <CustomSelect onSelected={setSelectedOption} options={MODELS} />
        <button type="submit" className={btnClass}>Send</button>
      </form>
      {taskID && (
        <div>
          <button onClick={() => handleCheckResult(taskID, setErrorMessage, setTaskResult, TASK)} className="text-accent-700 hover:underline text-2xl font-bold py-5 px-3">Check Result</button>
          <div className='p-3 grid grid-cols-9 gap-x-4 gap-y-2'>
            <div className='col-span-2 font-bold text-lg'>Task ID:</div>
                <div className='col-span-7'>{taskID}</div>
            </div>
          </div>
      )}
      {taskResult && (
          <div className='px-3 pb-3 grid grid-cols-9 gap-x-4 gap-y-2'>
              <div className='col-span-2 font-bold text-lg'>Task Status:</div>
              <div className='col-span-7'>{taskResult.status}</div>

              <div className='col-span-2 font-bold text-lg'>Result:</div>
              <div className='col-span-7'>{taskResult.result ? renderResult(taskResult.result) : 'No result available.'}</div>
          </div>

      )}
      {errorMessage && !taskResult && <div className='p-3 font-bold'>{errorMessage}</div>}
    </section>
  );
};
