import {Link, Outlet, useLoaderData, Form, redirect, useNavigation, useSubmit} from "react-router-dom";
import { useEffect } from "react";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import LearnSet from "../../Model/LearnSet.jsx";
import styled from "styled-components";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export async function action() {
    // const contact = await createContact();
    // return redirect(`/contacts/${contact.id}/edit`);
    return null;
}


const LearnSetContainer = styled.div`
    padding-top: 10px;
    background-color: aqua;
    font-size: 1px;
    overflow-y:auto;
    height: 90vh;
`

const LearnTitleRow = styled.div`
    background-color: red;
    padding-bottom: 10px;
    text-align: center;
`

const LearnSetRow = styled.div`
    background-color: aqua;
    padding-bottom: 20px;
`


export default function PracticeRoot() {
    const { contacts, q } = useLoaderData();
    const navigation = useNavigation();
    const submit = useSubmit();

    const searching =
        navigation.location &&
        new URLSearchParams(navigation.location.search).has(
            "q"
        );

    const choices = [{name: "Top 100", id: 1, numCompleted: 0, totalNumber: 100}, {name: "Top 100", id: 1, numCompleted: 0, totalNumber: 100}, {name: "Top 100", id: 1, numCompleted: 0, totalNumber: 100}, {name: "Top 100", id: 1, numCompleted: 0, totalNumber: 100}]
    // useEffect(() => {
    //     document.getElementById("q").value = q;
    // }, [q]);

    return (
        <Container style={{backgroundColor: "blue"}}>
            <LearnTitleRow as={Row}>
                <Col as={"h1"}>Practice Sets</Col>
                <Col as={"h2"}><FontAwesomeIcon icon="fa-solid fa-language" /> English -> German</Col>
            </LearnTitleRow>
            <Row>
                <LearnSetContainer as={Container} fluid={true}>
                    {choices.map(value => <LearnSetRow as={"Row"}><LearnSet learnSet={value}></LearnSet></LearnSetRow>)}
                </LearnSetContainer>
            </Row>
        </Container>
    );
}


export async function loader({ request }) {
    // const url = new URL(request.url);
    // const q = url.searchParams.get("q");
    // const contacts = await getContacts(q);
    // return { contacts, q };
    return 'null'
}