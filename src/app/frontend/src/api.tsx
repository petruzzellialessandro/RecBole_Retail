export enum TaskType {
  PREDICT = "predict",
  TRAIN = "train",
  EVALUATE = "evaluate",
}

export interface Option {
  value: string;
  label: string;
}

export const TASK_TYPES: Option[] = [
  { value: TaskType.PREDICT, label: 'Predict' },
  { value: TaskType.TRAIN, label: 'Train' },
  { value: TaskType.EVALUATE, label: 'Evaluate' },
];

export const MODELS: Option[] = [
  { value: 'Bert4Rec', label: 'Bert4Rec' },
  { value: 'Caser', label: 'Caser' },
  { value: 'GRU4Rec', label: 'GRU4Rec' },
  { value: 'TransRec', label: 'TransRec' },
];

export enum TaskStatus {
  STARTED = 'STARTED',
  PENDING = 'PENDING',
  SUCCESS = 'SUCCESS',
  FAILED = 'FAILURE',
  UNKNOWN = 'unknown',
}

export type BaseResponse = {
  status: TaskStatus;
  task_id: string;
};

export type PredictResponse = {
  status: TaskStatus;
  task_id: string;
  result: [];
};

export type EvaluateResponse = {
  status: TaskStatus;
  task_id: string;
  result: {};
};

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

// export const checkTaskStatus = async (task: string, taskId: string): Promise<any> => {
//   const checkStatus = async (resolve: any, reject: any) => {
//     try {
//       const response = await fetchData(`${BACKEND_URL}/${task}/task-status/${taskId}`);
//       if (response.status === TaskStatus.SUCCESS || response.status === TaskStatus.FAILED) {
//         resolve(response);
//       } else {
//         setTimeout(() => checkStatus(resolve, reject), 5000);
//       }
//     } catch (error) {
//       reject(error);
//     }
//   };

//   return new Promise(checkStatus);
// };

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
      // default:
      //   setErrorMessage('Status unknown: ' + statusResponse.status);
    }
  } catch (error) {
    setErrorMessage(`Failed to fetch task result: ${error}`);
  }
};