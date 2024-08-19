import { useState } from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
// import './PostItNote.css'; // Import the CSS file for styling

const Notes = () => {
    const [isMinimized, setIsMinimized] = useState(true);
    const [noteContent, setNoteContent] = useState('This is a page for notes, click the save icon to export to a text file');


    const toggleMinimize = () => {
      setIsMinimized(prevState => !prevState);
    };

    const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setNoteContent(e.target.value);
      };

    const saveNote = () => {
        const blob = new Blob([noteContent], { type: 'text/plain;charset=utf-8' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'Notes.txt';
        link.click();
        window.URL.revokeObjectURL(url);
      };
    
  
    return (
      <Card >
        <div className={`post-it-note ${isMinimized ? 'minimized' : ''}`} style={{padding:'10px', paddingTop:'0px', paddingBottom:'0px'}}>
            <Container>
                <div className="post-it-header">
                    <Row className='align-items-center'>
                        <Col className='d-flex justify-content-start'>
                            <span>Notes</span>            
                        </Col>
                        <Col className='d-flex justify-content-end'>
                            <Button id="save-btn" variant='light' onClick={saveNote}>
                                💾 
                            </Button>
                            <Button id="minimize-btn" variant='light'onClick={toggleMinimize}>
                                {isMinimized ? '+' : '-'}
                            </Button>
                        </Col>
                    </Row>
                </div>
                <Row>
                    {!isMinimized && (
                        <textarea
                        className="post-it-body"
                        value={noteContent}
                        onChange={handleContentChange}
                        rows={10}
                        style={{width: '30vw', backgroundColor:'white', color: 'black'}}
                        />
                    )}
                </Row>
            </Container>            
        </div>
      </Card>
    );
};

export default Notes;