import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import {Link, Outlet, useNavigate} from "react-router-dom";
import {Anchor, Col, Row} from "react-bootstrap";
import {Button} from "@mui/material";

export default function NavBar() {
    const navigate = useNavigate();
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
                                <a href={"/googleLogin"}>
                                    <Button>
                                    <Navbar.Text>
                                        Login with Google
                                    </Navbar.Text>
                                </Button>
                                </a>
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