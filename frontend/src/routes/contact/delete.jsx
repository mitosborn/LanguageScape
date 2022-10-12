import { redirect } from "react-router-dom";
import { deleteContact } from "../../contacts.js";

export async function action({ params }) {
    console.log(params)
    await deleteContact(params.contactId);
    return redirect("/contacts");
}

// Next button
// await fetcher.submit("./correct/1") -> /correct/:questionId, /incorrect/:questionId
// fetcher.load() -> set question to this

// Select answer: know answer already, show red/green based on correct/false