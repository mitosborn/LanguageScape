import {getSummary} from "./summary.js";
import {Button} from "@mui/material";

export async function loader({ params }) {
    const summary = await getSummary(params.summaryID);
    if (!summary) {
        throw new Response("", {
            status: 404,
            statusText: "Not Found",
        });
    }
    return summary;
}

// export async function action({ request, params }) {
//     let formData = await request.formData();
//     return updateContact(params.contactId, {
//         favorite: formData.get("favorite") === "true",
//     });
// }

import {redirect, useLoaderData, useLocation, useNavigate} from "react-router-dom";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";

export default function Summary(){
    const navigate = useNavigate()
    const {language, mode, currentQuestion, numQuestions} = useLoaderData();

    function continueLearning() {
        navigate(`/practice/${language}/${mode}/${currentQuestion + numQuestions}/${numQuestions}`)
    }


    return (
        <Container>
            <Row>
                <Col className={"d-flex justify-content-center m-5"}>
                    <h1>Session Summary</h1>
                </Col>
            </Row>
            <Row className={"d-flex justify-content-center"}>
                <Col lg={10} md={10} s={10} xs={12}>
                    <div className="d-grid gap-3">
                        <h1>Questions Correct</h1>
                        <h1>Questions Missed</h1>
                    </div>
                </Col>
            </Row>
            <Row>
                <Col>
                    <div className={"d-flex justify-content-center my-4 gap-3"}>

                    </div>
                </Col>
            </Row>
        </Container>
    )
}