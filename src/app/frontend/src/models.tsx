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

  export type BaseInteraction = {
    token: string;
    description: string;
  }
  
  export type PredictRecommendation = BaseInteraction & {
    score: number;
  };

  export type PredictResult = {
    user_token: string;
    recommendations: PredictRecommendation[];
    past_interactions: BaseInteraction[];
  }
  
  export type PredictResponse = BaseResponse & {
    result: PredictResult;
  };
  
  export type EvaluateResponse = BaseResponse & {
    result: {};
  };

  export type ErrorResponse = BaseResponse & {
    result: {
      error: string;
    };
  };