import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Container, Row, Col, Button, Stack, Card } from 'react-bootstrap';

import { HOST } from '../ARC_Config'
// const HOST = "http://localhost:8000";
// const HOST = "http://192.168.0.44:8000";

interface HeaderLabels {
  TAB_NAMES: {
    PERSONALIZED_SUGGESTIONS: string;
  }
}

interface AdviceIntroType {
  INTRO: string[];
}

interface AdviceType {
  [key: string]: {
    "Advice Title": string;
    "Advice Content": string;
    "Match Level": number;
    "Getting Ready": number;
    "Academics": number;
    "Friends/Family": number;
    "Bedtime": number;
    "External Aids": number;
    "Reframing": number;
    "Role Playing": number;
    "Behavior Activation": number;
    "Successive Approximation": number;
  };
}

const DEFAULT_ADVICE_DICT: AdviceType = {};

const PersonalizedAdvice: React.FC = () => {
  const [HeaderLabels, setHeaderLabels] = useState<HeaderLabels | null>(null);
  const [adviceLabels, setAdviceLabels] = useState<{ [key: string]: any } | null>(null);

  const [AdviceIntro, setAdviceIntro] = useState<AdviceIntroType | null>(null);
  const [Advice, setAdvice] = useState<AdviceType>(DEFAULT_ADVICE_DICT);

  const [showKeeps, setShowKeeps] = useState(false);
  const [keepList, setKeepList] = useState<{ [key: string]: boolean }>({});

  const [AllStars, setAllStars] = useState(true);
  const [match1, setMatch1] = useState(false);
  const [match2, setMatch2] = useState(false);
  const [match3, setMatch3] = useState(false);

  const [AllSituations, setAllSituations] = useState(true);
  const [GettingReady, setGettingReady] = useState(false);
  const [Academics, setAcademics] = useState(false);
  const [FriendsFamily, setFriendsFamily] = useState(false);
  const [Bedtime, setBedtime] = useState(false);

  const [AllTags, setAllTags] = useState(true);
  const [ExternalAids, setExternalAids] = useState(false);
  const [Reframing, setReframing] = useState(false);
  const [RolePlaying, setRolePlaying] = useState(false);
  const [BehaviorActivation, setBehaviorActivation] = useState(false);
  const [SuccessiveApproximation, setSuccessiveApproximation] = useState(false);

  const keepAdvice = (rowID: string, value: boolean) => {
    setKeepList(prevKeepList => ({
      ...prevKeepList,
      [rowID]: value,
    }));
  };

  const handleAllTagsClick = () => {
    setAllTags(true);
    setExternalAids(false);
    setReframing(false);
    setRolePlaying(false);
    setBehaviorActivation(false);
    setSuccessiveApproximation(false);
  };

  const handleTagButtonClick = (setter: React.Dispatch<React.SetStateAction<boolean>>) => {
    setAllTags(false);
    setter(prev => !prev);
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

  const handleAllStarsClick = () => {
    setAllStars(true);
    setMatch1(false);
    setMatch2(false);
    setMatch3(false);
  };

  const handleStarButtonClick = (setter: React.Dispatch<React.SetStateAction<boolean>>) => {
    setAllStars(false);
    setter(prev => !prev);
  };

  const handleReset = () => {
    setShowKeeps(false);
    handleAllStarsClick();
    handleAllSituationsClick();
    handleAllTagsClick();
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const HeaderLabelsResponse = await fetch(HOST + '/get-HeaderLabels');
        const HeaderLabels: HeaderLabels = await HeaderLabelsResponse.json();
        setHeaderLabels(HeaderLabels);

        const adviceLabelsResponse = await fetch(HOST + '/get-adviceLabels');
        const adviceLabels = await adviceLabelsResponse.json();
        setAdviceLabels(adviceLabels);

        const adviceIntroResponse = await fetch(HOST + '/get-AdviceIntro');
        const AdviceIntro: AdviceIntroType = await adviceIntroResponse.json();
        setAdviceIntro(AdviceIntro);

        const adviceResponse = await fetch(HOST + '/get-Advice');
        const data: AdviceType = await adviceResponse.json();
        setAdvice(data);

        const initialKeepList = Object.keys(data).reduce((acc, key) => {
          acc[key] = false;
          return acc;
        }, {} as { [key: string]: boolean });

        setKeepList(initialKeepList);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  if (!Advice) {
    return <div>Loading Advice...</div>;
  }
  
  if (!HeaderLabels) {
    return <div>Loading Header Labels...</div>;
  }
  
  if (!adviceLabels) {
    return <div>Loading Advice Labels...</div>;
  }
  
  if (!AdviceIntro) {
    return <div>Loading Advice Introduction...</div>;
  } 

  const filteredAdvice = Object.entries(Advice).filter(([rowID, row]) => {
    const keepCondition = !showKeeps || (showKeeps && keepList[rowID]);

    const matchCondition = AllStars || match1 || match2 || match3 ? (
      AllStars || (match1 && row["Match Level"] === 1) || (match2 && row["Match Level"] === 2) || (match3 && row["Match Level"] === 3)
    ) : true;

    const situationCondition = AllSituations || GettingReady || Academics || FriendsFamily || Bedtime ? (
      AllSituations || (GettingReady && row["Getting Ready"] >= 1) || (Academics && row["Academics"] >= 1) || (FriendsFamily && row["Friends/Family"] >= 1) || (Bedtime && row["Bedtime"] >= 1)
    ) : true;

    const tagCondition = AllTags || ExternalAids || Reframing || RolePlaying || BehaviorActivation || SuccessiveApproximation ? (
      AllTags || (ExternalAids && row["External Aids"] >= 1) || (Reframing && row["Reframing"] >= 1) || (RolePlaying && row["Role Playing"] >= 1) || (BehaviorActivation && row["Behavior Activation"] >= 1) || (SuccessiveApproximation && row["Successive Approximation"] >= 1)
    ) : true;

    return keepCondition && matchCondition && situationCondition && tagCondition;
  });

  return (
    <div>
      <h1 style={{ fontWeight: 'bold', fontSize: 40, textAlign: 'center' }}>{HeaderLabels.TAB_NAMES.PERSONALIZED_SUGGESTIONS}</h1>
      {AdviceIntro.INTRO.map((line, index) => (
        <ReactMarkdown key={index}>
          {line}
        </ReactMarkdown>
      ))}
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
          <h4>{adviceLabels.MATCH_LEVEL.TITLE}</h4>
        </Row>
        <Row style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={handleAllStarsClick}
              variant={AllStars ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.ALL}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleStarButtonClick(setMatch1)}
              variant={match1 ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              ★
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleStarButtonClick(setMatch2)}
              variant={match2 ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              ★★
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleStarButtonClick(setMatch3)}
              variant={match3 ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              ★★★
            </Button>
          </Col>
        </Row>
        <Row className="mt-3">
          <h4>{adviceLabels.SITUATIONS.TITLE}</h4>
        </Row>
        <Row style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={handleAllSituationsClick}
              variant={AllSituations ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.ALL}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleSituationButtonClick(setGettingReady)}
              variant={GettingReady ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.SITUATIONS.GETTING_READY}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleSituationButtonClick(setAcademics)}
              variant={Academics ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.SITUATIONS.ACADEMICS}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleSituationButtonClick(setFriendsFamily)}
              variant={FriendsFamily ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.SITUATIONS.FRIENDS_FAMILY}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleSituationButtonClick(setBedtime)}
              variant={Bedtime ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.SITUATIONS.BEDTIME}
            </Button>
          </Col>
        </Row>
        <Row className="mt-3">
          <h4>{adviceLabels.STRATEGY.TITLE}</h4>
        </Row>
        <Row style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={handleAllTagsClick}
              variant={AllTags ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.ALL}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleTagButtonClick(setExternalAids)}
              variant={ExternalAids ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.STRATEGY.EXTERNAL_AID}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleTagButtonClick(setReframing)}
              variant={Reframing ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.STRATEGY.REFRAME}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleTagButtonClick(setRolePlaying)}
              variant={RolePlaying ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.STRATEGY.RP}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleTagButtonClick(setBehaviorActivation)}
              variant={BehaviorActivation ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.STRATEGY.BA}
            </Button>
          </Col>
          <Col style={{ flex: 1, padding: '0 5px' }}>
            <Button
              onClick={() => handleTagButtonClick(setSuccessiveApproximation)}
              variant={SuccessiveApproximation ? 'info' : 'outline-info'}
              style={{ width: '100%' }}
            >
              {adviceLabels.STRATEGY.SA}
            </Button>
          </Col>
        </Row>
        <Row className="mt-4">
          <h4>{adviceLabels.ADVICE}</h4>
        </Row>
        <Row>
          <Button onClick={handleReset} variant="warning">{adviceLabels.RESET}</Button>
        </Row>
        <Row>
          <Stack gap={3} className="mt-3">
            {filteredAdvice.map(([rowID, row]) => (
              <Card key={rowID}>
                <Card.Header>
                  <Stack direction="horizontal" gap={3}>
                    <div>{row["Advice Title"]}</div>
                    <Button
                      onClick={() => keepAdvice(rowID, !keepList[rowID])}
                      variant={keepList[rowID] ? 'success' : 'outline-success'}
                      style={{ marginLeft: 'auto' }}
                    >
                      {keepList[rowID] ? adviceLabels.UNKEEP : adviceLabels.KEEP}
                    </Button>
                  </Stack>
                </Card.Header>
                <Card.Body>
                  <ReactMarkdown>{row["Advice Content"]}</ReactMarkdown>
                </Card.Body>
              </Card>
            ))}
          </Stack>
        </Row>
      </Container>
    </div>
  );
};

export default PersonalizedAdvice;