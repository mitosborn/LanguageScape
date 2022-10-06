import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import {Link, Outlet} from "react-router-dom";
import {Button, Col, FormControl, FormGroup, Row} from "react-bootstrap";

export default function Home() {
    return (
        <div className={"vh-100 vw-100"} style={{"backgroundColor": "blue"}}>
            <div className={"h-100 w-100"} id={"home"} style={{"backgroundColor": "yellow"}}>
                <Row style={{"height": "5vh"}}>
                    <Col>
                        <Navbar bg="light">
                            <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
                            <Navbar.Toggle aria-controls="basic-navbar-nav" />
                            <Navbar.Collapse id="basic-navbar-nav">
                                <Nav className="me-auto">
                                    <Nav.Link href="#home">Home</Nav.Link>
                                    <Nav.Link href="#link">Link</Nav.Link>
                                    <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                                        <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                                        <NavDropdown.Item href="#action/3.2">
                                            Another action
                                        </NavDropdown.Item>
                                        <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                                        <NavDropdown.Divider />
                                        <NavDropdown.Item href="#action/3.4">
                                            Separated link
                                        </NavDropdown.Item>
                                    </NavDropdown>
                                </Nav>
                            </Navbar.Collapse>
                        </Navbar>
                    </Col>
                </Row>
                <Row style={{"height": "95vh"}}>
                    <Col style={{"backgroundColor": "black"}}>
                        <Outlet></Outlet>
                    </Col>
                </Row>
            </div>
        </div>
    );
}
