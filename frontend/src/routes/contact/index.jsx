import {Col, Container, ListGroup, Row} from "react-bootstrap";

export default function Index() {
    return (
        <Container className={"m-5"}>
            <Row>
                <Col>
                    <ListGroup defaultActiveKey="#link1">
                        <ListGroup.Item action href="#link1">
                            Link 1
                        </ListGroup.Item>
                        <ListGroup.Item action href="#link2" disabled>
                            Link 2
                        </ListGroup.Item>
                        <ListGroup.Item action onClick={() => console.log("Clicked option")}>
                            This one is a button
                        </ListGroup.Item>
                    </ListGroup>
                </Col>
            </Row>
        </Container>
    );
}