import React from "react";
import ReactDOM from "react-dom/client";
import {
    createBrowserRouter,
    RouterProvider,
    Route,
} from "react-router-dom";
import "./index.css";
import ContactRoot, { loader as rootLoader, action as rootAction } from "./routes/contact/contactRoot.jsx";
import ErrorPage from "./error-page.jsx";
import Contact, {loader as contactLoader, action as contactAction} from "./routes/contact/contact.jsx";
import EditContact, {action as editAction} from "./routes/contact/edit.jsx";
import {action as destroyAction } from "./routes/contact/delete.jsx";
import SelectSpokenLang from "./routes/home/SelectSpokenLang.jsx";
import NavBar from "./routes/home/NavBar.jsx";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import MultipleChoiceQuestion, { loader as multipleChoiceLoader, action as multipleChoiceAction} from "./routes/practice/MultipleChoiceQuestion.jsx";
import Summary, {loader as summaryLoader} from "./routes/practice/Summary.jsx";
import PracticeRoot, {action as practiceAction, loader as practiceLoader} from "./routes/practice/PracticeRoot.jsx";
import {action as submitAction} from "./routes/practice/submit.jsx"

const router = createBrowserRouter([
    {
        path: "/",
        element: <NavBar/>,
        errorElement: <ErrorPage/>,
        // loader: rootLoader,
        // action: rootAction,
        children:
            [
                { index: true, element: <SelectSpokenLang/> },
                {
                    path: "/practice/:language",
                    element: <PracticeRoot/>,
                    errorElement: <ErrorPage/>,
                    loader: practiceLoader,
                    action: practiceAction,
                    children: []
                },
                {
                    path: "mc/:language/:learnSetId/:currentQuestion/:numQuestions",
                    element: <MultipleChoiceQuestion/>,
                    loader: multipleChoiceLoader,
                    action: multipleChoiceAction
                },
                {
                    path: "/summary",
                    element: <Summary />,
                    loader: summaryLoader,
                }
// langId/questionType
    //deu-eng (Fetch available exercises/choices)
            // Choose Fill-in-blank or Multiple Choice
            ]
    },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>
);