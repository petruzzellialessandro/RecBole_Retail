import React, { useState } from 'react';
import { fetchTaskResult, renderResponse } from '../api';
import { BtnProps } from '../App';
import { EvaluateResponse, PredictResponse } from '../models';

export const ResultForm: React.FC<BtnProps> = ({ btnClass }) => {
    const [taskID, settaskID] = useState('');
    const [taskResponse, setTaskResponse] = useState<PredictResponse | EvaluateResponse | null>(null);
    const [message, setMessage] = useState('');

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setMessage('');
        setTaskResponse(null);

        if (!taskID) {
            setMessage('Please select a task ID.');
            return;
        }

        try {
            const result = await fetchTaskResult(taskID);
            setTaskResponse(result);
        } catch (error) {
            setMessage(`Failed to fetch task result: ${error}`);
            setTaskResponse(null);
        }
    };

    return (
        <section>
            <h2>Fetch Task Result</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Enter task ID"
                    value={taskID}
                    onChange={(e) => settaskID(e.target.value.trim())}
                    required
                    className='flex-grow'
                />
                <button className={btnClass} type="submit">Fetch</button>
            </form>
            {/* {taskResponse && (
                <div className='p-3 grid grid-cols-9 gap-x-4 gap-y-2'>
                    <div className='col-span-2 font-bold text-lg'>Task Status:</div>
                    <div className='col-span-7'>{taskResponse.status}</div>

                    <div className='col-span-2 font-bold text-lg'>Result:</div>
                    <div className='col-span-7'>{taskResponse.result ? renderResult(taskResponse.result) : 'No result available.'}</div>
                </div>
            )}
            {message && showResponse && <div className='p-3 font-bold text-lg'>{message}</div>} */}
            {taskResponse && (
                <div className='p-3 grid grid-cols-9 gap-x-4 gap-y-2'>{taskResponse ? renderResponse(taskResponse) : 'No result available.'}</div>
            )}
            {message && <div className='p-3 font-bold text-lg'>{message}</div>}
        </section>
    );
};

export default ResultForm;
