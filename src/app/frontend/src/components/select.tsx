import React from 'react';
import Select from 'react-select';
import { Option } from '../models';

interface ModelSelectProps {
  onSelected: (selectedValue: string) => void;
  options: Option[];
  placeholder?: string;
}

const CustomSelect: React.FC<ModelSelectProps> = ({ onSelected, options, placeholder }) => {
  return (
    <Select
        classNamePrefix="select-model"
        className='w-80'
        options={options}
        placeholder= { placeholder ? placeholder : 'Model' }
        onChange={(option) => onSelected(option ? option.value : '')}
        required
    />
  );
};

export default CustomSelect;
