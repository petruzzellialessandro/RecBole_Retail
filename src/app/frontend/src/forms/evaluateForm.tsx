import React, { useState } from 'react';
import {
  sendEvaluationRequest,
  handleCheckResult,
  TaskType,
  getStatusLink,
  EvaluateResponse,
  MODELS
} from '../api';
import { BtnProps } from '../App';

import CustomSelect from '../components/select';
import InputFile from '../components/inputFile';

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
        <InputFile onFileSelect={(f) => setFile(f)} />
        <CustomSelect onSelected={setSelectedOption} options={MODELS} />
        <button type="submit" className={btnClass}>Evaluate</button>
      </form>
      {taskID && (
        <div>
          Task ID: <a href={getStatusLink(TASK, taskID)} target="_blank" rel="noopener noreferrer" className='underline'>{taskID}</a>
          <p>
            <button onClick={() => handleCheckResult(taskID, setErrorMessage, setTaskResult, TASK)} className="text-accent-700 hover:underline">Check Result</button>
          </p>
        </div>
      )}
      {taskResult && <div>Result: {JSON.stringify(taskResult.result)}</div>}
      {errorMessage && !taskResult && <div>{errorMessage}</div>}
    </section>
  );
};
