import {Col, Row} from "react-bootstrap";
import Container from "react-bootstrap/Container";


export default function PracticeNavBar({questionsCorrect, questionsWrong, numQuestions}) {

    console.log(questionsWrong, questionsCorrect)
    return (
        <Row id={"practice-navbar"}>
            <Col>
                <Container className={"my-2"}>
                    <Row>
                        <Col className={"d-flex justify-content-center"}>
                            <h4>Correct: {questionsCorrect.length}</h4>
                        </Col>
                        <Col className={"d-flex justify-content-center"}>
                            <h4>Incorrect: {questionsWrong.length}</h4>
                        </Col>
                        <Col className={"d-flex justify-content-center"}>
                            <h4>Questions Left: {numQuestions - (questionsCorrect.length + questionsWrong.length)}</h4>
                        </Col>
                    </Row>
                </Container>
            </Col>
        </Row>
    )
}

