import React from 'react';
import {Button} from 'react-bootstrap';

const ARC_C: React.FC = () => {
  
  const handleLink = () => {
    window.location.href = 'https://almaprism.com/';
  };

  return (
    <div>
      <h1 style={{ fontWeight: 'bold', fontSize: 40, textAlign: 'center' }}>Hands-On Training</h1>
      <p>ARC-C is a super cool irl game that incorporates the digital and real world of ARC through AR and sensor technology.</p>
      <div className="d-flex justify-content-center">
          <Button onClick={handleLink} style={{ width: '75%', maxWidth: '75%' }}>START HERE</Button>
      </div>
    </div>
  );
};

export default ARC_C;