import {
    useLoaderData,
    useNavigate,
    useParams,
} from "react-router-dom";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import {Button} from "@mui/material";
import {useState} from "react";
import {getQuestions} from "./practice.js";
import SessionSummary from "./SessionSummary.jsx";
import PracticeNavBar from "./PracticeNavBar.jsx";
// TODO: Get all questions in one batch and iterate through them/use setQuestion()
export async function loader({ params }) {
    const questions = await getQuestions(params.numQuestions);
    console.log("invoked loader")
    if (!questions) {
        throw new Response("", {
            status: 404,
            statusText: "ERROR: No questions from backend",
        });
    }
    return questions;
}

// export async function action({ request, params }) {
//     let formData = await request.formData();
//     // Send request to backend
//     let sessionID = 1
//     console.log("Called MC action")
//     console.log(request, params)
//     return redirect(`/summary`)
// }
// Send data back to backend -> backend returns session ID w/ summary of num right/wrong, etc
export default function MultipleChoiceQuestion() {
    const [questionIdx, setQuestionIdx] = useState(0)
    const [questionsCorrect, setQuestionsCorrect] = useState(0)
    const [questionsWrong, setQuestionsWrong] = useState(0)

    const questions = useLoaderData();
    const [question, setCurrentQuestion] = useState(questions[questionIdx])
    const [selectedAnswerId, setSelectedAnswerId] = useState(-1)
    const [questionAnswered, setQuestionAnswered] = useState(false)
    const [showSummary, setShowSummary] = useState(true)
    const navigate = useNavigate();
    const {language, mode, currentQuestion, numQuestions} = useParams()

    function checkAnswer(answer) {
        if (selectedAnswerId === -1) {
            setQuestionAnswered(true)
            setSelectedAnswerId(answer)
            if (answer === question['answer']) {
                setQuestionsCorrect(questionsCorrect + 1)
            }
            else {
                setQuestionsWrong(questionsWrong + 1)
            }
        }
    }

    function continueLearning() {
        console.log(language, mode, currentQuestion, numQuestions)
        navigate(`/practice/${language}/${mode}/${parseInt(currentQuestion) + parseInt(numQuestions)}/${numQuestions}`)
        setShowSummary(false)
        setQuestionAnswered(false)
        setSelectedAnswerId(-1)
    }
    async function submitAnswer() {
        // let formData = new FormData();
        // formData.append("answer", "false")
        // formData.append("id", "mbo2")
        // submit(formData, {method: "post"})
        setShowSummary(true)
        // navigate("/summary", {
        //     state: { ...params }
        // })
    }
    function nextQuestion() {
        if (questionIdx + 1 === questions.length){
            setShowSummary(true)
        }
        else {
            setQuestionIdx(questionIdx + 1)
            setCurrentQuestion(questions[questionIdx])
            console.log(questionIdx)
            setSelectedAnswerId(-1)
            setQuestionAnswered(false)
        }

    }
    return (
        <>
            <PracticeNavBar questionsCorrect={questionsCorrect} questionsWrong={questionsWrong} numQuestions={numQuestions}/>
            {showSummary ?
               <SessionSummary continueLearning={() => continueLearning()} />
                : <Container id="question-container">
                    <Row>
                        <Col className={"d-flex justify-content-center m-5"}>
                            {questionAnswered? <h1 >{question.sentence}</h1>: <h1 >{question.sentence.replace(question.choices[question['answer']], '_'.repeat(question.choices[question['answer']].length))}</h1>}
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
                                    {"Summary"}
                                </Button>
                            </div>
                        </Col>
                    </Row>
                </Container>}
        </>
    );
}
