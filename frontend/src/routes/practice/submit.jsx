import { redirect } from "react-router-dom";

export async function action({request, params}) {
    return redirect("/contacts");
}