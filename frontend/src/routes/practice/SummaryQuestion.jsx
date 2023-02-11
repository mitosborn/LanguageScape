import styled from "styled-components";

const SummaryQuestionText  = styled.div`
     display: inline;
`

const Blank = styled(SummaryQuestionText)`
    background-color: #FFFF00;
`


export default function SummaryQuestion({question}) {
    const {original_text, choices, answer} = question
    let sentence = original_text.replaceAll("\"","")
    let answerStart = sentence.indexOf(choices[answer])
    let answerEnd = answerStart + choices[answer].length
    let beforeAnswer = sentence.substring(0, answerStart)
    let afterAnswer = sentence.substring(answerEnd)

    return (
        <>
            <SummaryQuestionText as={"h4"}>{beforeAnswer}</SummaryQuestionText>
            <Blank as={"h4"}>{choices[answer]}</Blank>
            <SummaryQuestionText as={"h4"}>{afterAnswer}</SummaryQuestionText>
        </>
    )
}