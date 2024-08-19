import React, { useEffect, useState } from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import { Stack } from 'react-bootstrap';

import Notes from './Notes';
// import { HOST } from './ARC_Config.js'
import { HOST } from '../ARC_Config';

// const HOST = "http://localhost:8000";
// const HOST = HOST;

// Define types for your data
interface UserData {
  USER_NAME: string;
  USER_DOB: string;
  USER_AGE: number;
  USER_SEX: string;
  SESSION_DATE: string;
  TIME_SINCE: string;
  SESSION_ID: number;
  PLAYER_ID: number;
}

interface HeaderLabels {
  DEMOGRAPHICS: {
    DOB: string;
    AGE: string;
    SEX: string;
    SESS_DATE: string;
    SESS_ID: string;
    PLAYER_ID: string;
  };
  BUTTONS: {
    PRINT_REPORT: string;
    ADD_SESSION: string;
  };
}

const DEFAULT_USER_DATA: UserData = {
  USER_NAME: "Alan",
  USER_DOB: "2012",
  USER_AGE: 21,
  USER_SEX: "M",
  SESSION_DATE: "2012",
  TIME_SINCE: "2012",
  SESSION_ID: 52418964157,
  PLAYER_ID: 15241868411,
};

const UserInfo: React.FC = () => {
  const [userData, setUserData] = useState<UserData>(DEFAULT_USER_DATA);
  const [headersLabels, setHeadersLabels] = useState<HeaderLabels | null>(null);

  const [isLeft, setIsLeft] = useState<boolean>(false);

  const moveLeft = () => {
    setIsLeft(prevState => !prevState);
  };

  useEffect(() => {
    fetch(`${HOST}/get-UserData`)
      .then(response => response.json())
      .then((data: UserData) => setUserData(data))
      .catch(error => console.error('Error fetching user data:', error));

    fetch(`${HOST}/get-HeaderLabels`)
      .then(response => response.json())
      .then((data: HeaderLabels) => setHeadersLabels(data))
      .catch(error => console.error('Error fetching header labels:', error));
  }, []);

  if (!headersLabels) {
    return <div>Loading...</div>;
  }

  return (
    <div className="UserInfo">
      <Container>
        <Row>
          <Col className='col-3'>
            <h1 style={{fontWeight: 'bold', fontSize: 64}}>{userData.USER_NAME}</h1>
          </Col>
          <Col className='col-3'>
            <p>
              {headersLabels.DEMOGRAPHICS.DOB}: <b>{userData.USER_DOB}</b> <br />
              {headersLabels.DEMOGRAPHICS.AGE}: <b>{userData.USER_AGE}</b> <br />
              {headersLabels.DEMOGRAPHICS.SEX}: <b>{userData.USER_SEX}</b>
            </p>
          </Col>
          <Col className='col-4'>
            <p>
              {headersLabels.DEMOGRAPHICS.SESS_DATE}: <b>{userData.SESSION_DATE}</b> ({userData.TIME_SINCE} months ago) <br />
              {headersLabels.DEMOGRAPHICS.SESS_ID}: <b>{userData.SESSION_ID}</b> <br />
              {headersLabels.DEMOGRAPHICS.PLAYER_ID}: <b>{userData.PLAYER_ID}</b>
            </p>
          </Col>
          <Col className='col-2' style={{alignSelf: 'flex-start'}}>
            <Stack gap={1}>
              <Button variant="dark">{headersLabels.BUTTONS.PRINT_REPORT}</Button>
              <Button variant="dark">{headersLabels.BUTTONS.ADD_SESSION}</Button>
            </Stack>
          </Col>
        </Row>
      </Container>

      <div style={{
        position: 'fixed',
        right: isLeft ? 'auto' : '10px',
        left: isLeft ? '10px' : 'auto',
        bottom: '10px',
        zIndex: 1000,
      }}>
        <Button
          className={`arrow-btn ${isLeft ? 'right' : 'left'} no-underline`}
          onClick={moveLeft}
          variant='link'
          style={{
            position: 'absolute',
            top: '50%',
            transform: 'translateY(-50%)',
            right: isLeft ? '-10px' : 'auto',
            left: isLeft ? 'auto' : '-10px',
            zIndex: 1001,
          }}
        >
          {isLeft ? '→' : '←'}
        </Button>
        <Notes />
      </div>
    </div>
  );
};

export default UserInfo;
