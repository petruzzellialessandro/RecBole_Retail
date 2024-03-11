import React, { useState, ChangeEventHandler } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloudArrowUp } from "@fortawesome/free-solid-svg-icons";

interface InputFileProps {
    onFileSelect: (selectedValue: File) => void;
}

const InputFile: React.FC<InputFileProps> = ({ onFileSelect }) => {
    const [fileName, setFileName] = useState<string | null>(null);

    const onSelected: ChangeEventHandler<HTMLInputElement> = (event) => {
        if (event.target.files && event.target.files.length > 0) {
            const selectedFile = event.target.files[0];
            onFileSelect(selectedFile);
            setFileName(selectedFile.name);
        }
    };
      
    return (
        <label className='flex-grow relative cursor-pointer'>
            <input type="file" name="file" className='w-full top-0 left-0 absolute opacity-0 cursor-pointer' onChange={onSelected} required />
            <FontAwesomeIcon icon={faCloudArrowUp} className='mr-2'/>
            {fileName ? `File: ${fileName}` : 'File'} 
        </label>
    );
};

export default InputFile;
