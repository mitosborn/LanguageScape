import {getBackendEndpoint} from "../../constants.js";

export async function getQuestions(query) {
    // await fakeNetwork(`getContacts:${query}`);
    // let contacts = await localforage.getItem("contacts");
    // if (!contacts) contacts = [];
    // if (query) {
    //     contacts = matchSorter(contacts, query, { keys: ["first", "last"] });
    // }
    console.log("before")
    console.log(query)
    let searchParams = new URLSearchParams()
    searchParams.append("username", "liebe")
    searchParams.append("learnset", query.language)
    searchParams.append("num_translations", query.numQuestions)
    searchParams.append('original_language', 'deu')
    searchParams.append('target_language', 'eng')
    console.log(searchParams.toString())
    let questions = await (await fetch(getBackendEndpoint() + `/translation?${searchParams.toString()}`)).json()
    console.log(questions)
    questions = questions.map((question) => ({...question, original_text : question['original_text'].replaceAll("\" \"","\"\n\"")}))
    return questions;
}

export async function submitQuestion(query) {
    const {username, learn_set_name, translation_id, result} = query;
    let urlParams = new URLSearchParams()
    urlParams.append("username", username)
    urlParams.append("learnset", learn_set_name)
    urlParams.append("translation_id", translation_id)
    urlParams.append("result", result)
    let promiseResult = await (await fetch(getBackendEndpoint() + `/translation?${urlParams.toString()}`, {'method': "POST"})).json()
    console.log(promiseResult)
}


export async function getLearnsets(query) {
    let searchParams = new URLSearchParams()
    searchParams.append("username", "liebe")
    searchParams.append("language", "deu_eng")
    let learnsets = await (await fetch(getBackendEndpoint()+ `/translation/learnsets?${searchParams.toString()}`)).json()
    // learnsets = learnsets.map(learnset => JSON.parse(learnset))
    console.log(learnsets)
    return learnsets
}


// export async function createContact() {
//     await fakeNetwork();
//     let id = Math.random().toString(36).substring(2, 9);
//     let contact = { id, createdAt: Date.now() };
//     let contacts = await getContacts();
//     contacts.unshift(contact);
//     await set(contacts);
//     return contact;
// }
//
// export async function getContact(id) {
//     await fakeNetwork(`contact:${id}`);
//     let contacts = await localforage.getItem("contacts");
//     let contact = contacts.find(contact => contact.id === id);
//     return contact ?? null;
// }
//
// export async function updateContact(id, updates) {
//     await fakeNetwork();
//     let contacts = await localforage.getItem("contacts");
//     let contact = contacts.find(contact => contact.id === id);
//     if (!contact) throw new Error("No contact found for", id);
//     Object.assign(contact, updates);
//     await set(contacts);
//     return contact;
// }
//
// export async function deleteContact(id) {
//     let contacts = await localforage.getItem("contacts");
//     let index = contacts.findIndex(contact => contact.id === id);
//     if (index > -1) {
//         contacts.splice(index, 1);
//         await set(contacts);
//         return true;
//     }
//     return false;
// }
//
// function set(contacts) {
//     return localforage.setItem("contacts", contacts);
// }
//
// // fake a cache, so we don't slow down stuff we've already seen
// let fakeCache = {};
//
// async function fakeNetwork(key) {
//     if (!key) {
//         fakeCache = {};
//     }
//
//     if (fakeCache[key]) {
//         return;
//     }
//
//     fakeCache[key] = true;
//     return new Promise(res => {
//         setTimeout(res, Math.random() * 800);
//     });
// }