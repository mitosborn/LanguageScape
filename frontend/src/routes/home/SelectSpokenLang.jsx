import {Col, Container, ListGroup, Row} from "react-bootstrap";
import SelectLanguageDropdown from "./SelectLanguageDropdown.jsx";
import {Link} from "react-router-dom";
import SelectSpokenLangItem from "./SelectSpokenLangItem.jsx";

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
                    <ListGroup>
                        <SelectSpokenLangItem language={"German"} link={"/practice/deu-eng"}/>
                        <SelectSpokenLangItem language={"Spanish"} link={"/practice/esp-eng"}/>
                        <SelectSpokenLangItem language={"French"} link={"/practice/fr-eng"}/>
                    </ListGroup>
                </Col>
            </Row>
        </Container>
    );
}