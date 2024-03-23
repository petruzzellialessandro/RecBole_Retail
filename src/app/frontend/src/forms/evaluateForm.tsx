import React, { useEffect, useState } from 'react';
import {
  sendEvaluationRequest,
  handleCheckResult,
  copyToClipboard,
  renderEvaluateResponse,
} from '../api';
import { BtnProps } from '../App';
import CustomSelect from '../components/select';
import InputFile from '../components/inputFile';
import { EvaluateResponse, MODELS } from '../models';

export const EvaluateForm: React.FC<BtnProps> = ({ btnClass }) => {
  const [taskID, setTaskID] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);
  const [taskResponse, setTaskResponse] = useState<EvaluateResponse>();
  const [showResponse, setShowResponse] = useState<boolean>(false);
  const [showCheckButton, setShowCheckButton] = useState<boolean>(false);

  useEffect(() => {
    if (taskResponse) {
      setShowCheckButton(false);
      setShowResponse(true);
    }
  }, [taskResponse]);

  const handleEvaluationSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage('');
    setShowResponse(false);
    setShowCheckButton(true);

    if (!file || !selectedOption) {
      setMessage('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.append('model', selectedOption);
    formData.append('file', file);

    try {
      const response = await sendEvaluationRequest(formData);
      setTaskID(response.task_id);
      handleCheckResult(response.task_id, setMessage, setTaskResponse);
    } catch (error) {
      setMessage(`Failed to send evaluation request: ${error}`);
    }
  };

  return (
    <section>
      <h2>Evaluate Performance Metrics</h2>
      <form onSubmit={handleEvaluationSubmit}>
        <InputFile placeholder="Interactions file" onFileSelect={(f) => setFile(f)} />
        <CustomSelect onSelected={setSelectedOption} options={MODELS} />
        <button type="submit" className={btnClass}>Evaluate</button>
      </form>
      {taskID && (
          <div className='p-3 pb-0 grid grid-cols-9 gap-x-4 gap-y-2'>
            <div className='col-span-2 font-bold text-lg'>Task ID:</div>
            <div className='col-span-7'>{copyToClipboard(taskID)}</div>
          </div>
      )}
      {taskResponse && showResponse  && (
        <div className='p-3 grid grid-cols-9 gap-x-4 gap-y-2'>{taskResponse && showResponse ? renderEvaluateResponse(taskResponse) : 'No result available.'}</div>
      )}
      {message && showResponse && <div className='p-3 font-bold text-lg'>{message}</div>}
      {taskID && showCheckButton && (
        <button onClick={() => handleCheckResult(taskID, setMessage, setTaskResponse)} className="text-accent-700 hover:underline text-2xl font-bold p-3">Check Result</button>       
      )}
    </section>
  );
};
