import React, { ChangeEventHandler } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloudArrowUp } from "@fortawesome/free-solid-svg-icons";

interface InputFileProps {
    onFileSelect: (selectedValue: File) => void;
}

const InputFile: React.FC<InputFileProps> = ({ onFileSelect }) => {
    const onSelected: ChangeEventHandler<HTMLInputElement> = (event) => {
        if (event.target.files && event.target.files.length > 0) {
          onFileSelect(event.target.files[0]);
        }
      };
      
    return (
    <label className='flex-grow relative'>
    <input type="file" name="file" className='w-full top-0 left-0 flex-grow' onChange={onSelected} required />
    <FontAwesomeIcon icon={faCloudArrowUp} className=''/> Upload file
  </label>
  );
};

export default InputFile;
