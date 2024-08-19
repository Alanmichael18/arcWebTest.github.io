import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

import { HOST } from '../ARC_Config'
// const HOST = "http://localhost:8000";
// const HOST = "http://192.168.0.44:8000";

// Define interfaces for data structure
interface HeaderLabels {
  TAB_NAMES: {
    OVERVIEW: string;
  };
}

interface DocOnlyContent {
  OVERVIEW_INTRO: string[];
}

interface OverviewContent {
  COG_SUM: string[];
}

const Overview: React.FC = () => {
  const [headersLabels, setHeadersLabels] = useState<HeaderLabels | null>(null);
  const [docOnlyContent, setDocOnlyContent] = useState<DocOnlyContent | null>(null);
  const [overviewContent, setOverviewContent] = useState<OverviewContent | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [headerLabelsResponse, docOnlyContentResponse, overviewContentResponse] = await Promise.all([
          fetch(HOST + '/get-HeaderLabels'),
          fetch(HOST + '/get-DocOnlyContent'),
          fetch(HOST + '/get-OverviewContent')
        ]);

        const headerLabels: HeaderLabels = await headerLabelsResponse.json();
        setHeadersLabels(headerLabels);

        const docContent: DocOnlyContent = await docOnlyContentResponse.json();
        setDocOnlyContent(docContent);

        const overviewContent: OverviewContent = await overviewContentResponse.json();
        setOverviewContent(overviewContent);

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  if (!headersLabels) {
    return <div>Error fetching header labels...</div>;
  }
  if (!docOnlyContent || !overviewContent) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 style={{ fontWeight: 'bold', fontSize: 40, textAlign: 'center' }}>
        {headersLabels.TAB_NAMES.OVERVIEW}
      </h1>
      <div style={{ backgroundColor: 'lightblue', padding: '15px', borderRadius: '8px' }}>
        {docOnlyContent.OVERVIEW_INTRO.map((line, index) => (
          <ReactMarkdown key={index}>{line}</ReactMarkdown>
        ))}
      </div>
      <hr />
      <div>
        {overviewContent.COG_SUM.map((line, index) => (
          <ReactMarkdown key={index}>{line}</ReactMarkdown>
        ))}
      </div>
    </div>
  );
};

export default Overview;
