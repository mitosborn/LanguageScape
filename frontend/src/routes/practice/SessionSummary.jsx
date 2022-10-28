import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import {Button, List, ListItem} from "@mui/material";
import SummaryQuestion from "./SummaryQuestion.jsx";


export default function SessionSummary({continueLearning, questionsCorrect, questionsWrong}) {
    console.log(questionsCorrect, questionsWrong)
    return(
        <Container>
            <Row>
                <Col className={"d-flex justify-content-center my-4"}>
                    <h1>Session Summary</h1>
                </Col>
            </Row>
            <Row className={"d-flex justify-content-center"}>
                <Col>
                    <div className="gap-3">
                        <h2>✅ Questions Correct</h2>
                        <List sx={{ listStyleType: 'disc', pl: 5 }}>
                            {questionsCorrect.length > 0? questionsCorrect.map((question) => <ListItem sx={{ display: 'list-item' }}><SummaryQuestion question={question}/></ListItem>): <h4>Didn't get any, keep trying! 🙂</h4>}
                        </List>
                    </div>
                </Col>
            </Row>
            <Row>
                <Col lg={10} md={10} s={10} xs={12}>
                    <div className="gap-3">
                        <h2>❌ Questions Missed</h2>
                        <List sx={{ listStyleType: 'disc', pl: 5 }}>
                            {questionsWrong.length > 0? questionsWrong.map((question) => <ListItem sx={{ display: 'list-item' }}><SummaryQuestion question={question}/></ListItem>): <h4>All correct! 🚀</h4>}
                        </List>
                    </div>
                </Col>
            </Row>
            <Row>
                <Col>
                    <div className={"d-flex justify-content-center my-4 gap-3"}>
                        <Button onClick={() => continueLearning()}>Continue learning</Button>
                    </div>
                </Col>
            </Row>
        </Container>
    )
}