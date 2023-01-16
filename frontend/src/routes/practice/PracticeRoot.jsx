import {Link, Outlet, NavLink, useLoaderData, Form, redirect, useNavigation, useSubmit} from "react-router-dom";
import { getContacts, createContact } from "../../contacts.js";
import { useEffect } from "react";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";
import LearnSet from "../../Model/LearnSet.jsx";

export async function action() {
    // const contact = await createContact();
    // return redirect(`/contacts/${contact.id}/edit`);
    return null;
}

export default function PracticeRoot() {
    const { contacts, q } = useLoaderData();
    const navigation = useNavigation();
    const submit = useSubmit();

    const searching =
        navigation.location &&
        new URLSearchParams(navigation.location.search).has(
            "q"
        );

    const choices = [{name: "Top 100", id: 1, numCompleted: 0, totalNumber: 100}]
    // useEffect(() => {
    //     document.getElementById("q").value = q;
    // }, [q]);

    return (
        <div>
            <h1>Practice page</h1>
            <LearnSet learnSet={choices[0]}></LearnSet>
            <Outlet/>
        </div>
    );
}


export async function loader({ request }) {
    // const url = new URL(request.url);
    // const q = url.searchParams.get("q");
    // const contacts = await getContacts(q);
    // return { contacts, q };
    return 'null'
}