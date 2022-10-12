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
    const [disableButton, setDisableButton] = useState(false)
    const [selectedAnswerId, setSelectedAnswerId] = useState()
    const [correctAnswer, setCorrectAnswer] = useState(false)
    const style = createTheme({
        palette: {
            action: {
                background: "blue",
                disabled: "blue",
                selectedOpacity: 100,
                disabledOpacity: -1,
                
            },
        }
    });
    // const []
    // Disable button after clicking
    function checkAnswer(answer) {
        setDisableButton(true)
        // setSelectedAnswerId(answer)
        setCorrectAnswer(true)

    }
    return (
            <Container id="question-container">
                <Row>
                    <Col className={"d-flex justify-content-center m-5"}>
                            <h1>{question.sentence}</h1>
                    </Col>
                </Row>
                <Row className={"d-flex justify-content-center"}>
                    <Col md={4}>
                        <ThemeProvider theme={style}>
                            <div className="d-grid gap-3">
                                <Button disabled={disableButton} color={selectedAnswerId == 0 && correctAnswer? "success": selectedAnswerId == 0 && !correctAnswer ? "error" : "inherit"} variant="contained" size="lg" onClick={(e)=> checkAnswer(0)}>
                                    {question.choices[0]}
                                </Button>
                                <Button disabled={disableButton} color={selectedAnswerId == 1 && correctAnswer? "success": selectedAnswerId == 1 && !correctAnswer ? "error" : "common"} variant="contained" size="lg" onClick={()=> checkAnswer(1)}>
                                    {question.choices[1]}
                                </Button>
                            </div>
                        </ThemeProvider>
                    </Col>
                    <Col md={4}>
                        <ThemeProvider theme={style}>
                            <div className="d-grid gap-3">
                                <Button disabled={disableButton} color={selectedAnswerId == 2 && correctAnswer? "success": selectedAnswerId == 2 && !correctAnswer ? "error" : "common"} variant="contained" size="lg" onClick={()=> checkAnswer(2)}>
                                    {question.choices[2]}
                                </Button>
                                <Button disabled={disableButton} color={selectedAnswerId == 3 && correctAnswer? "success": selectedAnswerId == 3 && !correctAnswer ? "error" : "common"} variant="contained" size="lg" onClick={()=> checkAnswer(3)}>
                                    {question.choices[3]}
                                </Button>
                            </div>
                        </ThemeProvider>
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