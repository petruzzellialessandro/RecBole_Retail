import React, { useState } from 'react';
import { fetchTaskResult, TASK_TYPES } from '../api'; // Assicurati che il percorso sia corretto
import ModelSelect from '../components/modelSelect';
import { BtnProps } from '../App';

export const ResultForm: React.FC<BtnProps> = ({ btnClass }) => {
    const [taskId, setTaskId] = useState('');
    const [taskResult, setTaskResult] = useState<any | null>(null);
    const [errorMessage, setErrorMessage] = useState('');
    const [selectedOption, setSelectedOption] = useState<string>('');

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!taskId) {
            setErrorMessage('Please enter a task ID.');
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
                <ModelSelect onSelected={setSelectedOption} options={TASK_TYPES} placeholder='Select a task'/>
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
            {taskResult && <div><h3>Result:</h3><pre>{JSON.stringify(taskResult, null, 2)}</pre></div>}
            {errorMessage && <div>{errorMessage}</div>}
        </section>
    );
};

export default ResultForm;
