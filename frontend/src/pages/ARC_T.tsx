import React from 'react';
import {Button} from 'react-bootstrap';

const ARC_T: React.FC = () => {
  
  const handleLink = () => {
    window.location.href = 'https://almaprism.com/';
  };

  return (
    <div>
      <h1 style={{ fontWeight: 'bold', fontSize: 40, textAlign: 'center' }}>Game-Based Training</h1>
      <p>ARC-T is a super cool 20-day extension of ARC game that uses CUTTING EDGE game design and medical knowledge to help your kid!</p>
      <div className="d-flex justify-content-center">
          <Button onClick={handleLink} style={{ width: '75%', maxWidth: '75%' }}>START HERE</Button>
      </div>
    </div>
  );
};

export default ARC_T;