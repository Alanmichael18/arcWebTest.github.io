interface UserMetrics {
  MDS: Metric;
  TACR: Metric;
  SAD: Metric;
  SAV: Metric;
  [key: string]: Metric;
}

interface HeadersLabels {
  SECTION_NAMES: {
    FOR_DOCTORS: string;
  }
  TAB_NAMES: {
    PERSONALIZED_SUGGESTIONS: string;
  };
  SHOW: {
    BOOKMARK: string;
    ALL: string;
    KEPT: string;
  };
  MATCH_LEVEL: {
    TITLE: string;
  };
  SITUATIONS: {
    TITLE: string;
    GETTING_READY: string;
    ACADEMICS: string;
    FRIENDS_FAMILY: string;
    BEDTIME: string;
  };
  STRATEGY: {
    TITLE: string;
    EXTERNAL_AID: string;
    REFRAIM: string;
    RP: string;
    BA: string;
    SA: string;
  };
  ADVICE: string;
  RESET: string;
  UNKEEP: string;
  KEEP: string;
}

interface Metric {
  metricLayman: string;
  scoreRating: string;
}

interface AdviceIntroType {
  INTRO: string[];
}

interface Advice {
  [rowID: string]: {
    [key: string]: any;
    "Advice Title": string;
    "Advice Content": string;
    tags: Record<string, string>;
    "Match Level": string;
  };
}

import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Container, Row, Col, Button, Stack, Card, CardBody, CardText, CardFooter } from 'react-bootstrap';

import { HOST } from '../ARC_Config';
// const HOST = "http://localhost:8000";
// const HOST = "http://192.168.0.44:8000";

const PsychotherapySuggestions: React.FC = () => {
  const [UserMetrics, setUserMetrics] = useState<UserMetrics| null>(null);

  const [HeadersLabels, setHeadersLabels] = useState<HeadersLabels | null>(null);
  const [adviceLabels, setAdviceLabels] = useState<any>(null);

  const [AdviceIntro, setAdviceIntro] = useState<AdviceIntroType | null>(null);
  const [Advice, setAdvice] = useState<Advice>({});
  const [showKeeps, setShowKeeps] = useState<boolean>(false);
  const [keepList, setKeepList] = useState<{ [key: string]: boolean }>({});

  // Planning Ability
  const [MDS_none, setMDS_none] = useState<boolean>(true);
  const [MDS_low, setMDS_low] = useState<boolean>(false);
  const [MDS_high, setMDS_high] = useState<boolean>(false);

  // Adaptability
  const [TACR_none, setTACR_none] = useState<boolean>(true);
  const [TACR_low, setTACR_low] = useState<boolean>(false);
  const [TACR_high, setTACR_high] = useState<boolean>(false);

  // Inhibition
  const [SAD_none, setSAD_none] = useState<boolean>(true);
  const [SAD_low, setSAD_low] = useState<boolean>(false);
  const [SAD_high, setSAD_high] = useState<boolean>(false);

  // Working Memory
  const [SAV_none, setSAV_none] = useState<boolean>(true);
  const [SAV_low, setSAV_low] = useState<boolean>(false);
  const [SAV_high, setSAV_high] = useState<boolean>(false);

  // Situation Stuff
  const [AllSituations, setAllSituations] = useState<boolean>(true);
  const [GettingReady, setGettingReady] = useState<boolean>(false);
  const [Academics, setAcademics] = useState<boolean>(false);
  const [FriendsFamily, setFriendsFamily] = useState<boolean>(false);
  const [Bedtime, setBedtime] = useState<boolean>(false);

  useEffect(() => {
    fetch(HOST + '/get-UserMetrics')
      .then((response) => response.json())
      .then((data) => setUserMetrics(data))
      .catch((error) => console.error('Error fetching user metrics:', error));
    
    fetch(HOST + '/get-HeaderLabels')
      .then((response) => response.json())
      .then((HeadersLabels) => setHeadersLabels(HeadersLabels))
      .catch((error) => console.error('Error fetching data:', error));
    
    fetch(HOST + '/get-AdviceIntro')
      .then((response) => response.json())
      .then((AdviceIntro) => setAdviceIntro(AdviceIntro))
      .catch((error) => console.error('Error fetching data:', error));

    fetch(HOST + '/get-adviceLabels')
      .then((response) => response.json())
      .then((adviceLabels) => setAdviceLabels(adviceLabels))
      .catch((error) => console.error('Error fetching data:', error));

    const fetchAdviceData = async () => {
      try {
        const response = await fetch(HOST + '/get-Advice');
        const data = await response.json();
        setAdvice(data);
        
        const initialKeepList = Object.keys(data).reduce((acc, key) => {
          acc[key] = false;
          return acc;
        }, {} as { [key: string]: boolean });

        setKeepList(initialKeepList);
      } catch (error) {
        console.error('Error fetching advice data:', error);
      }
    };
    fetchAdviceData();
  }, []);

  if (!Advice || !UserMetrics || !HeadersLabels || !adviceLabels ||!AdviceIntro ) {
    return <div>Loading...</div>;
  }

  const keepAdvice = (rowID: string, value: boolean) => {
    setKeepList(prevKeepList => ({
      ...prevKeepList,
      [rowID]: value
    }));
  };

  const handleAllSituationsClick = () => {
    setAllSituations(true);
    setGettingReady(false);
    setAcademics(false);
    setFriendsFamily(false);
    setBedtime(false);
  };

  const handleSituationButtonClick = (setter: React.Dispatch<React.SetStateAction<boolean>>) => {
    setAllSituations(false);
    setter(prev => !prev);
  };

  const handleReset = () => {
    setShowKeeps(false);
    handleAllSituationsClick();

    setMDS_none(true);
    setMDS_low(false);
    setMDS_high(false);
    
    setTACR_none(true);
    setTACR_low(false);
    setTACR_high(false);
    
    setSAD_none(true);
    setSAD_low(false);
    setSAD_high(false);
    
    setSAV_none(true);
    setSAV_low(false);
    setSAV_high(false);
  };

  const filteredAdvice = Object.entries(Advice).filter(([rowID, row]) => {
    const keepCondition = !showKeeps || (showKeeps && keepList[rowID]);

    const MDSCondition = MDS_none || (MDS_low && row['MDS/Planning'] === 1) || (MDS_high && row['MDS/Planning'] === 2);
    const TACRCondition = TACR_none || (TACR_low && row['TACR/Adaptability'] === 1) || (TACR_high && row['TACR/Adaptability'] === 2);
    const SADCondition = SAD_none || (SAD_low && row['SAD/Inhibition'] === 1) || (SAD_high && row['SAD/Inhibition'] === 2);
    const SAVCondition = SAV_none || (SAV_low && row['SAV/WorkingMemory'] === 1) || (SAV_high && row['SAV/WorkingMemory'] === 2);
    const metricCondition = MDSCondition && TACRCondition && SADCondition && SAVCondition;

    const situationCondition = AllSituations || GettingReady || Academics || FriendsFamily || Bedtime ? (
      (AllSituations) || (GettingReady && row["Getting Ready"] >= 1) || (Academics && row["Academics"] >= 1) || (FriendsFamily && row["Friends/Family"] >= 1) || (Bedtime && row["Bedtime"] >= 1)
    ) : true;

    return keepCondition && metricCondition && situationCondition;
  });

  return (
    <div>
      <h1 style={{ fontWeight: 'bold', fontSize: 40, textAlign: 'center' }}>{HeadersLabels.SECTION_NAMES.FOR_DOCTORS}</h1>
      <div>
        {AdviceIntro.INTRO.map((line, index) => (
          <ReactMarkdown key={index}>
            {line}
          </ReactMarkdown>
        ))}
      </div>

      <Container fluid>

        <Row>
          <h4>{adviceLabels.SHOW.BOOKMARK}</h4>
        </Row>
        <Row className="mb-3">
          <Col>
            <Button
              variant={!showKeeps ? 'info' : 'outline-info'}
              onClick={() => setShowKeeps(false)}
              style={{ width: '20vw' }}
            >
              {adviceLabels.SHOW.ALL}
            </Button>
          </Col>
          <Col>
            <Button
              variant={showKeeps ? 'info' : 'outline-info'}
              onClick={() => setShowKeeps(true)}
              style={{ width: '20vw' }}
            >
              {adviceLabels.SHOW.KEPT}
            </Button>
          </Col>
        </Row>



        <Row>
          <h5>{UserMetrics.MDS.metricLayman} (MDS)</h5>
        </Row>
        <Row className="mb-3">
          <Col>
            <Button onClick={() => { setMDS_none(true); setMDS_low(false); setMDS_high(false); }} variant={MDS_none ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.N_A.replace('//', '/')}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => { setMDS_none(false); setMDS_low(true); setMDS_high(false); }} variant={MDS_low ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.LOW}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => { setMDS_none(false); setMDS_low(false); setMDS_high(true); }} variant={MDS_high ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.HIGH}
            </Button>
          </Col>
        </Row>

        <Row>
          <h5>{UserMetrics.TACR.metricLayman} (TACR)</h5>
        </Row>
        <Row className="mb-3">
          <Col>
            <Button onClick={() => { setTACR_none(true); setTACR_low(false); setTACR_high(false); }} variant={TACR_none ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.N_A.replace('//', '/')}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => { setTACR_none(false); setTACR_low(true); setTACR_high(false); }} variant={TACR_low ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.LOW}  
            </Button>
          </Col>
          <Col>
            <Button onClick={() => { setTACR_none(false); setTACR_low(false); setTACR_high(true); }} variant={TACR_high ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.HIGH}
            </Button>
          </Col>
        </Row>

        <Row>
          <h5>{UserMetrics.SAD.metricLayman} (SAD)</h5>
        </Row>
        <Row className="mb-3">
          <Col>
            <Button onClick={() => { setSAD_none(true); setSAD_low(false); setSAD_high(false); }} variant={SAD_none ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.N_A.replace('//', '/')}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => { setSAD_none(false); setSAD_low(true); setSAD_high(false); }} variant={SAD_low ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.LOW}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => { setSAD_none(false); setSAD_low(false); setSAD_high(true); }} variant={SAD_high ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.HIGH}  
            </Button>
          </Col>
        </Row>

        <Row>
          <h5>{UserMetrics.SAV.metricLayman} (SAV)</h5>
        </Row>
        <Row className="mb-3">
          <Col>
            <Button onClick={() => { setSAV_none(true); setSAV_low(false); setSAV_high(false); }} variant={SAV_none ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.N_A.replace('//', '/')}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => { setSAV_none(false); setSAV_low(true); setSAV_high(false); }} variant={SAV_low ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.LOW}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => { setSAV_none(false); setSAV_low(false); setSAV_high(true); }} variant={SAV_high ? 'info' : 'outline-info'} style={{ width: '12vw' }}>
              {adviceLabels.HIGH}
            </Button>
          </Col>
        </Row>



        <Row>
          <h4>{adviceLabels.SITUATIONS.TITLE}</h4>
        </Row>
        <Row className="mb-3">
          <Col className='col-1'>
            <Button onClick={handleAllSituationsClick} variant={AllSituations ? 'info' : 'outline-info'}>
              {adviceLabels.ALL}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => handleSituationButtonClick(setGettingReady)} variant={GettingReady ? 'info' : 'outline-info'}>
              {adviceLabels.SITUATIONS.GETTING_READY}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => handleSituationButtonClick(setAcademics)} variant={Academics ? 'info' : 'outline-info'}>
             {adviceLabels.SITUATIONS.ACADEMICS}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => handleSituationButtonClick(setFriendsFamily)} variant={FriendsFamily ? 'info' : 'outline-info'}>
              {adviceLabels.SITUATIONS.FRIENDS_FAMILY}
            </Button>
          </Col>
          <Col>
            <Button onClick={() => handleSituationButtonClick(setBedtime)} variant={Bedtime ? 'info' : 'outline-info'}>
              {adviceLabels.SITUATIONS.BED}
            </Button>
          </Col>
        </Row>

        <Row className='mb-3'>
            <Button onClick={handleReset} variant={AllSituations ? 'info' : 'outline-info'}>
              {adviceLabels.RESET}
            </Button>
        </Row>

      </Container>



      {filteredAdvice.map(([rowID, row]) => (
        <Stack gap={2} className="mx-auto mb-3" key={rowID}>
          <Card>
            <CardBody>
              <div className="d-flex justify-content-between align-items-center">
                <Card.Title className="mb-0">
                  <h3 className="mb-0">{row["Advice Title"]}</h3>
                </Card.Title>
                <Button
                  className={`btn-height-match ${keepList[rowID] ? 'btn-info' : 'btn-light'}`}
                  onClick={() => keepAdvice(rowID, !keepList[rowID])}
                >
                  {adviceLabels.KEEP}
                </Button>
              </div>
              <CardText>{row["Advice Content"]}</CardText>
            </CardBody>
            <CardFooter>
              {Object.entries(row["tags"]).map(([_, tag], j) => (
                <span key={j}><i>#{tag} </i></span>
              ))}
              <span>{row["Match Level"]}</span>
            </CardFooter>
          </Card>
        </Stack>
      ))}

    </div>
  );
};

export default PsychotherapySuggestions;