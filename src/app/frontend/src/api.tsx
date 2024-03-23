import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { BaseInteraction, ErrorResponse, EvaluateResponse, PredictRecommendation, PredictResponse, TaskStatus } from "./models";
import { faClipboard } from "@fortawesome/free-solid-svg-icons";

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

const fetchData = async (url: string) => {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

export const checkTaskStatus = async (taskId: string) => {
  const url = `${BACKEND_URL}/task-status/${taskId}`;
  return fetchData(url);
};

export const fetchTaskResult = async (taskId: string) => {
  const url = `${BACKEND_URL}/task-result/${taskId}`;
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
  setMessage: React.Dispatch<string>,
  setTaskResult: React.Dispatch<PredictResponse>
) => {
  try {
    const statusResponse = await checkTaskStatus(taskId);
    switch (statusResponse.status) {
      case TaskStatus.STARTED:
        setMessage('Task has started.');
        break;
        case TaskStatus.PENDING:
          setMessage('Task is not completed yet.');
          break;
          case TaskStatus.SUCCESS:
        const result = await fetchTaskResult(taskId);
        if (result) {
          setMessage('')
          setTaskResult(result);
        }
        break;
      case TaskStatus.FAILED:
        setMessage('Task failed.');
        break;
      default:
        setMessage('Status unknown.');
    }
  } catch (error) {
    setMessage(`Failed to fetch task result: ${error}`);
  }
};

export const renderResult = (result: boolean | [] | {}) => {
  const renderArray = (items: any[]) => (
    <ul>{items.map((item, index) => <li key={index}>{JSON.stringify(item)}</li>)}</ul>
  );

  const renderObject = (obj: object) => (
    <ul>{Object.entries(obj).map(([key, value]) => <li key={key}>{`${key}: ${JSON.stringify(value)}`}</li>)}</ul>
  );

  if (Array.isArray(result)) {
    return <div>{renderArray(result)}</div>;
  } else if (typeof result === 'object' && result !== null) {
    return <div>{renderObject(result)}</div>;
  } else {
    return <div>{result.toString()}</div>;
  }
};

export const renderResponse = (response: any) => {
  if((response as ErrorResponse).result.error) return renderErrorResponse((response));
  if((response as PredictResponse).result.recommendations) return renderPredictResponse(response);
  return renderEvaluateResponse(response);
};

export const renderErrorResponse = (response: ErrorResponse) => {
  return (
  <>
    <div className='col-span-2 font-bold text-lg'>Error:</div>
    <div className='col-span-7'>{response.result.error}</div>
  </>
  )
}

export const renderPredictResponse = (response: any) => {
  
  const renderInteractions = (interactions: BaseInteraction[]) => (
    <ul>
      {/* Token: {interaction.token}, Description: {interaction.description} */}
      {interactions.map((interaction, index) => (
        <li key={index}>{interaction.description}</li>
      ))}
    </ul>
  );

  const renderRecommendations = (recommendations: PredictRecommendation[]) => (
    <ul>
      {/* Token: {recommendation.token}, Description: {recommendation.description}, Score: {recommendation.score} */}
      {recommendations.map((recommendation, index) => (
        <li key={index}>
          {recommendation.description}
        </li>
      ))}
    </ul>
  );

  const renderPredict = (response: PredictResponse) => (
    <>
      <div className='col-span-2 font-bold text-lg'>Task Status:</div>
      <div className='col-span-7'>{response.status}</div>

      <div className='col-span-2 font-bold text-lg'>Recommendations:</div>
      <div className='col-span-7'>{renderRecommendations(response.result.recommendations)}</div>

      <div className='col-span-2 font-bold text-lg'>Past Interactions:</div>
      <div className='col-span-7'>{renderInteractions(response.result.past_interactions)}</div>
    </>
  );

  if ((response as ErrorResponse).result.error) {
    return renderErrorResponse(response as ErrorResponse)
  } else {
    return renderPredict(response as PredictResponse);
  }
};

export const renderEvaluateResponse = (response: EvaluateResponse) => {
  const renderObject = (obj: object) => (
    <ul>{Object.entries(obj).map(([key, value]) => <li key={key}>{`${key}: ${JSON.stringify(value)}`}</li>)}</ul>
  );

  return (
    <>
      <div className='col-span-2 font-bold text-lg'>Task Status:</div>
      <div className='col-span-7'>{response.status}</div>

      <div className='col-span-2 font-bold text-lg'>Metrics:</div>
      <div className='col-span-7'>{renderObject(response.result)}</div>
    </>
  );
}

export function copyToClipboard(text: string) {
  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (error) {
      console.log(`Error copying to clipboard: ${error}`);
    }
  };
  return (
    <span className="toClipboard" onClick={() => copyToClipboard(text)}>{text} <FontAwesomeIcon icon={faClipboard} /></span>
  )
}
