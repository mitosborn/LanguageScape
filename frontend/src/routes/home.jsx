import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import {Link, Outlet} from "react-router-dom";
import {Button, Col, FormControl, FormGroup, Row} from "react-bootstrap";

export default function Home() {
    return (
        <Container className={"p-0"} fluid={true}>
            <Row>
                <Col>
                    <Navbar bg="primary" variant="dark">
                        <Container fluid={true}>
                            <Navbar.Brand href="#home">LingScape</Navbar.Brand>
                            <Navbar.Toggle />
                            <Navbar.Collapse className="justify-content-end">
                                <Navbar.Text>
                                    Signed in as: <a href="#login">Mark Otto</a>
                                </Navbar.Text>
                            </Navbar.Collapse>
                        </Container>
                    </Navbar>
                </Col>
            </Row>
            <Row>
                <Col md={12}>
                    <Outlet></Outlet>
                </Col>
            </Row>
        </Container>
    );
}
