import React, { useState } from 'react';
import { sendEvaluationRequest, checkTaskStatus, fetchTaskResult } from '../api';
import { BtnProps } from '../App';

import ModelSelect from '../components/select';
import InputFile from '../components/inputFile';

export const EvaluateForm: React.FC<BtnProps> = ({btnClass}) => {
  const [taskID, setTaskID] = useState<string>('');
  const [taskResult, setTaskResult] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [file, setFile] = useState<File>();
  const TASK = 'evaluate';

  const handleEvaluationSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage('');
    
    if (!file || !selectedOption) {
      setErrorMessage('All fields are required.');
      return;
    }

    const formData = new FormData();
    formData.set('model', selectedOption);
    formData.set('file', file as Blob);

    try {
      const taskResponse = await sendEvaluationRequest(formData);
      setTaskID(taskResponse.task_id);
      setTaskResult(null);
      handleCheckResult(taskResponse.task_id);
    } catch (error) {
      setErrorMessage(`Failed to send evaluation request: ${error}`);
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
      <h2>Evaluate Performance Metrics</h2>
      <form onSubmit={handleEvaluationSubmit} className='flex flex-wrap gap-y-3 2xl:flex-nowrap 2xl: gap-x-3 items-center'>
        <InputFile onFileSelect={setFile} />
        <ModelSelect onSelected={setSelectedOption} />
        <button type="submit" className={btnClass}>Evaluate</button>
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
