// import { getSummary } from "../../summary.js";

import {Button} from "@mui/material";

export async function loader({ params }) {
    // const summary = await getSummary(params.summaryID);
    // if (!summary) {
    //     throw new Response("", {
    //         status: 404,
    //         statusText: "Not Found",
    //     });
    // }
    // return summary;
    return ""
}

// export async function action({ request, params }) {
//     let formData = await request.formData();
//     return updateContact(params.contactId, {
//         favorite: formData.get("favorite") === "true",
//     });
// }

import {redirect, useLocation, useNavigate} from "react-router-dom";

export default function Summary(){
    const navigate = useNavigate()
    const {state} = useLocation();

    if (state == null) { // This statement doesn't run need; need to validate other ways
        redirect(('/'))
    } else {
        console.log(state)
    }

    function continueLearning() {
        let {language, mode, currentQuestion, numQuestions} = state
        navigate(`/practice/${language}/${mode}/${currentQuestion + numQuestions}/${numQuestions}`)
    }


    return <div>
        <Button color={"info"} variant="contained" size="lg" onClick={()=> continueLearning()}>
            {"Continue Learning"}
        </Button>
    </div>
}