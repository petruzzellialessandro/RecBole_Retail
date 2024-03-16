import { TaskStatus, TaskType } from "./models";

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

const fetchData = async (url: string) => {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

export const getStatusLink = (task: string, taskId: string) => taskId ? `${BACKEND_URL}/${task}/task-status/${taskId}` : '';
export const getResultLink = (task: string, taskId: string) => taskId ? `${BACKEND_URL}/${task}/task-result/${taskId}` : '';

export const checkTaskStatus = async (task: string, taskId: string) => {
  const url = `${BACKEND_URL}/${task}/task-status/${taskId}`;
  return fetchData(url);
};

export const fetchTaskResult = async (task: string, taskId: string) => {
  const url = `${BACKEND_URL}/${task}/task-result/${taskId}`;
  return fetchData(url);
};

const postData = async (url: string, data: FormData) => {
  const response = await fetch(url, {
    method: 'POST',
    body: data
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export const sendPredictionRequest = async (data: FormData) => {
  const url = `${BACKEND_URL}/predict`;
  return postData(url, data);
};

export const sendEvaluationRequest = async (data: FormData) => {
  const url = `${BACKEND_URL}/evaluate`;
  return postData(url, data);
};

export const sendTrainingRequest = async (data: FormData) => {
  const url = `${BACKEND_URL}/train`;
  return postData(url, data);
};

export const handleCheckResult = async (
  taskId: string,
  setErrorMessage: React.Dispatch<string>,
  setTaskResult: React.Dispatch<any>,
  task: TaskType
) => {
  try {
    const statusResponse = await checkTaskStatus(task, taskId);
    switch (statusResponse.status) {
      case TaskStatus.STARTED:
        setErrorMessage('Task has started.');
        break;
        case TaskStatus.PENDING:
          setErrorMessage('Task is not completed yet.');
          break;
          case TaskStatus.SUCCESS:
        const result = await fetchTaskResult(task, taskId);
        if (result) {
          setErrorMessage('')
          setTaskResult(result);
        }
        break;
      case TaskStatus.FAILED:
        setErrorMessage('Task failed.');
        break;
      default:
        setErrorMessage('Status unknown.');
    }
  } catch (error) {
    setErrorMessage(`Failed to fetch task result: ${error}`);
  }
};

export const renderResult = (result: boolean | [] | {}) => {
  if (Array.isArray(result)) {
      return (
          <div>
              <ul>
                  {result.map((item, index) => (
                      <li key={index}>{item}</li>
                  ))}
              </ul>
          </div>
      );
  } else if (typeof result === 'object' && result !== null) {
      return (
          <div>
              <ul>
                  {Object.entries(result).map(([key, value]) => (
                      <li key={key}>{`${key}: ${value}`}</li>
                  ))}
              </ul>
          </div>
      );
  } else {
      return <div>{result.toString()}</div>;
  }
};

export { TaskType };
