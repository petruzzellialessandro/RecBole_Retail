import React from 'react';
import { Helmet } from 'react-helmet';
import { ResultForm } from './forms/resultForm';
import { PredictForm } from './forms/predictForm';
import { EvaluateForm } from './forms/evaluateForm';
import { TrainForm } from './forms/trainForm';

export interface BtnProps {
  btnClass: string;
}

const App: React.FC = () => {
  const btnClass = 'btn w-32 px-3 py-2 bg-accent-500 text-white rounded hover:bg-accent-700 transition-colors duration-300 ease-in-out';

  return (
    <div className="w-4/5 m-auto font-mono">
      <Helmet>
        <title>RecBole Retail</title>
      </Helmet>
      <div className='flex flex-row items-center justify-between mt-10 mb-5'>
        <div className='p-5 float float-col'>
          <h1 className='font-bold'>Rec<span className='text-accent-500'>Sys</span></h1>
          <h3>for the Retail Industry</h3>
        </div>
        <div className='flex flex-col justify-end me-5 w-44'>
          <span className='flex justify-center text-sm'>Powered by</span>
          <img src={`${process.env.PUBLIC_URL}/logo.png`} alt="RecBole" className="flex flex-grow" />
        </div>
      </div>
      <ResultForm btnClass={btnClass} />
      <PredictForm btnClass={btnClass} />
      <EvaluateForm btnClass={btnClass} />
      <TrainForm btnClass={btnClass} />

      <div className='flex flex-col justify-center my-20'>
        <div className='flex justify-center text-md'>This software has been developed for the</div>
        <div className='flex justify-center font-bold text-lg my-4'>Semantics in Intelligent Information Access Course, Computer Science MSc Degree @UniBA</div>
        <div className='flex justify-center text-lg'>by Francesco Peragine</div>
      </div>
    </div>
  );
};

export default App;
