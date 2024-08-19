import React, { useEffect, useState } from 'react';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import ReactMarkdown from 'react-markdown';

// Define types for better TypeScript support
interface UserMetric {
  metricLayman: string;
  metricFull: string;
  rawValue: number;
  zScore: number;
  score_rating: string;
}

interface MetricReport {
  REPORT: string[];
  COLOR: string;
}

interface MetricData {
  [key: string]: UserMetric;
}

interface ReportData {
  [key: string]: MetricReport;
}

import { HOST } from '../ARC_Config';

// const HOST = "http://localhost:8000";
// const HOST = "http://192.168.0.44:8000";

const METRICS = ["EFCS", "TACR", "MDS", "SAR", "SAD", "SAV"];

const MetricsReport: React.FC = () => {
  const [UserMetrics, setUserMetrics] = useState<MetricData | null>(null);
  const [MetricReport, setMetricReport] = useState<ReportData | null>(null);

  useEffect(() => {
    fetch(HOST + '/get-UserMetrics')
      .then((response) => response.json())
      .then((data) => setUserMetrics(data))
      .catch((error) => console.error('Error fetching UserMetrics:', error));

    fetch(HOST + '/get-MetricReport')
      .then((response) => response.json())
      .then((data) => setMetricReport(data))
      .catch((error) => console.error('Error fetching MetricReport:', error));
  }, []);

  if (!UserMetrics || !MetricReport) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 style={{ fontWeight: 'bold', fontSize: 40, textAlign: 'center' }}>Metrics Report</h1>
      {METRICS.map((metric) => {
        const metricData = UserMetrics[metric];
        const reportData = MetricReport[metric];

        // Add a check for undefined data
        if (!metricData || !reportData) {
          return null; // skip rendering if data is missing
        }

        return (
          <Card key={metric} className="mb-3">
            <Card.Header as="h4">
                {metricData.metricLayman} ({metric}, {metricData.metricFull})
            </Card.Header>
            <ListGroup variant="flush">
              <ListGroup.Item>
                <span>
                  <strong>Score: {metricData.rawValue}, Z-Score: {metricData.zScore}, 
                  <span style={{ color: reportData.COLOR }}> {metricData.score_rating}</span></strong> 
                </span>
                <br></br>
                <div>
                  {reportData.REPORT.map((line, index) => (
                    <ReactMarkdown key={index}>{line}</ReactMarkdown>
                  ))}
                </div>
              </ListGroup.Item>
            </ListGroup>
          </Card>
        );
      })}
    </div>
  );
};

export default MetricsReport;