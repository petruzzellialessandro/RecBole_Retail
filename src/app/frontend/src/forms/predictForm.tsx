import React, { useEffect, useState } from 'react';
import {
  sendPredictionRequest,
  handleCheckResult,
  renderPredictResponse,
  copyToClipboard
} from '../api';
import { BtnProps } from '../App';
import InputFile from '../components/inputFile';
import CustomSelect from '../components/select';
import { PredictResponse, MODELS } from '../models';

export const PredictForm: React.FC<BtnProps> = ({ btnClass }) => {
  const [userID, setUserID] = useState<string>('');
  const [k, setK] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);
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

  const handlePredictionSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage('');
    setShowResponse(false);
    setShowCheckButton(true);

    if (!userID || !k || !file || !selectedOption) {
      setMessage('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.append('model', selectedOption);
    formData.append('k', k);
    formData.append('user_token', userID);
    formData.append('file', file);

    try {
      const response = await sendPredictionRequest(formData);
      setTaskID(response.task_id);
      handleCheckResult(response.task_id, setMessage, setTaskResponse);
    } catch (error) {
      setMessage(`Failed to send recommendation request: ${error}`);
    }
  };

  return (
    <section>
      <h2>Request User Recommendation</h2>
      <form onSubmit={handlePredictionSubmit}>
        <input placeholder="User token" type="text" name="user_id" required className='w-auto' onChange={(e) => setUserID(e.target.value.trim())} />
        <input placeholder='K' type="number" min="1" name="k" required className='w-24' onChange={(e) => setK(e.target.value.trim())} />
        <InputFile placeholder="Products tokens file" onFileSelect={(f) => setFile(f)} />
        <CustomSelect onSelected={setSelectedOption} options={MODELS} />
        <button type="submit" className={btnClass}>Send</button>
      </form>
      {taskID && (
          <div className='p-3 pb-0 grid grid-cols-9 gap-x-4'>
            <div className='col-span-2 font-bold text-lg'>Task ID:</div>
            <div className='col-span-7'>{copyToClipboard(taskID)}</div>
          </div>
      )}
      {taskResponse && showResponse  && (
        <div className='p-3 grid grid-cols-9 gap-x-4 gap-y-2'>{taskResponse && showResponse ? renderPredictResponse(taskResponse) : 'No result available.'}</div>
      )}
      {message && showResponse && <div className='p-3 font-bold text-lg'>{message}</div>}
      {taskID && showCheckButton && (
        <button onClick={() => handleCheckResult(taskID, setMessage, setTaskResponse)} className="text-accent-700 hover:underline text-2xl font-bold p-3">Check Result</button>       
      )}
    </section>
  );
};
