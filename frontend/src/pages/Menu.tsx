import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Nav, Tab, Table } from 'react-bootstrap';
import Plot from 'react-plotly.js';
import ReactMarkdown from 'react-markdown';
import 'bootstrap/dist/css/bootstrap.min.css'; // Ensure Bootstrap CSS is imported

// PAGES
import UserInfo from './UserInfo'; // Top header
import PsychotherapySuggestions from './PsychotherapySuggestions'; // Psychotherapy Suggestions Tab
import PersonalizedAdvice from './PersonalizedAdvice'; // Personalized Suggestions Tab
import Overview from './Overview'; // Overview Tab

// Temporarily Disabled
// import MetricsReport from './MetricsReport'; // ARC-T
// import AboutMetrics from './AboutMetrics'; // AboutMetrics
// import ARC_C from './ARC_C'; // ARC-C
// import ARC_T from './ARC_T'; // ARC-T

import { HOST } from '../ARC_Config';

// const HOST = "http://localhost:8000";
// const HOST = "http://192.168.0.44:8000";

// Define interfaces for data structure
interface HeaderLabels {
  SECTION_NAMES: {
    PERFORMANCE_PLOT: string;
    SCORE_TABLE: string;
    DATA_SUMMARY: string;
  };
  CHART_LABELS: {
    LINE_CHART: string;
    RADAR_CHART: string;
  };
  TABLE_LABELS: {
    METRIC: string;
    FULL_NAME: string;
    CODE: string;
    RAW_VALUE: string;
    AVERAGE: string;
    T_SCORE: string;
  };
  BUTTONS: {
    EXPORT_CSV: string;
  };
  TAB_NAMES: {
    OVERVIEW: string;
    PSYCHOTHERAPY_SUGGESTIONS: string;
    PERSONALIZED_SUGGESTIONS: string;
    ABOUT_METRICS: string;
  };
}

interface Metric {
  metricCode: string;
  symbol?: 'star' | 'diamond';
  metricLayman: string;
  metricFull: string;
  rawValue: number;
  metricAverage: number;
  tScore: number;
}

interface UserMetrics {
  [key: string]: Metric;
}

interface ChartData {
  data: any[];
  layout: any;
}

interface DataSummary {
  CONTENT: string[];
}

interface UserData {
  USER_NAME: string;
}

const Menu: React.FC = () => {
  const [key, setKey] = useState<string>('Results');
  const [key2, setKey2] = useState<string>('Overview');
  const [headersLabels, setHeadersLabels] = useState<HeaderLabels | null>(null);
  const [graph, setGraph] = useState<string>('LineChart');
  const [lineChartData, setLineChartData] = useState<ChartData | null>(null);
  // const [radarChartData, setRadarChartData] = useState<ChartData | null>(null);
  const [userData, setUserData] = useState<UserData | null>(null);
  const [userMetrics, setUserMetrics] = useState<UserMetrics | null>(null);
  const [dataSummary, setDataSummary] = useState<DataSummary | null>(null);
  const [aboutData, setAboutData] = useState<any | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch all data in parallel
        const [headerLabelsResponse, lineChartResponse, userDataResponse, userMetricsResponse, dataSummaryResponse, aboutDataResponse] = await Promise.all([
          fetch(`${HOST}/get-HeaderLabels`),
          fetch(`${HOST}/get-LineChart`),
          // fetch(`${HOST}/get-RadarChart`),
          fetch(`${HOST}/get-UserData`),
          fetch(`${HOST}/get-UserMetrics`),
          fetch(`${HOST}/get-dataSummary`),
          fetch(`${HOST}/get-AboutData`)
        ]);
  
        // Process responses
        const headerLabels: HeaderLabels = await headerLabelsResponse.json();
        setHeadersLabels(headerLabels);
  
        // Check if the chart data needs further parsing
        const lineChartData: ChartData = await lineChartResponse.json();
        setLineChartData(typeof lineChartData === 'string' ? JSON.parse(lineChartData) : lineChartData);
  
        // const radarChartData: ChartData = await radarChartResponse.json();
        // setRadarChartData(radarChartData);
  
        const userData: UserData = await userDataResponse.json();
        setUserData(userData);
  
        const userMetrics: UserMetrics = await userMetricsResponse.json();
        setUserMetrics(userMetrics);
  
        const dataSummary: DataSummary = await dataSummaryResponse.json();
        setDataSummary(dataSummary);
  
        const aboutData: any = await aboutDataResponse.json();
        setAboutData(aboutData);
  
        // Log data for debugging
        console.log("Line Chart Data: ", lineChartData);
        console.log("Header Labels: ", headerLabels);
  
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  
    fetchData();
  }, []);  

  // Ensure all state variables are initialized
  const activeKey = key ?? 'Results';
  const activeGraph = graph ?? 'LineChart';
  const activeTab = key2 ?? 'Overview';

  if (!headersLabels) {
    return <div>HeadersLabels Problem...</div>;
  }
  if (!lineChartData) {
    return <div>Loading LineChartData...</div>;
  }
  // if (!radarChartData) {
  //   return <div>Loading RadarChartData...</div>;
  // }
  if (!userData) {
    return <div>Loading UserData...</div>;
  }
  if (!userMetrics) {
    return <div>Loading UserMetrics...</div>;
  }
  if (!dataSummary) {
    return <div>Loading dataSummary...</div>;
  }
  if (!aboutData) {
    return <div>Loading AboutData...</div>;
  }

  const specificOrder = ["EFCS", "TACR", "MDS", "SAR", "SAD", "SAV"];
  const metricsArray = Object.entries(userMetrics)
    .map(([key, value]) => ({ ...value, metricCode: key }))
    .sort((a, b) => specificOrder.indexOf(a.metricCode) - specificOrder.indexOf(b.metricCode));

  const downloadCSV = async () => {
    try {
      const response = await fetch(`${HOST}/download/UserMetrics`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${userData.USER_NAME}_UserMetrics.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading the file:', error);
    }
  };

  return (
    <div style={{ position: 'fixed', left: 5, top: 5, margin: '2vw', width: '97%' }}>
      <Container fluid>
        <Row className="justify-content-between" style={{ width: '100vw' }}>
          <UserInfo />
        </Row>
        <Row className="justify-content-between">
          <Col className='col-6'>
            <div style={{ overflowX: 'auto' }}>
              <Tab.Container id="menu-tabs" activeKey={activeKey} onSelect={(k) => setKey(k ?? 'Results')}>
                <Tab.Content style={{ height: '75vh', overflowY: 'auto' }}>
                  <Tab.Pane eventKey="Results">
                    <div>
                      <h2>{headersLabels.SECTION_NAMES.PERFORMANCE_PLOT}</h2>
                      <Container>
                        <Row>
                          <Col>
                            <Tab.Container id="charts" activeKey={activeGraph} onSelect={(g) => setGraph(g ?? 'LineChart')}>
                              <Nav variant="tabs" style={{ fontSize: 16 }}>
                                <Nav.Item>
                                  <Nav.Link eventKey="LineChart">{headersLabels.CHART_LABELS.LINE_CHART}</Nav.Link>
                                </Nav.Item>
                                {/* <Nav.Item>
                                  <Nav.Link eventKey="RadarChart">{headersLabels.CHART_LABELS.RADAR_CHART}</Nav.Link>
                                </Nav.Item> */}
                              </Nav>
                              <Tab.Content>
                                <Tab.Pane eventKey="LineChart">
                                  <Plot
                                    data={lineChartData.data}
                                    layout={lineChartData.layout}     
                                    style={{ width: '100%', height: '100%' }}
                                    useResizeHandler={true}
                                  />
                                </Tab.Pane>
                                {/* <Tab.Pane eventKey="RadarChart">
                                  <Plot
                                    data={radarChartData.data}
                                    layout={radarChartData.layout}
                                    style={{ width: '100%', height: '100%' }}
                                    useResizeHandler={true}
                                  />
                                </Tab.Pane> */}
                              </Tab.Content>
                            </Tab.Container>
                          </Col>
                        </Row>
                      </Container>
                      <hr />
                      <Container>
                        <h2>{headersLabels.SECTION_NAMES.SCORE_TABLE}</h2>
                        <a href="#download" onClick={downloadCSV} style={{ float: 'right' }}>
                          <u><b>{headersLabels.BUTTONS.EXPORT_CSV}</b></u>
                        </a>
                        <Table hover style={{ fontSize: '14px' }}>
                          <thead>
                            <tr>
                              <th></th>
                              <th style={{ width: '40px' }}>{headersLabels.TABLE_LABELS.METRIC}</th>
                              <th>{headersLabels.TABLE_LABELS.FULL_NAME}</th>
                              <th>{headersLabels.TABLE_LABELS.CODE}</th>
                              <th>{headersLabels.TABLE_LABELS.RAW_VALUE}</th>
                              <th>{headersLabels.TABLE_LABELS.AVERAGE}</th>
                              <th>{headersLabels.TABLE_LABELS.T_SCORE}</th>
                            </tr>
                          </thead>
                          <tbody>
                            {metricsArray.map((metric) => (
                              <tr key={metric.metricCode}
                                  style={{
                                    borderTop: metric.metricCode === 'EFCS' ? '3px solid black' : '1px solid lightgray',
                                    borderBottom: metric.metricCode === 'EFCS' || metric.metricCode === 'MDS' ? '3px solid black' : '1px solid lightgray',
                                  }}>
                                {/* Symbol column */}
                                <td style={{ width: '40px', textAlign: 'center' }}>
                                  {metric.symbol === 'star' && '★'}
                                  {metric.symbol === 'diamond' && '♦'}
                                </td>
                                <td style={{ backgroundColor: metric.tScore < 40 ? 'rgba(243, 224, 124, 0.3)' : metric.tScore > 60 ? 'rgba(165, 243, 124, 0.3)' : 'transparent' }}>
                                  {metric.metricLayman}
                                </td>
                                <td>{metric.metricFull}</td>
                                <td>{metric.metricCode}</td>
                                <td>{metric.rawValue}</td>
                                <td>{metric.metricAverage}</td>
                                <td>{metric.tScore}</td>
                              </tr>
                            ))}
                          </tbody>
                        </Table>
                      </Container>
                      <hr />
                      <h2>{headersLabels.SECTION_NAMES.DATA_SUMMARY}</h2>
                      <div>
                        {dataSummary.CONTENT.map((line, index) => (
                          <ReactMarkdown key={index}>{line}</ReactMarkdown>
                        ))}
                      </div>
                    </div>
                  </Tab.Pane>
                </Tab.Content>
              </Tab.Container>
            </div>
          </Col>
          
          <Col className='col-6'>
            <Container fluid>
              <Tab.Container id="Actions" activeKey={activeTab} onSelect={(k) => setKey2(k ?? 'Overview')}>
                <Row>
                  <Col>
                    <Nav variant="tabs" style={{ fontSize: 16 }}>
                      <Nav.Item>
                        <Nav.Link eventKey="Overview">{headersLabels.TAB_NAMES.OVERVIEW}</Nav.Link>
                      </Nav.Item>
                      <Nav.Item>
                        <Nav.Link style={{ backgroundColor: 'rgb(135, 255, 105)' }} eventKey="PsychotherapySuggestions">{headersLabels.TAB_NAMES.PSYCHOTHERAPY_SUGGESTIONS}</Nav.Link>
                      </Nav.Item>
                      <Nav.Item>
                        <Nav.Link style={{ backgroundColor: 'rgb(255, 145, 237)' }} eventKey="PersonalizedAdvice">{headersLabels.TAB_NAMES.PERSONALIZED_SUGGESTIONS}</Nav.Link>
                      </Nav.Item>
                      {/* <Nav.Item>
                        <Nav.Link eventKey="MetricsReport">Report</Nav.Link>
                      </Nav.Item>
                      <Nav.Item>
                        <Nav.Link eventKey="AboutMetrics">{headersLabels.TAB_NAMES.ABOUT_METRICS}</Nav.Link>
                      </Nav.Item>
                      <Nav.Item>
                        <Nav.Link eventKey="ARC_C">ARC-C</Nav.Link>
                      </Nav.Item>
                      <Nav.Item>
                        <Nav.Link eventKey="ARC_T">ARC-T</Nav.Link>
                      </Nav.Item> */}
                    </Nav>
                  </Col>
                </Row>
                <div style={{ overflowX: 'auto', whiteSpace: 'nowrap' }}>
                </div>
                <Row>
                  <Col>
                    <Tab.Content style={{ height: '80vh', overflowY: 'auto' }}>
                      <Tab.Pane eventKey="Overview">
                        <Overview />
                      </Tab.Pane>
                      <Tab.Pane eventKey="PsychotherapySuggestions">
                        <PsychotherapySuggestions />
                      </Tab.Pane>
                      <Tab.Pane eventKey="PersonalizedAdvice">
                        <PersonalizedAdvice />
                      </Tab.Pane>
                      {/* <Tab.Pane eventKey="MetricsReport">
                        <MetricsReport />
                      </Tab.Pane>
                      <Tab.Pane eventKey="AboutMetrics">
                        <AboutMetrics />
                      </Tab.Pane>
                      <Tab.Pane eventKey="ARC_C">
                        <ARC_C />
                      </Tab.Pane>
                      <Tab.Pane eventKey="ARC_T">
                        <ARC_T />
                      </Tab.Pane> */}
                    </Tab.Content>
                  </Col>
                </Row>
              </Tab.Container>
            </Container>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Menu;
