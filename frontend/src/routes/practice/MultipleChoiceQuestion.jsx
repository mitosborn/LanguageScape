import {Form, useFetcher, useLoaderData} from "react-router-dom";
import { getContact, updateContact } from "../../contacts.js";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import {Button, createTheme, ThemeProvider} from "@mui/material";
import {useState} from "react";
import { common } from '@mui/material/colors';
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
    id: 1,
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
    const [selectedAnswerId, setSelectedAnswerId] = useState()
    const [questionAnswered, setQuestionAnswered] = useState(false)

    function checkAnswer(answer) {
        console.log(answer)
        if (selectedAnswerId == null) {
            setQuestionAnswered(true)
            setSelectedAnswerId(answer)
        }
    }
    return (
            <Container id="question-container">
                <Row>
                    <Col className={"d-flex justify-content-center m-5"}>
                            <h1>{question.sentence}</h1>
                    </Col>
                </Row>
                <Row className={"d-flex justify-content-center"}>
                    <Col lg={8} md={10} s={10} xs={12}>
                        <div className="d-grid gap-3">
                            <Button disabled={questionAnswered && selectedAnswerId !== 0 && question['answer'] !== 0} color={questionAnswered && question['answer'] === 0? "success": questionAnswered && question['answer'] !== 0 ? "error" : "common"} variant="contained" size="lg" onClick={(e)=> checkAnswer(0)}>
                                {question.choices[0]}
                            </Button>
                            <Button disabled={questionAnswered && selectedAnswerId !== 1 && question['answer'] !== 1} color={questionAnswered && question['answer'] === 1? "success": questionAnswered && question['answer'] !== 1 ? "error" : "common"} variant="contained" size="lg" onClick={()=> checkAnswer(1)}>
                                {question.choices[1]}
                            </Button>
                            <Button disabled={questionAnswered && selectedAnswerId !== 2 && question['answer'] !== 2} color={questionAnswered && question['answer'] === 2? "success": questionAnswered && question['answer'] !== 2 ? "error" : "common"} variant="contained" size="lg" onClick={()=> checkAnswer(2)}>
                                {question.choices[2]}
                            </Button>
                            <Button disabled={questionAnswered && selectedAnswerId !== 3 && question['answer'] !== 3} color={questionAnswered && question['answer'] === 3? "success": questionAnswered && question['answer'] !== 3 ? "error" : "common"} variant="contained" size="lg" onClick={()=> checkAnswer(3)}>
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