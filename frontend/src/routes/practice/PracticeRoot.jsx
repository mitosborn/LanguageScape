import {Link, Outlet, useLoaderData, Form, redirect, useNavigation, useSubmit} from "react-router-dom";
import { useEffect } from "react";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import LearnSet from "../../Model/LearnSet.jsx";
import styled from "styled-components";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {getLearnsets} from "./practice.js";

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
    padding: 5px 0;
    text-align: center;
`

const LearnSetRow = styled.div`
    background-color: aqua;
    padding-bottom: 20px;
`

const ChooseLearnsetContainer = styled.div`

`


export default function PracticeRoot() {
    const { language, targetLanguage, learnSets } = useLoaderData();
    const navigation = useNavigation();
    const submit = useSubmit();

    const searching =
        navigation.location &&
        new URLSearchParams(navigation.location.search).has(
            "q"
        );
    // useEffect(() => {
    //     document.getElementById("q").value = q;
    // }, [q]);

    return (
        <ChooseLearnsetContainer as={Container} fluid={true}>
            <LearnTitleRow as={Row}>
                <Col as={"h1"}>Practice Sets</Col>
                <Col as={"h2"}><FontAwesomeIcon icon="fa-solid fa-language" /> {language} -> {targetLanguage}</Col>
            </LearnTitleRow>
            <Row>
                <LearnSetContainer as={Container} fluid={true}>
                    {learnSets.map(value => <LearnSetRow as={"Row"}><LearnSet learnSet={value}></LearnSet></LearnSetRow>)}
                </LearnSetContainer>
            </Row>
        </ChooseLearnsetContainer>
    );
}


export async function loader({request, params}) {
    console.log(params)
    const learnsets = await getLearnsets(params);
    console.log(learnsets)
    return {language: "English", targetLanguage: "German", learnSets: [{name: "Top 100", id: 1, numCompleted: 0, totalNumber: 100, description: "LS1"}, {name: "Top 100", id: 1, numCompleted: 0, totalNumber: 100, description: "LS2"}, {name: "Top 100", id: 1, numCompleted: 0, totalNumber: 100, description: "LS3"}, {name: "Top 100", id: 1, numCompleted: 0, totalNumber: 100, description: "LS4"}]}
}