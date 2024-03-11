import React from 'react';
import Select from 'react-select';
import { Option } from '../api';

interface ModelSelectProps {
  onSelected: (selectedValue: string) => void;
  options: Option[];
  placeholder?: string;
}

const ModelSelect: React.FC<ModelSelectProps> = ({ onSelected, options, placeholder }) => {
  return (
    <Select
        classNamePrefix="select-model"
        className='min-w-52 flex-grow'
        options={options}
        placeholder= { placeholder ? placeholder : 'Select a model' }
        onChange={(option) => onSelected(option ? option.value : '')}
        required
    />
  );
};

export default ModelSelect;
