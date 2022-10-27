import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import {Button} from "@mui/material";


export default function SessionSummary({continueLearning}) {
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
                        <h2>Questions Correct</h2>
                    </div>
                </Col>
            </Row>
            <Row>
                <Col lg={10} md={10} s={10} xs={12}>
                    <h2>Questions Missed</h2>
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