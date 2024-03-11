import React, { useState } from 'react';
import { fetchTaskResult, renderResult, TASK_TYPES } from '../api';
import { BtnProps } from '../App';
import CustomSelect from '../components/select';

export const ResultForm: React.FC<BtnProps> = ({ btnClass }) => {
    const [taskId, setTaskId] = useState('');
    const [taskResult, setTaskResult] = useState<any | null>(null);
    const [errorMessage, setErrorMessage] = useState('');
    const [selectedOption, setSelectedOption] = useState<string>('');

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!taskId || !selectedOption) {
            setErrorMessage('Please select a task type and enter a task ID.');
            return;
        }

        try {
            const result = await fetchTaskResult(selectedOption, taskId);
            setTaskResult(result);
            setErrorMessage('');
        } catch (error) {
            setErrorMessage(`Failed to fetch task result: ${error}`);
            setTaskResult(null);
        }
    };

    return (
        <section>
            <h2>Fetch Task Result</h2>
            <form onSubmit={handleSubmit}>
                <CustomSelect onSelected={setSelectedOption} options={TASK_TYPES} placeholder='Select a Task Type'/>
                <input
                    type="text"
                    placeholder="Enter task ID"
                    value={taskId}
                    onChange={(e) => setTaskId(e.target.value)}
                    required
                    className='flex-grow'
                />
                <button className={btnClass} type="submit">Fetch</button>
            </form>
            {taskResult && (
                <div className='p-3 grid grid-cols-9 gap-x-4 gap-y-2'>
                    <div className='col-span-2 font-bold text-lg'>Task ID:</div>
                    <div className='col-span-7'>{taskResult.task_id}</div>

                    <div className='col-span-2 font-bold text-lg'>Task Status:</div>
                    <div className='col-span-7'>{taskResult.status}</div>

                    <div className='col-span-2 font-bold text-lg'>Result:</div>
                    <div className='col-span-7'>{taskResult.result ? renderResult(taskResult.result) : 'No result available.'}</div>
                </div>

            )}
            {errorMessage && <div>{errorMessage}</div>}
        </section>
    );
};

export default ResultForm;
