import React from 'react';
import Select from 'react-select';

const models = [
  { value: 'Bert4Rec', label: 'Bert4Rec' },
  { value: 'Caser', label: 'Caser' },
  { value: 'GRU4Rec', label: 'GRU4Rec' },
  { value: 'TransRec', label: 'TransRec' },
];

interface ModelSelectProps {
  onSelected: (selectedValue: string) => void;
}

const ModelSelect: React.FC<ModelSelectProps> = ({ onSelected }) => {
  return (
    <Select
        classNamePrefix="select-model"
        className='min-w-52 flex-grow'
        options={models}
        placeholder="Select a model"
        onChange={(option) => onSelected(option ? option.value : '')}
        required
    />
  );
};

export default ModelSelect;
