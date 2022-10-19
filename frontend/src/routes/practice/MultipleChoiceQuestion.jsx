import {Form, useActionData, useFetcher, useLoaderData, useSubmit} from "react-router-dom";
import { getContact, updateContact } from "../../contacts.js";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import {Button} from "@mui/material";
import {useState} from "react";
import {getQuestions, submitQuestion} from "./practice.js";
// TODO: Get all questions in one batch and iterate through them/use setQuestion()
export async function loader({ params }) {
    const questions = await getQuestions();
    if (!questions) {
        throw new Response("", {
            status: 404,
            statusText: "Not Found",
        });
    }
    return questions;
}

export async function action({ request, params }) {
    let formData = await request.formData();
    return submitQuestion(formData);
}

export default function MultipleChoiceQuestion() {
    let questionIdx = 0
    const questions = useLoaderData();
    const [question, setCurrentQuestion] = useState(questions[questionIdx])
    const [selectedAnswerId, setSelectedAnswerId] = useState()
    const [questionAnswered, setQuestionAnswered] = useState(false)
    const submit = useSubmit();

    function checkAnswer(answer) {
        console.log(answer)
        if (selectedAnswerId == null) {
            setQuestionAnswered(true)
            setSelectedAnswerId(answer)
        }
    }

    async function submitAnswer() {
        let formData = new FormData();
        formData.append("answer", "false")
        formData.append("id", "mbo2")
        submit(formData, {method: "post"})
    }

    function nextQuestion() {
        setCurrentQuestion(questions[++questionIdx])
        setSelectedAnswerId(null)
        setQuestionAnswered(false)

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
                <Row>
                    <Col>
                        <div className={"d-flex justify-content-center my-4 gap-3"}>
                            <Button hidden={!questionAnswered} color={"info"} variant="contained" size="lg" onClick={()=> nextQuestion()}>
                                {"Next Question"}
                            </Button>
                            <Button hidden={!questionAnswered} color={"info"} variant="contained" size="lg" onClick={()=> submitAnswer()}>
                                {"Submit"}
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