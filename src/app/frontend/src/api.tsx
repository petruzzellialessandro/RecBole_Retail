const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export interface TaskStatusResponse {
  status: 'pending' | 'completed' | 'failed' | 'unknown';
  message?: string;
}

const fetchData = async (url: string) => {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

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