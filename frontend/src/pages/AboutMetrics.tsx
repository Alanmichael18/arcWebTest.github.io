import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';

import ReactMarkdown from 'react-markdown';
import { HOST } from '../ARC_Config';

// const HOST = "http://localhost:8000";
// const HOST = "http://192.168.0.44:8000";

const BLANK_DICT = {'one': '1', 'two':'2'};
const DEFAULT_DICT = {'EFCS': BLANK_DICT, 'TACR':BLANK_DICT, 'MDS':BLANK_DICT, 'SAV':BLANK_DICT, 'SAR':BLANK_DICT, 'SAD':BLANK_DICT, "ABOUT_METRICS":"HI"};

const AboutMetrics: React.FC = () => {
  const [AboutData, setAboutData] = useState(DEFAULT_DICT);

  useEffect(() => {
    fetch(HOST + '/get-AboutData')
      .then((response) => response.json())
      .then((AboutData) => setAboutData(AboutData))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);
  if (!AboutData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 style={{ fontWeight: 'bold', fontSize: 40, textAlign: 'center' }}>About Metrics</h1>
      <Card style={{width: '45vw'}}>
        <ListGroup>
          <ListGroup.Item>
          {Object.entries(AboutData.EFCS || {}).map(([_, line], index) => (
              <ReactMarkdown key={index}>
                  {line}
              </ReactMarkdown>
          ))}
          </ListGroup.Item>

          <ListGroup.Item >
          {Object.entries(AboutData.TACR || {}).map(([_, line], index) => (
              <ReactMarkdown key={index}>
                  {line}
              </ReactMarkdown>
          ))}
          </ListGroup.Item>
          
          <ListGroup.Item>
          {Object.entries(AboutData.MDS || {}).map(([_, line], index) => (
              <ReactMarkdown key={index}>
                  {line}
              </ReactMarkdown>
          ))}
          </ListGroup.Item>

          <ListGroup.Item>
          {Object.entries(AboutData.SAR || {}).map(([_, line], index) => (
              <ReactMarkdown key={index}>
                  {line}
              </ReactMarkdown>
          ))}
          </ListGroup.Item>

          <ListGroup.Item>
          {Object.entries(AboutData.SAD || {}).map(([_, line], index) => (
              <ReactMarkdown key={index}>
                  {line}
              </ReactMarkdown>
          ))}
          </ListGroup.Item>
          
          <ListGroup.Item>
          {Object.entries(AboutData.SAV || {}).map(([_, line], index) => (
              <ReactMarkdown key={index}>
                  {line}
              </ReactMarkdown>
          ))}
          </ListGroup.Item>
        </ListGroup>
      </Card>
    </div>
  );
};

export default AboutMetrics;