import React, { useState } from 'react';
import {
  sendEvaluationRequest,
  handleCheckResult,
  renderResult,
} from '../api';
import { BtnProps } from '../App';
import CustomSelect from '../components/select';
import InputFile from '../components/inputFile';
import { TaskType, EvaluateResponse, MODELS } from '../models';

export const EvaluateForm: React.FC<BtnProps> = ({ btnClass }) => {
  const [taskID, setTaskID] = useState<string>('');
  const [taskResult, setTaskResult] = useState<EvaluateResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);
  const TASK = TaskType.EVALUATE;

  const handleEvaluationSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage('');

    if (!file || !selectedOption) {
      setErrorMessage('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.append('model', selectedOption);
    formData.append('file', file);

    try {
      const taskResponse = await sendEvaluationRequest(formData);
      setTaskID(taskResponse.task_id);
      setTaskResult(null);
      handleCheckResult(taskResponse.task_id, setErrorMessage, setTaskResult, TaskType.EVALUATE);
    } catch (error) {
      setErrorMessage(`Failed to send evaluation request: ${error}`);
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
          <div className='p-3 grid grid-cols-9 gap-x-4 gap-y-2'>
            <div className='col-span-2 font-bold text-lg'>Task ID:</div>
            <div className='col-span-7'>{taskID}</div>
          </div>
      )}
      {taskID && !taskResult && (
        <button onClick={() => handleCheckResult(taskID, setErrorMessage, setTaskResult, TASK)} className="text-accent-700 hover:underline text-2xl font-bold p-3">Check Result</button>       
      )}
      {taskResult && (
        <div className='p-3 grid grid-cols-9 gap-x-4 gap-y-2'>
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
