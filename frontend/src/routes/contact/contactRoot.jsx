import {Link, Outlet, NavLink, useLoaderData, Form, redirect, useNavigation, useSubmit} from "react-router-dom";
import { getContacts, createContact } from "../../contacts.js";
import { useEffect } from "react";
import Container from "react-bootstrap/Container";
import {Col, Row} from "react-bootstrap";

export async function action() {
    const contact = await createContact();
    return redirect(`/contacts/${contact.id}/edit`);
}

export default function ContactRoot() {
    const { contacts, q } = useLoaderData();
    const navigation = useNavigation();
    const submit = useSubmit();

    const searching =
        navigation.location &&
        new URLSearchParams(navigation.location.search).has(
            "q"
        );

    useEffect(() => {
        document.getElementById("q").value = q;
    }, [q]);

    return (
        <Container fluid={true} className={"p-0"}>
            <Row className={"m-0 p-0"}>
                <Col md={2}  id="sidebar">
                        <h1>React Router Contacts</h1>
                        <div>
                            <Form id="search-form" role="search">
                                <input
                                    id="q"
                                    className={searching ? "loading" : ""}
                                    aria-label="Search contacts"
                                    placeholder="Search"
                                    type="search"
                                    name="q"
                                    defaultValue={q}
                                    onChange={(event) => {
                                        const isFirstSearch = q == null;
                                        submit(event.currentTarget.form, {
                                            replace: !isFirstSearch,
                                        });
                                    }}
                                />
                                <div
                                    id="search-spinner"
                                    aria-hidden
                                    hidden={!searching}
                                />
                                <div
                                    className="sr-only"
                                    aria-live="polite"
                                ></div>
                            </Form>
                            <Form method="post">
                                <button type="submit">New</button>
                            </Form>
                        </div>
                        <nav>
                            {contacts.length ? (
                                <ul>
                                    {contacts.map((contact) => (
                                        <li key={contact.id}>
                                            <NavLink
                                                to={`${contact.id}`}
                                                className={({ isActive, isPending }) =>
                                                    isActive
                                                        ? "active"
                                                        : isPending
                                                            ? "pending"
                                                            : ""
                                                }
                                            >
                                                {contact.first || contact.last ? (
                                                    <>
                                                        {contact.first} {contact.last}
                                                    </>
                                                ) : (
                                                    <i>No Name</i>
                                                )}{" "}
                                                {contact.favorite && <span>???</span>}
                                            </NavLink>
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p>
                                    <i>No contacts</i>
                                </p>
                            )}
                        </nav>
                </Col>
                <Col md={10} id="detail" style={{"backgroundColor":"pink"}} className={navigation.state === "loading" ? "loading" : ""}>
                    <Outlet />
                </Col>
            </Row>
        </Container>
    );
}


export async function loader({ request }) {
    const url = new URL(request.url);
    const q = url.searchParams.get("q");
    const contacts = await getContacts(q);
    return { contacts, q };
}