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
import Index from "./routes/contact/index.jsx";
import Home from "./routes/home.jsx";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import MultipleChoiceQuestion, { loader as multipleChoiceLoader, action as multipleChoiceAction } from "./routes/practice/MultipleChoiceQuestion.jsx";
import PracticeRoot from "./routes/practice/PracticeRoot.jsx";
import {action as submitAction} from "./routes/practice/submit.jsx"

const router = createBrowserRouter([
    {
        path: "/",
        element: <Home />,
        errorElement: <ErrorPage />,
        // loader: rootLoader,
        // action: rootAction,
        children:
            [
                { index: true, element: <Index /> },
                {
                    path: "/contacts",
                    element: <ContactRoot />,
                    errorElement: <ErrorPage />,
                    loader: rootLoader,
                    action: rootAction,
                    children: [
                    {
                        path: ":contactId",
                        element: <Contact />,
                        loader: contactLoader,
                        action: contactAction
                    },
                    {
                        path: ":contactId/edit",
                        element: <EditContact />,
                        loader: contactLoader,
                        action: editAction,
                    },
                    {
                        path: ":contactId/destroy",
                        action: destroyAction,
                        errorElement: <div>Oops! There was an error.</div>
                    }
                ]
                },
                {
                    path: "/practice/:language",
                    element: <PracticeRoot />,
                    errorElement: <ErrorPage />,
                    loader: rootLoader,
                    action: rootAction,
                    children: [
                        {
                            path: ":mode",
                            element: <MultipleChoiceQuestion />,
                            loader: multipleChoiceLoader,
                            action: multipleChoiceAction
                        },
                        {
                            path: "submit",
                            action: submitAction,
                            errorElement: <div>Oops! There was an error.</div>
                        },
                        // {
                        //     path: "incorrect/:questionId",
                        //     action: incorrectAction,
                        //     errorElement: <div>Oops! There was an error.</div>
                        // }
                    ]
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