import {Col, Row} from "react-bootstrap";
import Container from "react-bootstrap/Container";


export default function PracticeNavBar({questionsCorrect, questionsWrong, numQuestions}) {
    console.log(questionsWrong, questionsCorrect)
    return (
        <Row>
            <Col>
                <Container className={"my-2"}>
                    <Row>
                        <Col className={"d-flex justify-content-center"}>
                            <h5>Correct: {questionsCorrect}</h5>
                        </Col>
                        <Col className={"d-flex justify-content-center"}>
                            <h5>Incorrect: {questionsWrong}</h5>
                        </Col>
                        <Col className={"d-flex justify-content-center"}>
                            <h5>Questions Left: {numQuestions - (questionsCorrect + questionsWrong)}</h5>
                        </Col>
                    </Row>
                </Container>
            </Col>
        </Row>
    )
}

