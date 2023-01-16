import {Col, Container, ListGroup, Row} from "react-bootstrap";
import SelectLanguageDropdown from "./SelectLanguageDropdown.jsx";

export default function SelectSpokenLang() {
    return (
        <Container className={"my-5"}>
            <Row>
                <Col>
                    <h2>Languages</h2>
                </Col>
                <Col >
                    <SelectLanguageDropdown/>
                </Col>
            </Row>
            <Row>
                <Col>
                    <div className={"d-flex justify-content-around py-2"}>
                        <h2>I want to learn</h2>
                    </div>
                </Col>
            </Row>
            <Row className={"d-flex justify-content-around"}>
                <Col>
                    <ListGroup defaultActiveKey="#link1">
                        <ListGroup.Item action href="#link1">
                            German
                        </ListGroup.Item>
                        <ListGroup.Item action href="#link2">
                            Spanish
                        </ListGroup.Item>
                        <ListGroup.Item action onClick={() => console.log("Clicked option")}>
                            French
                        </ListGroup.Item>
                    </ListGroup>
                </Col>
            </Row>
        </Container>
    );
}