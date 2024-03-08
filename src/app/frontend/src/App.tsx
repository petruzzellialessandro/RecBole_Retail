import React from 'react';
import { Helmet } from 'react-helmet';
import { PredictForm } from './forms/predictForm';
import { EvaluateForm } from './forms/evaluateForm';
import { TrainForm } from './forms/trainForm';

export interface BtnProps {
  btnClass: string;
}

const App: React.FC = () => {
  const btnClass = 'btn w-32 px-3 py-2 bg-accent-500 text-white rounded hover:bg-accent-700 transition-colors duration-300 ease-in-out';

  return (
    <div className="container font-mono">
      <Helmet>
        <title>RecBole Retail</title>
      </Helmet>
      <div className='flex flex-row items-center justify-between'>
        <div className='p-5 float float-col'>
          <h1 className='font-bold'>Rec<span className='text-accent-500'>Sys</span></h1>
          <h3>for the Retail Industry</h3>
        </div>
        <div className='flex flex-col justify-end me-5 w-32'>
          <span className='flex justify-center font-bold text-sm'>Powered by</span>
          <img src={`${process.env.PUBLIC_URL}/logo.png`} alt="RecBole" className="flex flex-grow" />
        </div>
      </div>
      <PredictForm btnClass={btnClass} />
      <EvaluateForm btnClass={btnClass} />
      <TrainForm btnClass={btnClass} />
    </div>
  );
};

export default App;
