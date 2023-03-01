import {
    redirect,
    useLoaderData,
    useParams, useSubmit,
} from "react-router-dom";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import {Button} from "@mui/material";
import {useState} from "react";
import {getQuestions, submitQuestion} from "./practice.js";
import SessionSummary from "./SessionSummary.jsx";
import PracticeNavBar from "./PracticeNavBar.jsx";
import {updateContact} from "../../contacts.js";
// TODO: Get all questions in one batch and iterate through them/use setQuestion()
export async function loader({ params }) {
    const questions = await getQuestions(params);
    console.log("invoked loader")
    if (!questions) {
        throw new Response("", {
            status: 404,
            statusText: "ERROR: No questions from backend",
        });
    }
    return questions;
}

export async function action({ request, params }) {
    const {language, learnSetId, currentQuestion, numQuestions} = params
    return redirect(`/mc/${language}/${learnSetId}/${parseInt(currentQuestion) + parseInt(numQuestions)}/${numQuestions}`);
}

// Send data back to backend -> backend returns session ID w/ summary of num right/wrong, etc
export default function MultipleChoiceQuestion() {
    const [questionIdx, setQuestionIdx] = useState(0)
    const [questionsCorrect, setQuestionsCorrect] = useState([])
    const [questionsWrong, setQuestionsWrong] = useState([])
    const questions = useLoaderData();
    const [selectedAnswerId, setSelectedAnswerId] = useState(-1)
    const [questionAnswered, setQuestionAnswered] = useState(false)
    const [showSummary, setShowSummary] = useState(false)
    const submit = useSubmit();
    const {numQuestions} = useParams()

    function checkAnswer(answer) {
        if (selectedAnswerId === -1) {
            setQuestionAnswered(true)
            setSelectedAnswerId(answer)
            if (answer === questions[questionIdx]['answer']) {
                setQuestionsCorrect([...questionsCorrect, questions[questionIdx]])

            }
            else {
                setQuestionsWrong([...questionsWrong, questions[questionIdx]])
            }
        }
    }

    function continueLearning() {
        setShowSummary(false)
        setQuestionAnswered(false)
        setSelectedAnswerId(-1)
        setQuestionIdx(0)
        setQuestionsCorrect([])
        setQuestionsWrong([])
        submit(null, {method: "post"})
        // redirect(`/practice/${language}/${mode}/${parseInt(currentQuestion) + parseInt(numQuestions)}/${numQuestions}`)
    }
    // async function showSummary() {
    //     // let formData = new FormData();
    //     // formData.append("answer", "false")
    //     // formData.append("id", "mbo2")
    //     // submit(formData, {method: "post"})
    //     setShowSummary(true)
    //
    // }

    // function uploadAnswer() {
    //     // let formData = new FormData();
    //     // formData.append("answer", "false")
    //     // formData.append("id", "mbo2")
    //     // submit(formData, {method: "post"})
    //     let promise = submitQuestion({});
    // }

    function nextQuestion() {
        if (questionIdx + 1 === questions.length){
            setShowSummary(true)
        }
        else {
            // setCurrentQuestion(questions[questionIdx + 1])
            console.log(questionIdx)
            setQuestionIdx(questionIdx + 1)
            setSelectedAnswerId(-1)
            setQuestionAnswered(false)
            return submitQuestion({})
        }

    }
    return (
        <>
            <PracticeNavBar questionsCorrect={questionsCorrect} questionsWrong={questionsWrong} numQuestions={numQuestions}/>
            {showSummary ?
               <SessionSummary questionsCorrect={questionsCorrect} questionsWrong={questionsWrong} continueLearning={() => continueLearning()} />
                : <Container id="question-container">
                    <Row>
                        <Col className={"d-flex justify-content-center m-5"}>
                            {questionAnswered? <h1 >{questions[questionIdx].original_text}</h1>: <h1 >{questions[questionIdx].original_text.replace(questions[questionIdx].choices[questions[questionIdx]['answer']], '_'.repeat(questions[questionIdx].choices[questions[questionIdx]['answer']].length))}</h1>}
                        </Col>
                    </Row>
                    <Row className={"d-flex justify-content-center"}>
                        <Col lg={8} md={10} s={10} xs={12}>
                            <div className="d-grid gap-3">
                                <Button disabled={questionAnswered && selectedAnswerId !== 0 && questions[questionIdx]['answer'] !== 0} color={questionAnswered && questions[questionIdx]['answer'] === 0? "success": questionAnswered && questions[questionIdx]['answer'] !== 0 ? "error" : "common"} variant="contained" size="lg" onClick={(e)=> checkAnswer(0)}>
                                    {questions[questionIdx].choices[0]}
                                </Button>
                                <Button disabled={questionAnswered && selectedAnswerId !== 1 && questions[questionIdx]['answer'] !== 1} color={questionAnswered && questions[questionIdx]['answer'] === 1? "success": questionAnswered && questions[questionIdx]['answer'] !== 1 ? "error" : "common"} variant="contained" size="lg" onClick={()=> checkAnswer(1)}>
                                    {questions[questionIdx].choices[1]}
                                </Button>
                                <Button disabled={questionAnswered && selectedAnswerId !== 2 && questions[questionIdx]['answer'] !== 2} color={questionAnswered && questions[questionIdx]['answer'] === 2? "success": questionAnswered && questions[questionIdx]['answer'] !== 2 ? "error" : "common"} variant="contained" size="lg" onClick={()=> checkAnswer(2)}>
                                    {questions[questionIdx].choices[2]}
                                </Button>
                                <Button disabled={questionAnswered && selectedAnswerId !== 3 && questions[questionIdx]['answer'] !== 3} color={questionAnswered && questions[questionIdx]['answer'] === 3? "success": questionAnswered && questions[questionIdx]['answer'] !== 3 ? "error" : "common"} variant="contained" size="lg" onClick={()=> checkAnswer(3)}>
                                    {questions[questionIdx].choices[3]}
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
                                <Button hidden={!questionAnswered} color={"info"} variant="contained" size="lg" onClick={()=> setShowSummary(true)}>
                                    {"Summary"}
                                </Button>
                            </div>
                        </Col>
                    </Row>
                </Container>}
        </>
    );
}
