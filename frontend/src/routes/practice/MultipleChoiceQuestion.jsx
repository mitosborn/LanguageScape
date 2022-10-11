import {Form, useFetcher, useLoaderData} from "react-router-dom";
import { getContact, updateContact } from "../../contacts.js";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import {Button} from "@mui/material";

export async function loader({ params }) {
    // const contact = await getContact(params.contactId);
    // if (!contact) {
    //     throw new Response("", {
    //         status: 404,
    //         statusText: "Not Found",
    //     });
    // }
    return question;
}

export async function action({ request, params }) {
    let formData = await request.formData();
    return updateContact(params.contactId, {
        favorite: formData.get("favorite") === "true",
    });
}

let question = {
    sentence : "Ich gehe ___ Berliner Kirche",
    answer: 1,
    choices: ["ins", "in die", "auf der", "zum"]
}

async function submit({ request, params }) {
    let formData = await request.formData();
    return updateContact(params.contactId, {
        favorite: formData.get("favorite") === "true",
    });
}


export default function MultipleChoiceQuestion() {
    const question = useLoaderData();
    return (
            <Container id="question-container">
                <Row>
                    <Col className={"d-flex justify-content-center m-5"}>
                            <h1>{question.sentence}</h1>
                    </Col>
                </Row>
                <Row className={"d-flex justify-content-center"}>
                    <Col md={4}>
                        <div className="d-grid gap-3">
                            <Button variant="primary" size="lg">
                                {question.choices[0]}
                            </Button>
                            <Button variant="secondary" size="lg">
                                {question.choices[1]}
                            </Button>
                        </div>
                    </Col>
                    <Col md={4}>
                        <div className="d-grid gap-3">
                            <Button variant="primary" size="lg">
                                {question.choices[2]}
                            </Button>
                            <Button variant="secondary" size="lg">
                                {question.choices[3]}
                            </Button>
                        </div>
                    </Col>
                </Row>

            </Container>
    );
}

function Favorite({ contact }) {
    const fetcher = useFetcher();

    let favorite = contact.favorite;
    if (fetcher.formData) {
        favorite = fetcher.formData.get("favorite") === "true";
    }

    return (
        <fetcher.Form method="post">
            <button
                name="favorite"
                value={favorite ? "false" : "true"}
                aria-label={
                    favorite
                        ? "Remove from favorites"
                        : "Add to favorites"
                }
            >
                {favorite ? "★" : "☆"}
            </button>
        </fetcher.Form>
    );
}