import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import {Link, Outlet} from "react-router-dom";
import {Button, Col, FormControl, FormGroup, Row} from "react-bootstrap";
import {
    MDBContainer,
    MDBCollapse,
    MDBNavbar,
    MDBNavbarToggler,
    MDBIcon,
    MDBBtn,
} from 'mdb-react-ui-kit';

export default function NavBar() {
    return (
        <Container className={"p-0"} fluid={true}>
            <Row id={"main-navbar"}>
                <Col>
                    <Container className={"my-2"}>
                        <Row>
                            <Col className={"d-flex justify-content-center"}>
                            </Col>
                            <Col className={"d-flex justify-content-center"}>
                                <Link to={"/"} style={{ color: 'inherit', textDecoration: 'inherit'}}>
                                    <h1>LangScape</h1>
                                </Link>
                            </Col>
                            <Col className={"d-flex justify-content-center"}>
                                <Navbar.Text>
                                    Signed in as: <a href="#login">Mark Otto</a>
                                </Navbar.Text>
                            </Col>
                        </Row>
                    </Container>
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
// {/*<Row>*/}
// {/*    <Col>*/}
// //         <Navbar bg="primary" variant="dark">
// //             <Container fluid={true}>
// {/*                <Navbar.Brand href="#home">LingScape</Navbar.Brand>*/}
// {/*                <Navbar.Toggle />*/}
// {/*                <Navbar.Collapse className="justify-content-end">*/}
// {/*                    <Navbar.Text>*/}
// {/*                        Signed in as: <a href="#login">Mark Otto</a>*/}
// {/*                    </Navbar.Text>*/}
// {/*                </Navbar.Collapse>*/}
// {/*            </Container>*/}
// {/*        </Navbar>*/}
// {/*    </Col>*/}
// {/*</Row>*/}